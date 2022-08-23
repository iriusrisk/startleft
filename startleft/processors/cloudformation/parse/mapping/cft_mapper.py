import logging
import re
import uuid

logger = logging.getLogger(__name__)

DEFAULT_TRUSTZONE = "b61d6911-338d-46a8-9f39-8dcd24abfe91"


def get_first_element_from_list(values):
    return values[0] if isinstance(values, list) else values


def get_resource_name_from_resource_reference(resource_id_reference: str):
    return re.match(r"\$\{aws_[\w-]+\.([\w-]+)\.(id|arn|stream_arn)\}", resource_id_reference).group(1)


def get_variable_name_from_variable_reference(variable_reference: str):
    return variable_reference[variable_reference.find(".") + 1:variable_reference.find("}")]


def format_aws_fns(source_objects):
    if 'Fn::ImportValue' in source_objects:
        source_objects = get_import_value_resource_name(source_objects['Fn::ImportValue'])
    elif 'Fn::GetAtt' in source_objects:
        source_objects = source_objects['Fn::GetAtt'][0]
    return source_objects


def set_cidr_blocks(source_object, source_component_name, value):
    if "ingress" in source_object['Properties'] and source_object['Properties']['ingress'][0]['cidr_blocks'] == value:
        source_object['Properties']['ingress'][0]['cidr_blocks'] = [source_component_name]
    elif "egress" in source_object['Properties'] and source_object['Properties']['egress'][0]['cidr_blocks'] == value:
        source_object['Properties']['egress'][0]['cidr_blocks'] = [source_component_name]


def format_source_objects(source_objects):
    if isinstance(source_objects, dict):
        source_objects = format_aws_fns(source_objects)
    if isinstance(source_objects, str):
        source_objects = [source_objects]
    if source_objects is None:
        source_objects = []

    return source_objects


def get_mappings_for_name_and_tags(mapping_definition):
    mapping_name = None
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
                __search_and_add_tag(c_tags, tag, source_model, source_object)
        else:
            __search_and_add_tag(c_tags, mapping, source_model, source_object)

    return c_tags


def __search_and_add_tag(c_tags: [], query, source_model, source_object):
    tag = source_model.search(query, source=source_object)
    if isinstance(tag, str):
        c_tags.append(tag)


def set_optional_parameters_to_resource(resource, mapping_tags, resource_tags, singleton_multiple_name=None,
                                        singleton_multiple_tags=None):
    if mapping_tags is not None and resource_tags is not None and len(
            list(filter(lambda tag: tag is not None and tag != '', resource_tags))) > 0:
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
    lower_limit = import_value_string.index("FnGetAtt") + len("FnGetAtt")
    upper_limit = import_value_string.index("GroupId")
    if isinstance(lower_limit, int) and isinstance(upper_limit, int):
        result = import_value_string[lower_limit:upper_limit]
        return result
    else:
        return None


def repeated_type4_hub_definition_component(mapping, id_map, component_name):
    if "$ip" in str(mapping["name"]) or "$ip" in str(mapping["type"]):
        same_name_component = component_name in id_map
        return same_name_component
    else:
        return False


def create_core_dataflow(df_name, source_obj, source_resource_id, destination_resource_id):
    dataflow = {"name": df_name, "source": source_obj, "source_node": source_resource_id,
                "destination_node": destination_resource_id}
    return dataflow


class CloudformationTrustzoneMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {}

    def run(self, source_model):
        trustzones = []

        if "$source" in self.mapping:
            source_objs = format_source_objects(source_model.search(self.mapping["$source"]))
        else:
            source_objs = [self.mapping]

        logger.debug("Finding trustzones")
        for source_obj in source_objs:
            trustzone = {"name": source_model.search(self.mapping["name"], source=source_obj),
                         "source": source_obj
                         }
            if "properties" in self.mapping:
                trustzone["properties"] = self.mapping["properties"]

            source_id = source_model.search(self.mapping["id"], source=trustzone)
            self.id_map[source_id] = source_id
            trustzone["id"] = source_id

            logger.debug(f"Found trustzone: [{trustzone['id']}][{trustzone['name']}]")
            trustzones.append(trustzone)

        return trustzones


