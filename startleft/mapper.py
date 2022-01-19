import logging
import uuid
import re

logger = logging.getLogger(__name__)

DEFAULT_TRUSTZONE = "b61d6911-338d-46a8-9f39-8dcd24abfe91"


def format_AWS_Fns(source_objects):
    if 'Fn::ImportValue' in source_objects:
        source_objects = get_import_value_resource_name(source_objects['Fn::ImportValue'])
    elif 'Fn::GetAtt' in source_objects:
        source_objects = source_objects['Fn::GetAtt'][0]
    return source_objects


def format_source_objects(source_objects):
    if isinstance(source_objects, dict):
        source_objects = format_AWS_Fns(source_objects)
    if isinstance(source_objects, str):
        source_objects = [source_objects]

    return source_objects


def get_mappings_for_name_and_tags(mapping_definition):
    mapping_tags = None
    if "name" in mapping_definition:
        mapping_name = mapping_definition["name"]
    else:
        logger.debug(f"Required mandatory field: 'name' in mapping definition: {mapping_definition}")
    if "tags" in mapping_definition:
        mapping_tags = mapping_definition["tags"]
    return mapping_name, mapping_tags


def get_tags(source_model, source_object, mapping):
    c_tags = []
    if mapping is not None:
        if isinstance(mapping, list):
            for tag in mapping:
                c_tags.append(source_model.search(tag, source=source_object))
        else:
            c_tags.append(source_model.search(mapping, source=source_object))

    return c_tags


def set_optional_parameters_to_resource(resource, mapping_tags, resource_tags, singleton_multiple_name=None,
                                        singleton_multiple_tags=None):
    if mapping_tags is not None and resource_tags is not None and len(
            list(filter(lambda tag: tag is not None and tag is not '', resource_tags))) > 0:
        resource["tags"] = resource_tags
    if singleton_multiple_name is not None:
        resource["singleton_multiple_name"] = singleton_multiple_name
    if mapping_tags is not None and singleton_multiple_tags is not None:
        resource["singleton_multiple_tags"] = singleton_multiple_tags

    return resource


def get_altsource_mapping_path_value(source_model, alt_source_object, mapping_path):
    value = None

    mapping_path_value = source_model.search(mapping_path, source=alt_source_object)
    if isinstance(mapping_path_value, str):
        value = mapping_path_value
    elif isinstance(mapping_path_value, dict):
        if "Fn::Join" in mapping_path_value:
            value = []
            separator = mapping_path_value["Fn::Join"][0]
            for e in mapping_path_value["Fn::Join"][1]:
                if isinstance(e, str):
                    value.append(e)
                else:
                    pass

            value = separator.join(value)
        elif "Fn::Sub" in mapping_path_value:
            value = mapping_path_value["Fn::Sub"]

    return value


def get_import_value_resource_name(import_value_string):
    # gets resource name from an AWS Fn::ImportValue field in format:
    # "Fn::ImportValue": "ECSFargateGoServiceStack:ExportsOutputFnGetAttResourceNameGroupIdNNNNNNNN"
    lower_limit = import_value_string.index("FnGetAtt")+len("FnGetAtt")
    upper_limit = import_value_string.index("GroupId")
    if isinstance(lower_limit, int) and isinstance(upper_limit, int):
        result = import_value_string[lower_limit:upper_limit]
        return result
    else:
        return None


class TrustzoneMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {}

    def run(self, source_model):
        trustzones = []

        if "$source" in self.mapping:
            source_objs = format_source_objects(source_model.search(self.mapping["$source"]))
        else:
            source_objs = [self.mapping]

        for source_obj in source_objs:
            trustzone = {"name": source_model.search(self.mapping["name"], source=source_obj),
                         "source": source_obj
                         }
            if "properties" in self.mapping:
                trustzone["properties"] = self.mapping["properties"]

            source_id = source_model.search(self.mapping["id"], source=trustzone)
            self.id_map[source_id] = source_id
            trustzone["id"] = source_id

            logger.debug(f"Added trustzone: [{trustzone['id']}][{trustzone['name']}]")
            trustzones.append(trustzone)

        return trustzones


class ComponentMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.source = None
        self.id_map = {}

    def run(self, source_model, id_parents):
        """
        Iterates through the source model and returns the parameters to create the components
        :param source_model:
        :param id_parents:
        :return:
        """
        components = []

        source_objects = format_source_objects(source_model.search(self.mapping["$source"], source=None))
        mapping_name, mapping_tags = get_mappings_for_name_and_tags(self.mapping)

        for source_object in source_objects:
            component_type = format_AWS_Fns(source_model.search(self.mapping["type"], source=source_object))
            component_name, singleton_multiple_name = self.__get_component_names(source_model, source_object,
                                                                                 mapping_name)
            parents, parents_from_component = self.__get_parent_resources_ids(source_model, source_object, id_parents,
                                                                              component_name)
            component_tags, singleton_multiple_tags = self.__get_component_tags(source_model, source_object,
                                                                                mapping_tags)

            for parent_number, parent_element in enumerate(parents):
                # If there is more than one parent (i.e. subnets), the component will replicated inside each
                component = {"name": component_name, "type": component_type, "source": source_object,
                             "parent": self.__get_parent_id(parent_element, parents_from_component, component_name)}

                if "properties" in self.mapping:
                    component["properties"] = self.mapping["properties"]
                component = set_optional_parameters_to_resource(component, mapping_tags, component_tags,
                                                                singleton_multiple_name, singleton_multiple_tags)
                component_id = self.__generate_id(source_model, component, component_name, parent_number)
                component["id"] = component_id

                # If the component is defining child components the ID must be saved in a parent dict
                if "$children" in self.mapping["$source"]:
                    logger.debug("Component is defining child components...")
                    children = source_model.search(self.mapping["$source"]["$children"], source=source_object)
                    # TODO: Alternative options for $path when nothing is returned
                    if children not in id_parents:
                        id_parents[children] = list()
                    id_parents[children].append(component_id)

                logger.debug(
                    f"Added component: [{component['id']}][{component['type']}] | Parent: [{component['parent']}]")
                components.append(component)
                logger.debug("")

        # Here we should already have all the components

        if "$altsource" in self.mapping and components == []:
            logger.debug("No components found. Trying to find components from alternative source")
            alt_source = self.mapping["$altsource"]

            for alt in alt_source:
                mapping_type = alt["$mappingType"]
                mapping_path = alt["$mappingPath"]
                mapping_lookups = alt["$mappingLookups"]
                alt_source_objects = format_source_objects(source_model.search(mapping_type, source=None))

                for alt_source_object in alt_source_objects:
                    value = get_altsource_mapping_path_value(source_model, alt_source_object, mapping_path)

                    for mapping_lookup in mapping_lookups:
                        result = re.match(mapping_lookup["regex"], value)

                        if result is not None:
                            if DEFAULT_TRUSTZONE not in self.id_map:
                                self.id_map[DEFAULT_TRUSTZONE] = str(uuid.uuid4())

                            mapping_name, mapping_tags = get_mappings_for_name_and_tags(mapping_lookup)
                            component_name, singleton_multiple_name = self.__get_component_names(source_model,
                                                                                                 alt_source_object,
                                                                                                 mapping_name)
                            component_tags, singleton_multiple_tags = self.__get_component_tags(source_model,
                                                                                                alt_source_object,
                                                                                                mapping_tags)
                            component = {"id": str(uuid.uuid4()), "name": component_name,
                                         "type": mapping_lookup["type"], "parent": self.id_map[DEFAULT_TRUSTZONE]}

                            component = set_optional_parameters_to_resource(component, mapping_tags, component_tags,
                                                                            singleton_multiple_name,
                                                                            singleton_multiple_tags)

                            components.append(component)

        return components

    def __get_component_names(self, source_model, source_object, mapping):
        singleton_multiple_name = None
        if self.__multiple_sources_mapping_inside(mapping):
            component_name, singleton_multiple_name = self.__get_component_singleton_names(source_model, source_object,
                                                                                           mapping)
        else:
            component_name = self.__get_component_individual_name(source_model, source_object, mapping)
        return component_name, singleton_multiple_name

    def __get_component_individual_name(self, source_model, source_object, mapping):
        if "name" in self.mapping:
            source_component_name = format_AWS_Fns(source_model.search(mapping, source=source_object))
            logger.debug(f"+Found source object with name {source_component_name}")
        else:
            source_component_name = None
            logger.error(f"+Found source object with name None")
        return source_component_name

    def __get_component_singleton_names(self, source_model, source_object, mapping):
        if "name" in self.mapping:
            source_component_name, source_component_multiple_name = source_model.search(mapping, source=source_object)
            source_component_name = format_AWS_Fns(source_component_name)
            logger.debug(f"+Found singleton source object with multiple name {source_component_name}")
        else:
            source_component_name = None
            logger.error(f"+Found singleton source object with name None")
        return source_component_name, source_component_multiple_name

    def __get_component_tags(self, source_model, source_object, mapping):
        component_tags = None
        singleton_multiple_tags = None

        if mapping is not None:
            if self.__multiple_sources_mapping_inside(mapping):
                component_tags, singleton_multiple_tags = self.__get_component_singleton_tags(source_model, source_object,
                                                                                              mapping)
            else:
                component_tags = get_tags(source_model, source_object, mapping)
        return component_tags, singleton_multiple_tags

    def __get_component_singleton_tags(self, source_model, source_object, mapping):
        c_tags = []
        c_multiple_tags = []

        if "tags" in self.mapping:
            if isinstance(mapping, list):
                for tag in mapping:
                    if self.__multiple_sources_mapping_inside(tag):
                        c_temp_tags, c_temp_multiple_tags = source_model.search(tag, source=source_object)
                        c_tags.append(c_temp_tags)
                        c_multiple_tags.append(c_temp_multiple_tags)
                    else:
                        c_temp_tags = source_model.search(tag, source=source_object)
                        c_tags.append(c_temp_tags)
                        c_multiple_tags.append(c_temp_tags)
            else:
                c_temp_tags, c_temp_multiple_tags = source_model.search(mapping, source=source_object)
                c_tags.append(c_temp_tags)
                c_multiple_tags.append(c_temp_multiple_tags)

        return c_tags, c_multiple_tags

    def __multiple_sources_mapping_inside(self, mapping_definition):
        return "$singleton" in self.mapping["$source"] and \
               len(list(filter(lambda obj: "$numberOfSources" in obj, mapping_definition))) > 0

    def __get_parent_resources_ids(self, source_model, source_object, id_parents, component_name):
        # Retrieves a list of parent resources (components or trustZones) of the element.
        parents_from_component = False
        if "parent" in self.mapping:
            if "$parent" in self.mapping["parent"]:
                # In this case the parent component is the one in charge of defining which components
                # are their children, so it's ID should be stored before reaching the child components
                # With $parent, it will check if the supposed id_parents exist,
                # otherwise performing a standard search using action inside $parent
                if len(id_parents) > 0:
                    parent = id_parents[component_name]
                    parents_from_component = True
                else:
                    parent = source_model.search(self.mapping["parent"]["$parent"], source=source_object)
            else:
                # Just takes the parent component from the "parent" field in the mapping file
                # TODO: What if the object can't find a parent component? Should it have a default parent in case the path didn't find anything?
                parent = source_model.search(self.mapping["parent"], source=source_object)
        else:
            parent = ""

        if isinstance(parent, list):
            if len(parent) == 0:
                parent = [DEFAULT_TRUSTZONE]
        if isinstance(parent, str):
            if parent == "":
                parent = [DEFAULT_TRUSTZONE]
            else:
                parent = [parent]

        return parent, parents_from_component

    def __get_parent_id(self, parent_element, parents_from_component, component_name):
        if parents_from_component:
            # If the parent component was detected outside the component we need to look at the parent dict
            parent_id = parent_element
            self.id_map[parent_element] = parent_id
            logger.debug(f"Component {component_name} gets parent ID from existing component")
        else:
            found = False

            logger.debug("Trying to get parent ID from existing component...")
            if parent_element in self.id_map:
                parent_id = self.id_map[parent_element]
                found = True
                logger.debug(f"Parent ID detected: [{parent_id}][{parent_element}]")
            if not found:
                logger.debug("ID not found. Trying to get parent ID from parent substring...")
                for key in self.id_map:
                    if key in parent_element:
                        parent_id = self.id_map[key]
                        found = True
                        logger.debug(f"Parent ID detected: [{parent_id}][{key}]")
                        break
            if not found:
                logger.debug("No ID found. Creating new parent ID...")
                parent_id = str(uuid.uuid4())
                self.id_map[parent_element] = parent_id

        return parent_id

    def __generate_id(self, source_model, component, component_name, parent_number):
        if "id" in self.mapping:
            source_id = source_model.search(self.mapping["id"], source=component)
        else:
            source_id = str(uuid.uuid4())

        # make a previous lookup on the list of parent mappings
        c_id = None
        if source_id is not None and len(self.id_map) > 0:
            if component_name in self.id_map.keys():
                c_id = self.id_map[component_name]
        # a new ID can be generated if there is more a parent and this is not the first one
        if c_id is None or parent_number > 0:
            c_id = str(uuid.uuid4())
        self.id_map[source_id] = c_id

        return c_id


class DataflowNodeMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {}

    def run(self, source_model, source):
        source_objs = source_model.search(self.mapping, source=source)
        if isinstance(source_objs, str):
            source_objs = [source_objs]
        return source_objs


class DataflowMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {}

    def run(self, source_model):

        dataflows = []

        source_objs = format_source_objects(source_model.search(self.mapping["$source"], source=None))
        mapping_name, mapping_tags = get_mappings_for_name_and_tags(self.mapping)

        for source_obj in source_objs:
            df_name = source_model.search(mapping_name, source=source_obj)

            source_mapper = DataflowNodeMapper(self.mapping["source"])
            destination_mapper = DataflowNodeMapper(self.mapping["destination"])
            source_nodes = source_mapper.run(source_model, source_obj)
            if source_nodes is not None and len(source_nodes) > 0:
                for source_node in source_nodes:
                    destination_nodes = destination_mapper.run(source_model, source_obj)
                    if destination_nodes is not None and len(destination_nodes) > 0:
                        for destination_node in destination_nodes:
                            # skip self referencing dataflows unless they are temporary (action $hub)
                            if "$hub" not in source_mapper.mapping\
                                    and "$hub" not in destination_mapper.mapping\
                                    and source_node == destination_node:
                                continue

                            dataflow = {"name": df_name}

                            if source_node in self.id_map:
                                source_node_id = self.id_map[source_node]
                            else:
                                #check first if is a temporary dataflow
                                if "$hub" in source_mapper.mapping:
                                    self.id_map[source_node] = "source-hub-"+source_node
                                    source_node_id = self.id_map[source_node]
                                else:
                                    # not generate component IDs that may have been generated on component mapping
                                    continue

                            if destination_node in self.id_map:
                                destination_node_id = self.id_map[destination_node]
                            else:
                                # check first if is a temporary dataflow
                                if "$hub" in destination_mapper.mapping:
                                    self.id_map[destination_node] = "destination-hub-"+destination_node
                                    destination_node_id = self.id_map[destination_node]
                                else:
                                    # not generate component IDs that may have been generated on component mapping
                                    continue

                            dataflow["source_node"] = source_node_id
                            dataflow["destination_node"] = destination_node_id
                            dataflow["source"] = source_obj
                            if "properties" in self.mapping:
                                dataflow["properties"] = self.mapping["properties"]
                            if "bidirectional" in self.mapping:
                                if self.mapping["bidirectional"] == "true":
                                    dataflow["bidirectional"] = True
                                elif self.mapping["bidirectional"] == "false":
                                    dataflow["bidirectional"] = False

                            source_id = source_model.search(self.mapping["id"], source=dataflow)
                            if source_id not in self.id_map:
                                df_id = str(uuid.uuid4())
                                self.id_map[source_id] = df_id
                            dataflow["id"] = df_id

                            dataflow_tags = get_tags(source_model, source_obj, mapping_tags)
                            dataflow = set_optional_parameters_to_resource(dataflow, mapping_tags, dataflow_tags)

                            dataflows.append(dataflow)
        return dataflows
