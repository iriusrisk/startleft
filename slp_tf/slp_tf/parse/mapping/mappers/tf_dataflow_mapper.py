from slp_tf.slp_tf.parse.mapping.mappers.tf_base_mapper import TerraformBaseMapper, is_terraform_resource_reference, \
    get_resource_id_from_resource_reference


class TerraformDataflowMapper(TerraformBaseMapper):
    def run(self, source_model, id_dataflows):
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

                            dataflow_tags = self.get_tags(source_model, source_obj, mapping_tags)
                            dataflow = self.set_optional_parameters_to_resource(dataflow, mapping_tags, dataflow_tags)

                            id_dataflows[source_resource_id] = {"hub_type": hub_type,
                                                                "destination_id": destination_resource_id}
                            dataflows.append(dataflow)
        return dataflows

    def __get_dataflows_component_ids(self, resource_id):
        node_ids = None
        if resource_id in self.id_map:
            node_ids = self.id_map[resource_id]
        return [node_ids] if isinstance(node_ids, str) else node_ids

    def __determine_hub_mapping_type(self, source_mapper, destination_mapper):
        # (usage of _key is deprecated)
        # SG mapping type 2
        if "$hub" in source_mapper.mapping and "$hub" in destination_mapper.mapping:
            return "type2-hub-"

        # SG mappings: type 1
        elif "$hub" not in source_mapper.mapping and "$hub" in destination_mapper.mapping \
                and any(key in source_mapper.mapping.get("$path", "") for key in ("_key", "resource_id")):
            return "type1-hub-"

        # SG mapping type 3 inbound
        elif "$hub" not in source_mapper.mapping \
                and any(key in destination_mapper.mapping.get("$hub", {}).get("$path", "")
                        for key in ("_key", "resource_id")):
            return "type3-hub-"

        # SG mapping type 3 outbound
        elif any(key in source_mapper.mapping.get("$hub", {}).get("$path", "")
                 for key in ("_key", "resource_id")):
            return "type3-hub-"

        else:
            return None

    class DataflowNodeMapper(TerraformBaseMapper):
        def run(self, source_model, source):
            source_resource_names = self.format_source_objects(source_model.search(self.mapping, source=source))

            if source_resource_names is not None:
                for index, resource_id in enumerate(source_resource_names):
                    if is_terraform_resource_reference(resource_id):
                        source_resource_names[index] = get_resource_id_from_resource_reference(resource_id)
                    elif self.is_terraform_variable_reference(resource_id):
                        source_resource_names[index] = self.get_terraform_variable_default_value(source_model,
                                                                                                 resource_id)
            return source_resource_names