class CloudformationComponentMapper:
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
            component_type = format_aws_fns(source_model.search(self.mapping["type"], source=source_object))
            component_name, singleton_multiple_name = self.__get_component_names(source_model, source_object,
                                                                                 mapping_name)
            parent_names, parents_from_component = self.__get_parent_names(source_model, source_object, id_parents,
                                                                           component_name)
            component_tags, singleton_multiple_tags = self.__get_component_tags(source_model, source_object,
                                                                                mapping_tags)

            for parent_name_number, parent_name in enumerate(parent_names):
                # If there is more than one parent (i.e. subnets), the component will replicated inside each
                parent_ids = self.__get_parent_id(parent_name, parents_from_component, component_name)
                if isinstance(parent_ids, str):
                    parent_ids = [parent_ids]
                for parent_number, parent_id in enumerate(parent_ids):
                    base_component = {"name": component_name, "type": component_type, "source": source_object,
                                      "parent": parent_id}

                    if "properties" in self.mapping:
                        base_component["properties"] = self.mapping["properties"]
                    base_component = set_optional_parameters_to_resource(base_component, mapping_tags, component_tags,
                                                                         singleton_multiple_name,
                                                                         singleton_multiple_tags)

                    # Special case related with support components for Security Groups
                    # To avoid repeated components generated from AWS Cidr IP fields
                    if repeated_type4_hub_definition_component(self.mapping, self.id_map, component_name):
                        continue

                    component_ids = self.__generate_id(source_model, base_component, component_name, parent_name_number)

                    if isinstance(component_ids, str):
                        component_ids = [component_ids]

                    for component_number, component_id in enumerate(component_ids):
                        component = base_component.copy()
                        component["id"] = component_id

                        # If the component is defining child components the ID must be saved in a parent dict
                        if "$children" in self.mapping["$source"]:
                            logger.debug("Component is defining child components...")
                            child_name = source_model.search(self.mapping["$source"]["$children"], source=source_object)

                            if child_name not in self.id_map:
                                # This child has not been mapped yet but its ID must be created
                                # Because the own child mapping definition has no information about its own parent
                                child_id = str(uuid.uuid4())
                                self.id_map[child_name] = child_id
                            else:
                                # Every generated child is unique
                                # And has 1:1 correspondence with its parent
                                # But self.id_map is a dict that groups by name
                                # And the same parent and children may be in different subnets
                                # So for this $children case:
                                #  self.id_map[parent_name] = [parent_1_id, parent_2_id...parent_N_id]
                                #  self.id_map[child_name] = [child_parent_1_id, child_parent_2_id...child_parent_N_id]
                                child_id = str(uuid.uuid4())
                                if isinstance(self.id_map[child_name], str):
                                    self.id_map[child_name] = [self.id_map[child_name], child_id]
                                elif isinstance(self.id_map[child_name], list):
                                    self.id_map[child_name].append(child_id)
                            if child_id not in id_parents:
                                id_parents[child_id] = list()
                            id_parents[child_id].append(component_id)
                        elif "$skip" not in self.mapping["$source"] and "$parent" in self.mapping["parent"]:
                            # $parent and $children are related mappings
                            # In this case, component_id may be a list with a different treatment
                            if parent_number != component_number:
                                continue
                        # For the rest of cases that are not $children, id_parents must be set with new parents found
                        else:
                            if component_id not in id_parents:
                                id_parents[component_id] = parent_id

                        logger.debug(
                            f"Found component: [{component['id']}][{component['type']}] | Parent: [{component['parent']}]")
                        components.append(component)

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
            value = get_first_element_from_list(source_model.search(mapping, source=source_object))
            source_component_name = format_aws_fns(value)
            logger.debug(f"Found source object with name {source_component_name}")
        else:
            source_component_name = None
            logger.error(f"Found source object with name None")
        return source_component_name

    def __get_component_singleton_names(self, source_model, source_object, mapping):
        source_component_multiple_name = None
        if "name" in self.mapping:
            source_component_name, source_component_multiple_name = source_model.search(mapping, source=source_object)
            source_component_name = format_aws_fns(source_component_name)

            logger.debug(f"Found singleton source object with multiple name {source_component_name}")
        else:
            source_component_name = None
            logger.error(f"Found singleton source object with name None")
        return source_component_name, source_component_multiple_name

    def __get_component_tags(self, source_model, source_object, mapping):
        component_tags = None
        singleton_multiple_tags = None

        if mapping is not None:
            if self.__multiple_sources_mapping_inside(mapping):
                component_tags, singleton_multiple_tags = self.__get_component_singleton_tags(source_model,
                                                                                              source_object, mapping)
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

    def __get_parent_names(self, source_model, source_object, id_parents, component_name):
        # Retrieves a list of parent resource names (components or trustZones) of the element.
        parents_from_component = False
        if "parent" in self.mapping:
            if "$parent" in self.mapping["parent"]:
                # Special case with $parent, where the parent component is in charge of defining which components
                # are their children, so its ID should be stored before reaching the child components
                # With $parent, it will check if the supposed id_parents exist,
                # otherwise performing a standard search using action inside $parent
                if len(id_parents) > 0 and component_name in self.id_map:
                    component_id = self.id_map[component_name]
                    # for $parent elements, all parents have the same name (but IDs may be different)
                    if isinstance(component_id, list):
                        # so to get the name of the element, any of the children id is needed (the first, in this case)
                        component_id = component_id[0]
                    parent_ids = id_parents[component_id]
                    parent = []
                    for parent_id in parent_ids:
                        # reverse search in the dictionary of resource names
                        # some of those entries have got lists
                        for resource_name, resource_ids in self.id_map.items():
                            found = False
                            if isinstance(resource_ids, str):
                                if parent_id == resource_ids:
                                    parent = resource_name
                                    found = True
                                    break
                            elif isinstance(resource_ids, list):
                                for resource_id in resource_ids:
                                    if parent_id == resource_id:
                                        parent = resource_name
                                        found = True
                                        break
                            if found:
                                break

                    parents_from_component = True
                else:
                    parent = source_model.search(self.mapping["parent"]["$parent"], source=source_object)
            else:
                # Just takes the parent component from the "parent" field in the mapping file
                # If the object were not to find a parent component: use path or findFirst actions with default value
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
        parent_id = None
        if parents_from_component:
            # If the parent component was detected outside the component we need to look at the parent dict
            parent_id = self.id_map[parent_element]
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
            # The usual case, as "id" field is mandatory in mapping definitions
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
        if parent_number > 0:
            if isinstance(self.id_map[source_id], list):
                self.id_map[source_id].append(c_id)
            if isinstance(self.id_map[source_id], str):
                self.id_map[source_id] = [self.id_map[source_id], c_id]
        else:
            self.id_map[source_id] = c_id

        return c_id


class CloudformationDataflowNodeMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {}

    def run(self, source_model, source):
        return format_source_objects(source_model.search(self.mapping, source=source))


class CloudformationDataflowMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {}

    def run(self, source_model, id_dataflows):
        df_id = None
        dataflows = []

        source_objs = format_source_objects(source_model.search(self.mapping["$source"], source=None))
        mapping_name, mapping_tags = get_mappings_for_name_and_tags(self.mapping)

        for source_obj in source_objs:
            df_name = source_model.search(mapping_name, source=source_obj)

            source_mapper = CloudformationDataflowNodeMapper(self.mapping["source"])
            destination_mapper = CloudformationDataflowNodeMapper(self.mapping["destination"])
            source_resource_names = source_mapper.run(source_model, source_obj)
            destination_resource_names = destination_mapper.run(source_model, source_obj)
            hub_type = self.__determine_hub_mapping_type(source_mapper, destination_mapper)

            for source_resource_name in source_resource_names or []:
                # components should be located
                source_resource_ids = self.__get_dataflows_component_ids(source_resource_name)
                # if a component is not on list, it may be a Security Group
                if "$hub" in source_mapper.mapping:
                    if hub_type is not None:
                        source_resource_ids = [hub_type + source_resource_name]

                for source_resource_id in source_resource_ids or []:
                    for destination_resource_name in destination_resource_names or []:
                        destination_hub_type = None
                        # components should be located
                        destination_resource_ids = self.__get_dataflows_component_ids(destination_resource_name)

                        # if a component is not on list, it may be a Security Group
                        if "$hub" in destination_mapper.mapping:
                            if destination_resource_ids is None:
                                destination_resource_id_for_hub_mapping = ["hub-" + destination_resource_name]
                                self.id_map[destination_resource_name] = destination_resource_id_for_hub_mapping
                            if hub_type is not None:
                                destination_resource_ids = [hub_type + destination_resource_name]

                        if destination_resource_ids is None:
                            continue

                        for destination_resource_id in destination_resource_ids:
                            # skip self referencing dataflows unless they are temporary (action $hub)
                            if "$hub" not in source_mapper.mapping \
                                    and "$hub" not in destination_mapper.mapping \
                                    and source_resource_id == destination_resource_id:
                                continue

                            dataflow = create_core_dataflow(df_name, source_obj, source_resource_id
                                                            , destination_resource_id)
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

                            id_dataflows[source_resource_id] = {"hub_type": hub_type,
                                                                "destination_id": destination_resource_id}
                            dataflows.append(dataflow)
        return dataflows

    def __get_dataflows_component_ids(self, resource_name):
        node_ids = None
        if resource_name in self.id_map:
            node_ids = self.id_map[resource_name]
        if isinstance(node_ids, str):
            node_ids = [node_ids]
        return node_ids

    def __determine_hub_mapping_type(self, source_mapper, destination_mapper):

        # SG mapping type 2
        if "$hub" in source_mapper.mapping and "$hub" in destination_mapper.mapping:
            return "type2-hub-"

        # SG mappings: type 1
        elif "$hub" not in source_mapper.mapping and "$hub" in destination_mapper.mapping \
                and "$path" in source_mapper.mapping and "_key" in source_mapper.mapping["$path"]:
            return "type1-hub-"

        # SG mapping type 3 inbound
        elif "$hub" not in source_mapper.mapping and "$hub" in destination_mapper.mapping \
                and "$path" in destination_mapper.mapping["$hub"] \
                and "_key" in destination_mapper.mapping["$hub"]["$path"]:
            return "type3-hub-"

        # SG mapping type 3 outbound
        elif "$hub" in source_mapper.mapping and "$path" in source_mapper.mapping["$hub"] \
                and "_key" in source_mapper.mapping["$hub"]["$path"]:
            return "type3-hub-"

        else:
            return None
