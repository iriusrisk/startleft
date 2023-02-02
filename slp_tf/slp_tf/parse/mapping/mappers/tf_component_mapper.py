import re
import uuid

from slp_tf.slp_tf.parse.mapping.mappers.tf_base_mapper import TerraformBaseMapper, is_terraform_resource_reference, \
    get_resource_id_from_resource_reference


def get_children(mapping):
    children = mapping.get("$source", {}).get("$children", None)
    if not children:
        children = mapping.get("$children", None)

    return children


class TerraformComponentMapper(TerraformBaseMapper):

    def __init__(self, mapping, default_trustzone, id_map):
        super(TerraformComponentMapper, self).__init__(mapping)
        # Set the "b61d6911-338d-46a8-9f39-8dcd24abfe91" if default_trustzone none exist in mapping file
        # for giving compatibility with the verbose IR mapping file
        self.default_trustzone = default_trustzone or "b61d6911-338d-46a8-9f39-8dcd24abfe91"
        self.id_map = id_map

    def run(self, source_model, id_parents):
        """
        Iterates through the source model and returns the parameters to create the components
        :param source_model:
        :param id_parents:
        :return:
        """
        components = []

        source_objects = self.format_source_objects(source_model.search(self.mapping["$source"], source=None))
        mapping_name, mapping_tags = self.get_mappings_for_name_and_tags(self.mapping)
        component_type = self.mapping["type"]

        for source_object in source_objects:
            source_object['type'] = component_type
            component_resource_id = self._get_component_resource_id(source_model, source_object)
            component_name, singleton_multiple_name = self.__get_component_names(source_model, source_object,
                                                                                 mapping_name)
            parent_resource_ids, parents_from_component = \
                self.__get_parent_resource_ids(source_model, source_object, id_parents, component_resource_id)
            component_tags, singleton_multiple_tags = self.__get_component_tags(source_model, source_object,
                                                                                mapping_tags)

            for parent_resource_number, parent_resource_id in enumerate(parent_resource_ids):
                # If there is more than one parent (i.e. subnets), the component will replicated inside each
                parent_component_ids = self.__get_parent_component_ids(parent_resource_id)
                for parent_number, parent_component_id in enumerate(parent_component_ids):
                    base_component = {"name": component_name, "type": component_type, "source": source_object,
                                      "parent": parent_component_id}

                    if "properties" in self.mapping:
                        base_component["properties"] = self.mapping["properties"]
                    base_component = self.set_optional_parameters_to_resource(base_component, mapping_tags,
                                                                              component_tags, singleton_multiple_name,
                                                                              singleton_multiple_tags)

                    # Special case related with support components for Security Groups
                    if self.repeated_type4_hub_definition_component(source_model, self.mapping, component_resource_id):
                        continue

                    component_ids = self.__generate_id(
                        source_model, {**source_object, **base_component}, parent_resource_number)

                    if isinstance(component_ids, str):
                        component_ids = [component_ids]

                    for component_number, component_id in enumerate(component_ids):
                        component = base_component.copy()
                        component["id"] = component_id

                        # If the component is defining child components the ID must be saved in a parent dict
                        if get_children(self.mapping):
                            self.__add_child_to_parent_list(source_model, source_object, component_id, id_parents)
                        elif "$skip" not in self.mapping["$source"] and "$parent" in self.mapping["parent"]:
                            # $parent and $children are related mappings
                            # In this case, component_id may be a list with a different treatment
                            if parent_number != component_number:
                                continue
                        # For the rest of cases that are not $children, id_parents must be set with new parents found
                        else:
                            if component_id not in id_parents:
                                id_parents[component_id] = parent_component_id

                        self.logger.debug(
                            f"Found component: [{component['id']}][{component['type']}] | Parent: [{component['parent']}]")
                        components.append(component)

        # Here we should already have all the components

        if "$altsource" in self.mapping and components == []:
            components.extend(self.__get_alt_source_components(source_model))

        return components

    def __add_child_to_parent_list(self, source_model, source_object, parent_id, id_parents):
        self.logger.debug("Component is defining child components...")
        child_id = str(uuid.uuid4())
        child_resource_id = source_model.search(get_children(self.mapping), source=source_object)

        if is_terraform_resource_reference(child_resource_id):
            child_resource_id = get_resource_id_from_resource_reference(child_resource_id)

        self.__add_child_to_childs_map(child_id, child_resource_id)

        if child_id not in id_parents:
            id_parents[child_id] = list()
        id_parents[child_id].append(parent_id)

    def __add_child_to_childs_map(self, child_id, child_resource_id):
        if child_resource_id not in self.id_map:
            # This child has not been mapped yet but its ID must be created
            # Because the own child mapping definition has no information about its own parent
            self.id_map[child_resource_id] = child_id
        elif isinstance(self.id_map[child_resource_id], str):
            # Every generated child is unique
            # And has 1:1 correspondence with its parent
            # But self.id_map is a dict that groups by name
            # And the same parent and children may be in different subnets
            # So for this $children case:
            #  self.id_map[parent_name] = [parent_1_id, parent_2_id...parent_N_id]
            #  self.id_map[child_name] = [child_parent_1_id, child_parent_2_id...child_parent_N_id]
            self.id_map[child_resource_id] = [self.id_map[child_resource_id], child_id]
        elif isinstance(self.id_map[child_resource_id], list):
            self.id_map[child_resource_id].append(child_id)

    def __default_alt_source_mapping_lookups_template(self):
        return {
            "type": self.mapping["type"],
            "name": f'{self.mapping["type"]} from altsource',
            "tags": [{
                "$numberOfSources":
                    {"oneSource": {"$path": "resource_type"},
                     "multipleSource": {"$format": "{resource_name} ({resource_type})"}}
            }]
        }

    def __get_alt_source_components(self, source_model) -> []:
        self.logger.debug("No components found. Trying to find components from alternative source")
        alt_source = self.mapping["$altsource"]

        alt_source_components = []
        for alt in alt_source:
            mapping_type = alt["$mappingType"]
            mapping_path = alt["$mappingPath"]
            mapping_lookups = alt["$mappingLookups"]
            alt_source_objects = self.format_source_objects(source_model.search(mapping_type, source=None))

            for alt_source_object in alt_source_objects:
                value = self.get_altsource_mapping_path_value(source_model, alt_source_object, mapping_path)

                for mapping_lookup in mapping_lookups:
                    mapping_lookup = {**self.__default_alt_source_mapping_lookups_template(), **mapping_lookup}
                    result = re.match(mapping_lookup["regex"], value)

                    if result is not None:
                        if self.default_trustzone not in self.id_map:
                            self.id_map[self.default_trustzone] = str(uuid.uuid4())

                        mapping_name, mapping_tags = self.get_mappings_for_name_and_tags(mapping_lookup)
                        component_name, singleton_multiple_name = self.__get_component_names(source_model,
                                                                                             alt_source_object,
                                                                                             mapping_name)
                        component_tags, singleton_multiple_tags = self.__get_component_tags(source_model,
                                                                                            alt_source_object,
                                                                                            mapping_tags)
                        alt_source_object['altsource'] = True

                        component = {"id": str(uuid.uuid4()), "name": component_name,
                                     "type": mapping_lookup["type"], "parent": self.id_map[self.default_trustzone],
                                     "source": alt_source_object}

                        component = self.set_optional_parameters_to_resource(component, mapping_tags,
                                                                             component_tags,
                                                                             singleton_multiple_name,
                                                                             singleton_multiple_tags)

                        alt_source_components.append(component)

            return alt_source_components

    def __get_component_names(self, source_model, source_object, mapping):
        singleton_multiple_name = None
        if self.__multiple_sources_mapping_inside(mapping):
            component_name, singleton_multiple_name = self.__get_component_singleton_names(source_model, source_object,
                                                                                           mapping)
        else:
            component_name = self.__get_component_individual_name(source_model, source_object, mapping)
        return component_name, singleton_multiple_name

    def __get_component_individual_name(self, source_model, source_object, mapping):
        source_component_name = None

        if "name" in self.mapping:
            source_component_name = self.get_first_element_from_list(source_model.search(mapping, source=source_object))
            if self.is_terraform_variable_reference(source_component_name):
                source_component_name = self.format_terraform_variable(
                    source_model, source_object, source_component_name)
            elif is_terraform_resource_reference(source_component_name):
                source_component_name = get_resource_id_from_resource_reference(source_component_name)

        if source_component_name:
            self.logger.debug(f"Found source object with name {source_component_name}")
        else:
            self.logger.error(f"Found source object with name None")

        return source_component_name

    def get_first_element_from_list(self, values):
        return values[0] if isinstance(values, list) else values

    def __get_component_singleton_names(self, source_model, source_object, mapping):
        source_component_name = None

        source_component_multiple_name = None
        if "name" in self.mapping:
            source_component_name, source_component_multiple_name = source_model.search(mapping, source=source_object)
            if self.is_terraform_variable_reference(source_component_name):
                source_component_name = self.format_terraform_variable(source_model, source_object,
                                                                       source_component_name)
            elif is_terraform_resource_reference(source_component_name):
                source_component_name = get_resource_id_from_resource_reference(source_component_name)

        if source_component_name:
            self.logger.debug(f"Found singleton source object with multiple name {source_component_name}")
        else:
            self.logger.error(f"Found singleton source object with name None")

        return source_component_name, source_component_multiple_name

    def __get_component_tags(self, source_model, source_object, mapping):
        component_tags = None
        singleton_multiple_tags = None

        if mapping is not None:
            if self.__multiple_sources_mapping_inside(mapping):
                component_tags, singleton_multiple_tags = self.__get_component_singleton_tags(source_model,
                                                                                              source_object, mapping)
            else:
                component_tags = self.get_tags(source_model, source_object, mapping)
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
        return len(list(filter(lambda obj: "$numberOfSources" in obj, mapping_definition))) > 0

    def __get_parent_resource_ids(self, source_model, source_object, id_parents, component_resource_id):
        # Retrieves a list of parent resource names (components or trustZones) of the element.
        parents_from_component = False
        if "parent" in self.mapping:
            if "$parent" in self.mapping["parent"]:
                # Special case with $parent, where the parent component is in charge of defining which components
                # are their children, so its ID should be stored before reaching the child components
                # With $parent, it will check if the supposed id_parents exist,
                # otherwise performing a standard search using action inside $parent
                if len(id_parents) > 0 and component_resource_id in self.id_map:
                    component_id = self.id_map[component_resource_id]
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
                parent = [self.default_trustzone]
            for index, resource_id in enumerate(parent):
                if is_terraform_resource_reference(resource_id):
                    parent[index] = get_resource_id_from_resource_reference(resource_id)
        if isinstance(parent, str):
            if parent == "":
                parent = [self.default_trustzone]
            else:
                parent = [get_resource_id_from_resource_reference(parent)
                          if is_terraform_resource_reference(parent) else parent]

        if parent is None:
            parent = [self.default_trustzone]

        return parent, parents_from_component

    def __get_parent_component_ids(self, parent_resource_id):
        self.logger.debug("Trying to get parent ID from existing component...")
        parent_component_id = None
        if parent_resource_id in self.id_map:
            parent_component_id = self.id_map[parent_resource_id]
            self.logger.debug(f"Parent ID detected: [{parent_component_id}][{parent_resource_id}]")
        else:
            self.logger.debug("ID not found. Trying to get parent ID from parent substring...")
            for key in self.id_map:
                if key in parent_resource_id:
                    parent_component_id = self.id_map[key]
                    self.logger.debug(f"Parent ID detected: [{parent_component_id}][{key}]")
                    break

        if not parent_component_id:
            self.logger.debug("No ID found. Creating new parent ID...")
            parent_component_id = str(uuid.uuid4())
            self.id_map[parent_resource_id] = parent_component_id

        return [parent_component_id] if isinstance(parent_component_id, str) \
            else parent_component_id

    def __generate_id(self, source_model, component, parent_number):
        c_resource_id = self._get_component_resource_id(source_model, component)

        # make a previous lookup on the list of parent mappings
        c_id = None
        if c_resource_id is not None and len(self.id_map) > 0:
            if c_resource_id in self.id_map.keys():
                c_id = self.id_map[c_resource_id]
        # a new ID can be generated if there is more a parent and this is not the first one
        if c_id is None or parent_number > 0:
            c_id = str(uuid.uuid4())
        if parent_number > 0:
            if isinstance(self.id_map[c_resource_id], list):
                self.id_map[c_resource_id].append(c_id)
            if isinstance(self.id_map[c_resource_id], str):
                self.id_map[c_resource_id] = [self.id_map[c_resource_id], c_id]
        else:
            self.id_map[c_resource_id] = c_id

        return c_id

    def _get_component_resource_id(self, source_model, component):
        resource_id = source_model.search(self.mapping["id"], source=component)
        component_resource_id = self.get_first_element_from_list(resource_id)
        if self.is_terraform_variable_reference(component_resource_id):
            component_resource_id = self.get_terraform_variable_default_value(source_model, component_resource_id)
        return component_resource_id
