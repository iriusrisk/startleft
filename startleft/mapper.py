import logging
import uuid
import re

logger = logging.getLogger(__name__)

DEFAULT_TRUSTZONE = "public-cloud"


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
                         "type": source_model.search(self.mapping["type"], source=source_obj),
                         "source": source_obj
                         }
            if "properties" in self.mapping:
                trustzone["properties"] = self.mapping["properties"]

            source_id = source_model.search(self.mapping["id"], source=trustzone)
            if source_id not in self.id_map:
                tz_id = str(uuid.uuid4())
                self.id_map[source_id] = tz_id
            else:
                tz_id = self.id_map[source_id]
            trustzone["id"] = tz_id

            logger.debug(f"Added trustzone: [{trustzone['id']}][{trustzone['name']}][{trustzone['type']}]")
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

        source_objs = source_model.search(self.mapping["$source"], source=None)
        if not isinstance(source_objs, list):
            source_objs = [source_objs]

        for source_obj in source_objs:

            # Retrieves the name from the source model
            if "name" in self.mapping:
                c_name = source_model.search(self.mapping["name"], source=source_obj)
                logger.debug(f"+Found source object with name {c_name}")
            else:
                c_name = None
                logger.error(f"+Found source object with name None")

            # Retrieves the parent component of the element.
            parents_from_component = False
            if "parent" in self.mapping:
                if "$parent" in self.mapping["parent"]:
                    # In this case the parent component is the one in charge of defining which components
                    # are their childs, so it's ID should be stored before reaching the child components
                    parent = id_parents[c_name]
                    parents_from_component = True
                else:
                    # Just takes the parent component from the "parent" field in the mapping file
                    # TODO: What if the object can't find a parent component? Should it have a default parent in case the path didn't find anything?
                    parent = source_model.search(self.mapping["parent"], source=source_obj)
            else:
                parent = ""

            # Retrieves the tags
            c_tags = []
            if "tags" in self.mapping:
                if isinstance(self.mapping["tags"], list):
                    for tag in self.mapping["tags"]:
                        c_tags.append(source_model.search(tag, source=source_obj))
                else:
                    c_tags.append(source_model.search(self.mapping["tags"], source=source_obj))

            c_type = source_model.search(self.mapping["type"], source=source_obj)

            if isinstance(parent, list):
                if len(parent) == 0:
                    parent = [DEFAULT_TRUSTZONE]
            if isinstance(parent, str):
                if parent == "":
                    parent = [DEFAULT_TRUSTZONE]
                else:
                    parent = [parent]
            for parent_element in parent:
                # A component won't be added if it has no parent component
                component = {"name": c_name, "type": c_type, "tags": c_tags}
                if parents_from_component:
                    # If the parent component was detected outside the component we need to look at the parent dict
                    parent_id = parent_element
                    self.id_map[parent_element] = parent_id
                    logger.debug(f"Component {c_name} gets parent ID from existing component")
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

                component["parent"] = parent_id
                component["source"] = source_obj

                if "properties" in self.mapping:
                    component["properties"] = self.mapping["properties"]

                if "id" in self.mapping:
                    source_id = source_model.search(self.mapping["id"], source=component)
                else:
                    source_id = str(uuid.uuid4())

                c_id = str(uuid.uuid4())
                self.id_map[source_id] = c_id
                component["id"] = c_id

                # If the component is defining child components the ID must be saved in a parent dict
                if "$children" in self.mapping["$source"]:
                    logger.debug("Component is defining child components...")
                    children = source_model.search(self.mapping["$source"]["$children"], source=source_obj)
                    # TODO: Alternative options for $path when nothing is returned
                    if children not in id_parents:
                        id_parents[children] = list()
                    id_parents[children].append(c_id)

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

                alt_source_objs = source_model.search(mapping_type, source=None)
                if not isinstance(alt_source_objs, list):
                    alt_source_objs = [alt_source_objs]

                for alt_source_obj in alt_source_objs:
                    mapping_path_value = source_model.search(mapping_path, source=alt_source_obj)

                    value = ""

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

                    for x in mapping_lookups:
                        result = re.match(x["regex"], value)

                        if result is not None:
                            if DEFAULT_TRUSTZONE not in self.id_map:
                                self.id_map[DEFAULT_TRUSTZONE] = str(uuid.uuid4())
                            component = {"id": str(uuid.uuid4()), "name": x["name"], "type": x["type"], "tags": [],
                                         "parent": self.id_map[DEFAULT_TRUSTZONE]}
                            components.append(component)

        return components


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
            df_type = source_model.search(self.mapping["type"], source=source_obj)

            from_mapper = DataflowNodeMapper(self.mapping["from"])
            to_mapper = DataflowNodeMapper(self.mapping["to"])
            for from_node in from_mapper.run(source_model, source_obj):
                for to_node in to_mapper.run(source_model, source_obj):
                    # skip self referencing dataflows
                    if from_node == to_node:
                        continue

                    dataflow = {"name": df_name, "type": df_type}

                    if from_node in self.id_map:
                        from_node_id = self.id_map[from_node]
                    else:
                        from_node_id = str(uuid.uuid4())
                        self.id_map[from_node] = from_node_id

                    if to_node in self.id_map:
                        to_node_id = self.id_map[to_node]
                    else:
                        to_node_id = str(uuid.uuid4())
                        self.id_map[to_node] = to_node_id

                    dataflow["from_node"] = from_node_id
                    dataflow["to_node"] = to_node_id
                    dataflow["source"] = source_obj
                    if "properties" in self.mapping:
                        dataflow["properties"] = self.mapping["properties"]

                    source_id = source_model.search(self.mapping["id"], source=dataflow)
                    if source_id not in self.id_map:
                        df_id = str(uuid.uuid4())
                        self.id_map[source_id] = df_id
                    dataflow["id"] = df_id

                    dataflows.append(dataflow)
        return dataflows
