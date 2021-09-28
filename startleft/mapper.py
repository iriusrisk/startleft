import uuid

id_parents = dict()


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

            trustzones.append(trustzone)

        return trustzones


class ComponentMapper:
    def __init__(self, mapping):
        self.mapping = mapping
        self.source = None
        self.id_map = {}

    def run(self, source_model):
        """
        Iterates through the source model and returns the parameters to create the components
        :param source_model:
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
            else:
                c_name = None

            # Retrieves the parent component of the element.
            parentsFromComponent = False
            if "parent" in self.mapping:
                if "$parent" in self.mapping["parent"]:
                    # In this case the parent component is the one in charge of defining which components
                    # are their childs, so it's ID should be stored before reaching the child components
                    parent = id_parents[c_name]
                    parentsFromComponent = True
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
                    parent = ["public-cloud"]
            if isinstance(parent, str):
                if parent == "":
                    parent = ["public-cloud"]
                else:
                    parent = [parent]
            for parent_element in parent:
                # A component won't be added if it has no parent component
                component = {"name": c_name, "type": c_type, "tags": c_tags}

                if parentsFromComponent:
                    # If the parent component was detected outside the component we need to look at the parent dict
                    parent_id = parent_element
                    self.id_map[parent_element] = parent_id
                else:
                    found = False
                    if parent_element in self.id_map:
                        parent_id = self.id_map[parent_element]
                        found = True
                    if not found:
                        for key in self.id_map:
                            if key in parent_element:
                                parent_id = self.id_map[key]
                                found = True
                                break
                    if not found:
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
                    children = source_model.search(self.mapping["$source"]["$children"], source=source_obj)
                    # TODO: Alternative options for $path when nothing is returned
                    if children not in id_parents:
                        id_parents[children] = list()
                    id_parents[children].append(c_id)

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
