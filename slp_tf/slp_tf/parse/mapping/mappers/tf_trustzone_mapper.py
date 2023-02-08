from slp_tf.slp_tf.parse.mapping.mappers.tf_base_mapper import TerraformBaseMapper


class TerraformTrustzoneMapper(TerraformBaseMapper):
    def run(self, source_model, _):
        trustzones = []

        if "$source" in self.mapping:
            source_objs = self.format_source_objects(source_model.search(self.mapping["$source"]))
        else:
            source_objs = [self.mapping]

        self.logger.debug("Finding trustzones")
        for source_obj in source_objs:
            trustzone = {"name": source_model.search(self.mapping["name"], source=source_obj),
                         "source": source_obj
                         }
            if "properties" in self.mapping:
                trustzone["properties"] = self.mapping["properties"]

            source_id = source_model.search(self.mapping["id"], source=trustzone)
            self.id_map[source_id] = source_id
            trustzone["id"] = source_id

            if "type" in self.mapping:
                trustzone["type"] = source_model.search(self.mapping["type"], source=source_obj)
            else:
                trustzone["type"] = trustzone["id"]

            self.logger.debug(f"Found trustzone: [{trustzone['id']}][{trustzone['name']}][{trustzone['type']}]")
            trustzones.append(trustzone)

        return trustzones
