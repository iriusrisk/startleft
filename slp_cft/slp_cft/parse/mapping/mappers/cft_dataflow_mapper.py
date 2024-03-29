import uuid

from slp_cft.slp_cft.parse.mapping.mappers.cft_base_mapper import CloudformationBaseMapper


class CloudformationDataflowMapper(CloudformationBaseMapper):
    def run(self, source_model, id_dataflows):
        df_id = None
        dataflows = []

        source_objs = self.format_source_objects(source_model.search(self.mapping["$source"], source=None))
        mapping_name, mapping_tags = self.get_mappings_for_name_and_tags(self.mapping)

        for source_obj in source_objs:
            df_name = source_model.search(mapping_name, source=source_obj)

            source_mapper = self.DataflowNodeMapper(self.mapping["source"])
            destination_mapper = self.DataflowNodeMapper(self.mapping["destination"])
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

                            dataflow = self.create_core_dataflow(df_name, source_obj, source_resource_id,
                                                                 destination_resource_id)

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

                            dataflow_tags = self.get_tags(source_model, source_obj, mapping_tags)
                            dataflow = self.set_optional_parameters_to_resource(dataflow, mapping_tags, dataflow_tags)

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

    class DataflowNodeMapper(CloudformationBaseMapper):
        def run(self, source_model, source):
            return self.format_source_objects(source_model.search(self.mapping, source=source))

