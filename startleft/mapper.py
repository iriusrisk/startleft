import logging
import uuid
import re

logger = logging.getLogger(__name__)

DEFAULT_TRUSTZONE = "b61d6911-338d-46a8-9f39-8dcd24abfe91"


class TrustzoneMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {}

    def run(self, source_model):
        trustzones = []

        if "$source" in self.mapping:
            source_objs = source_model.search(self.mapping["$source"])
            if not isinstance(source_objs, list):
                source_objs = [source_objs]
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

        source_objects = source_model.search(self.mapping["$source"], source=None)
        if not isinstance(source_objects, list):
            source_objects = [source_objects]

        for source_object in source_objects:
            component_type = source_model.search(self.mapping["type"], source=source_object)

            if "$singleton" in self.mapping["$source"] and "$numberOfSources" in self.mapping["name"]:
                component_name, singleton_multiple_name = self.__get_component_singleton_names(source_model,source_object)
            else:
                component_name = self.__get_component_name(source_model, source_object)

            parents, parents_from_component = self.__get_parent_resources_ids(source_model, source_object, id_parents, component_name)
            component_tags = self.__get_component_tags(source_model, source_object)

            for parent_number, parent_element in enumerate(parents):
                # If there is more than one parent (i.e. subnets), the component will replicated inside each
                component = {"name": component_name, "type": component_type, "tags": component_tags,
                             "parent": self.__get_parent_id(parent_element, parents_from_component, component_name),
                             "source": source_object}

                if "properties" in self.mapping:
                    component["properties"] = self.mapping["properties"]
                if "$singleton" in self.mapping["$source"] and "$numberOfSources" in self.mapping["name"]:
                    component["singleton_multiple_name"] = singleton_multiple_name

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


                logger.debug(f"Added component: [{component['id']}][{component['type']}] | Parent: [{component['parent']}]")
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

                alt_source_objects = source_model.search(mapping_type, source=None)
                if not isinstance(alt_source_objects, list):
                    alt_source_objects = [alt_source_objects]

                for alt_source_object in alt_source_objects:
                    value = self.__get_altsource_mapping_path_value(source_model, alt_source_object, mapping_path)

                    for x in mapping_lookups:
                        result = re.match(x["regex"], value)

                        if result is not None:
                            if DEFAULT_TRUSTZONE not in self.id_map:
                                self.id_map[DEFAULT_TRUSTZONE] = str(uuid.uuid4())
                            component = {"id": str(uuid.uuid4()), "name": x["name"], "type": x["type"], "tags": [],
                                         "parent": self.id_map[DEFAULT_TRUSTZONE]}
                            components.append(component)

        return components

    def __get_component_name(self, source_model, source_object):
        if "name" in self.mapping:
            source_component_name = source_model.search(self.mapping["name"], source=source_object)
            logger.debug(f"+Found source object with name {source_component_name}")
        else:
            source_component_name = None
            logger.error(f"+Found source object with name None")
        return source_component_name

    def __get_component_singleton_names(self, source_model, source_object):
        if "name" in self.mapping:
            source_component_name, source_component_multiple_name = source_model.search(self.mapping["name"],
                                                                                        source=source_object)
            logger.debug(f"+Found singleton source object with multiple name {source_component_name}")
        else:
            source_component_name = None
            logger.error(f"+Found singleton source object with name None")
        return source_component_name, source_component_multiple_name

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

    def __get_component_tags(self, source_model, source_object):
        c_tags = []
        if "tags" in self.mapping:
            if isinstance(self.mapping["tags"], list):
                for tag in self.mapping["tags"]:
                    c_tags.append(source_model.search(tag, source=source_object))
            else:
                c_tags.append(source_model.search(self.mapping["tags"], source=source_object))

        return c_tags

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

    def __get_altsource_mapping_path_value(self, source_model, alt_source_object, mapping_path):
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

        source_objs = source_model.search(self.mapping["$source"], source=None)
        if not isinstance(source_objs, list):
            source_objs = [source_objs]
        for source_obj in source_objs:
            df_name = source_model.search(self.mapping["name"], source=source_obj)

            source_mapper = DataflowNodeMapper(self.mapping["source"])
            destination_mapper = DataflowNodeMapper(self.mapping["destination"])
            source_nodes = source_mapper.run(source_model, source_obj)
            if source_nodes is not None and len(source_nodes) > 0:
                for source_node in source_nodes:
                    destination_nodes = destination_mapper.run(source_model, source_obj)
                    if destination_nodes is not None and len(destination_nodes) > 0:
                        for destination_node in destination_nodes:
                            # skip self referencing dataflows
                            if source_node == destination_node:
                                continue

                            dataflow = {"name": df_name}

                            if source_node in self.id_map:
                                source_node_id = self.id_map[source_node]
                            else:
                                # not generate component IDs that may have been generated on component mapping
                                continue

                            if destination_node in self.id_map:
                                destination_node_id = self.id_map[destination_node]
                            else:
                                # not generate components that may have been generated on components mapping
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

                            dataflows.append(dataflow)
        return dataflows
