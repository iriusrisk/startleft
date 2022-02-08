import logging, uuid

from startleft.mapper import TrustzoneMapper, ComponentMapper, DataflowMapper, create_core_dataflow

logger = logging.getLogger(__name__)

DESTINATION_NODE_NAME = "destination_node_name"
HUB_TYPE = "hub_type"
SOURCE_NODE_NAME = "source_node_name"
TYPE1 = "type1"
TYPE2 = "type2"
TYPE3 = "type3"

class Transformer:
    def __init__(self, source_model=None, threat_model=None):
        self.source_model = source_model
        self.threat_model = threat_model
        self.map = {}
        self.id_map = {}
        self.id_parents = dict()
        self.id_dataflows = dict()

    def build_lookup(self):
        if "lookup" in self.map:
            self.source_model.lookup = self.map["lookup"]

    def transform_trustzones(self):
        for mapping in self.map["trustzones"]:
            mapper = TrustzoneMapper(mapping)
            mapper.id_map = self.id_map
            source_trustzones = mapper.run(self.source_model)
            for trustzone_number, trustzone_element in enumerate(source_trustzones):
                if "$source" in mapping and isinstance(mapping["$source"], dict):
                    if "$singleton" in mapping["$source"] and trustzone_number > 0:
                        continue
                self.threat_model.add_trustzone(**trustzone_element)

    def transform_components(self):
        singleton = []
        components = []
        catchall = []
        skip = []
        for mapping in self.map["components"]:
            mapper = ComponentMapper(mapping)
            mapper.id_map = self.id_map
            for component in mapper.run(self.source_model, self.id_parents):
                if isinstance(mapping["$source"], dict):
                    if "$skip" in mapping["$source"]:
                        skip.append(component)
                        continue
                    elif "$catchall" in mapping["$source"]:
                        catchall.append(component)
                        continue
                    elif "$singleton" in mapping["$source"]:
                        singleton.append(component)
                        continue

                components.append(component)

        results = []
        for component in components:
            skip_this = False
            for skip_component in skip:
                if component["id"] == skip_component["id"]:
                    logger.debug("Skipping component '{}'".format(component["id"]))
                    skip_this = True
                    break
            if not skip_this:
                results.append(component)

        for component in catchall:
            skip_this = False
            for skip_component in skip:
                if component["id"] == skip_component["id"]:
                    logger.debug("Skipping catchall component '{}'".format(component["id"]))
                    skip_this = True
                    break
            for current_component in results:
                if component["id"] == current_component["id"]:
                    logger.debug("Catchall component already added '{}'".format(component["id"]))
                    skip_this = True
                    break
            if not skip_this:
                results.append(component)

        singleton_types_added = []
        for component in singleton:
            skip_this = False
            for skip_component in skip:
                if component["id"] == skip_component["id"]:
                    logger.debug("Skipping singleton component '{}'".format(component["id"]))
                    skip_this = True
                    break
            if not skip_this:
                if component["type"] not in singleton_types_added:
                    results.append(component)
                    singleton_types_added.append(component["type"])
                else:
                    # if the component is singleton and it already exists in otm (from a previous mapping)
                    # no new component is generated but the existing component is updated
                    # a)with the group name (even more if had a component name)
                    # b)with a new tag with data from this source component
                    for result in results:
                        if result["type"] == component["type"]:
                            if "singleton_multiple_name" in component:
                                result["name"] = component["singleton_multiple_name"]

                            # update "result" component with its multiple tags before adding tags from "component"
                            if "singleton_multiple_tags" in result:
                                if len(result["tags"]) <= len(result["singleton_multiple_tags"])\
                                        and result["tags"] is not result["singleton_multiple_tags"]:
                                    result["tags"] = result["singleton_multiple_tags"]

                            if "singleton_multiple_tags" in component:
                                for tag in component["singleton_multiple_tags"]:
                                    if tag not in result["tags"]:
                                        result["tags"].append(tag)
                            continue

        # removal of auxiliary data before adding components
        for component in results:
            if "singleton_multiple_name" in component:
                del component["singleton_multiple_name"]
            if "singleton_multiple_tags" in component:
                del component["singleton_multiple_tags"]

        for final_component in results:
            parent_component = next(filter(lambda x: x["id"] == final_component['parent'], results), None)
            if parent_component:
                final_component["parent_type"] = "component"
            else:
                final_component["parent_type"] = "trustZone"

            self.threat_model.add_component(**final_component)

    def transform_dataflows(self):
        for mapping in self.map["dataflows"]:
            mapper = DataflowMapper(mapping)
            mapper.id_map = self.id_map
            for dataflow in mapper.run(self.source_model, self.id_dataflows):
                self.threat_model.add_dataflow(**dataflow)

        self.__generate_dataflows_from_hubs()
        self.__clean_hub_dataflows()

    def run(self, iac_mapping):
        self.map = iac_mapping
        self.build_lookup()
        self.transform_trustzones()
        self.transform_components()
        self.transform_dataflows()

    def __generate_dataflows_from_hubs(self):
        for dataflow in self.threat_model.dataflows:
            if "-hub" in dataflow.source_node or "-hub" in dataflow.destination_node:
                for cursor_dataflow in self.threat_model.dataflows:

                    if self.__same_dataflows(dataflow, cursor_dataflow):
                        continue

                    if self.__case_1_dataflow(dataflow, cursor_dataflow):
                        if self.__case_1_outbound_dataflow(dataflow, cursor_dataflow):
                            self.__generate_dataflow_from_hub(dataflow, cursor_dataflow)

                        elif self.__case_1_inbound_dataflow(dataflow, cursor_dataflow):
                            self.__generate_dataflow_from_hub(cursor_dataflow, dataflow)

    def __separate_hub_type_and_hub_dataflow(self, node_id):
        hub_type = None
        if "type1-hub-" in node_id:
            hub_type = TYPE1
            node_id = node_id[10:]
        if "type2-hub-" in node_id:
            hub_type = TYPE2
            node_id = node_id[10:]
        if "type3-hub-" in node_id:
            hub_type = TYPE3
            node_id = node_id[10:]
        return hub_type, node_id

    def __generate_dataflow_from_hub(self, origin_dataflow, target_dataflow):
        df_name = origin_dataflow.name + " -> " + target_dataflow.name
        source_obj = None
        # the origin of dataflow is always the same
        source_resource_id = origin_dataflow.source_node
        # guess the end of dataflow
        origin_dataflow_hub_info = self.__get_hub_dataflow_info(origin_dataflow)
        target_dataflow_hub_info = self.__get_hub_dataflow_info(target_dataflow)

        if origin_dataflow_hub_info[DESTINATION_NODE_NAME] == target_dataflow_hub_info[DESTINATION_NODE_NAME]:
            destination_resource_id = target_dataflow.source_node
        else:
            destination_resource_id = target_dataflow.destination_node

        # cleansing of names of hub tagging
        source_hub_type, source_resource_id = self.__separate_hub_type_and_hub_dataflow(source_resource_id)
        destination_hub_type, destination_resource_id =\
            self.__separate_hub_type_and_hub_dataflow(destination_resource_id)
        # getting IDs if type is REFERENCED
        if source_hub_type is not None:
            source_resource_id = self.id_map[source_resource_id]
        if destination_hub_type is not None:
            destination_resource_id = self.id_map[destination_resource_id]

        # creates a dataflow with common fields to both
        dataflow = create_core_dataflow(df_name, source_obj, source_resource_id, destination_resource_id)
        # adds additional fields
        dataflow["id"] = str(uuid.uuid4())
        dataflow["tags"] = origin_dataflow.tags + target_dataflow.tags
        self.threat_model.add_dataflow(**dataflow)
        logger.debug(": " + df_name)

    def __same_dataflows(self, dataflow_1, dataflow_2):
        dataflow_1_hub_info = self.__get_hub_dataflow_info(dataflow_1)
        dataflow_2_hub_info = self.__get_hub_dataflow_info(dataflow_2)

        if dataflow_1_hub_info[SOURCE_NODE_NAME] == dataflow_2_hub_info[SOURCE_NODE_NAME] \
                and dataflow_1_hub_info[DESTINATION_NODE_NAME] == dataflow_2_hub_info[DESTINATION_NODE_NAME]:
            return True
        elif dataflow_1.name == dataflow_2.name and dataflow_1.source == dataflow_2.source:
            return True
        else:
            return False

    def __case_1_dataflow(self, dataflow, cursor_dataflow):
        """ Look for 1 to 1 dataflows like in VPCEndpoints - Security Group - IP
         Basic requirements for origin node: to be a real end component """
        dataflow_hub_info = self.__get_hub_dataflow_info(dataflow)
        cursor_dataflow_hub_info = self.__get_hub_dataflow_info(cursor_dataflow)
        # first condition: the component is a real end component "referencing" a hub i.e. a Security Group
        if dataflow_hub_info[HUB_TYPE] is TYPE1:
            # second condition: the cursor dataflow is an inbound/outbound, "defined" from a hub i.e. a Security Group
            if cursor_dataflow_hub_info[HUB_TYPE] is TYPE3:
                return True
            else:
                return False
        else:
            return False

    def __case_1_outbound_dataflow(self, dataflow, cursor_dataflow):
        # additional requirements for outbound dataflows
        dataflow_hub_info = self.__get_hub_dataflow_info(dataflow)
        cursor_dataflow_hub_info = self.__get_hub_dataflow_info(cursor_dataflow)

        if dataflow_hub_info[DESTINATION_NODE_NAME] == cursor_dataflow_hub_info[SOURCE_NODE_NAME]:
            return True
        else:
            return False

    def __case_1_inbound_dataflow(self, dataflow, cursor_dataflow):
        # additional requirements for inbound dataflows
        dataflow_hub_info = self.__get_hub_dataflow_info(dataflow)
        cursor_dataflow_hub_info = self.__get_hub_dataflow_info(cursor_dataflow)

        if dataflow_hub_info[DESTINATION_NODE_NAME] == cursor_dataflow_hub_info[DESTINATION_NODE_NAME]:
            return True
        else:
            return False

    def __case_2_dataflow(self, dataflow, cursor_dataflow):
        """ Look for dataflows amongst more than one Security Group: Component A - SG A - SG B - Component B
         Basic requirements for origin node: to be a real end component """
        dataflow_hub_info = self.__get_hub_dataflow_info(dataflow)
        cursor_dataflow_hub_info = self.__get_hub_dataflow_info(cursor_dataflow)

        # first condition: the component is a real end component "referencing" a hub i.e. a Security Group
        if dataflow_hub_info[HUB_TYPE] is TYPE1:
            # second condition: the cursor dataflow is an inbound/outbound, "defined" from a hub i.e. a Security Group
            if cursor_dataflow_hub_info[HUB_TYPE] is TYPE2:
                return True
            else:
                return False
        else:
            return False

    def __get_hub_dataflow_info(self, dataflow):
        dataflow_hub_type_source, dataflow_source_node_name = \
            self.__separate_hub_type_and_hub_dataflow(dataflow.source_node)
        dataflow_hub_type_destination, dataflow_destination_node_name = \
            self.__separate_hub_type_and_hub_dataflow(dataflow.destination_node)

        if dataflow_hub_type_source is not None:
            dataflow_hub_type = dataflow_hub_type_source
        else:
            dataflow_hub_type = dataflow_hub_type_destination

        hub_dataflow_info = {HUB_TYPE: dataflow_hub_type, SOURCE_NODE_NAME: dataflow_source_node_name,
                             DESTINATION_NODE_NAME: dataflow_destination_node_name}
        return hub_dataflow_info

    def __clean_hub_dataflows(self):
        # code for cleaning temporary dataflows coming from $hub action
        for dataflow in reversed(self.threat_model.dataflows):
            if "-hub" in dataflow.source_node or "-hub" in dataflow.destination_node:
                self.threat_model.dataflows.remove(dataflow)
                logger.debug("cleaning temp dataflow:"+dataflow.name)
