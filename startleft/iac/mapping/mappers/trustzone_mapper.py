from startleft.iac.mapping.mappers.base_mapper import BaseMapper


class TrustzoneMapper(BaseMapper):
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

            self.logger.debug(f"Found trustzone: [{trustzone['id']}][{trustzone['name']}]")
            trustzones.append(trustzone)

        return trustzones
