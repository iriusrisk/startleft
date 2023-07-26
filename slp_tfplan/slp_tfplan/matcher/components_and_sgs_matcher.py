from typing import Dict, List

from dependency_injector.wiring import inject, Provide

from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.matcher.resource_matcher import ResourceMatcher, ResourcesMatcherContainer
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM, TFPlanComponent


class ComponentsAndSGsMatcher:
    """
    This class is responsible for matching components and security groups.
    """
    @inject
    def __init__(self,
                 otm: TFPlanOTM, relationships_extractor: RelationshipsExtractor,
                 components_sg_matcher: ResourceMatcher = Provide[ResourcesMatcherContainer.component_sg_matcher]):
        # Data structures
        self.otm: TFPlanOTM = otm
        self.relationships_extractor: RelationshipsExtractor = relationships_extractor

        # Injected dependencies
        self.are_component_in_sg = components_sg_matcher.are_related

    def match(self) -> Dict[str, List[TFPlanComponent]]:
        """
        Returns a list of Dict of security groups and their related components.
        :return: Dict of security groups and their related components.
        """
        components_in_sgs: Dict[str, List[TFPlanComponent]] = {}

        for security_group in self.otm.security_groups:
            components_in_sg = []
            for component in self.otm.components:
                if self.are_component_in_sg(component,
                                            security_group,
                                            relationships_extractor=self.relationships_extractor,
                                            launch_templates=self.otm.launch_templates):
                    components_in_sg.append(component)

            if components_in_sg:
                components_in_sgs[security_group.id] = components_in_sg

        return components_in_sgs
