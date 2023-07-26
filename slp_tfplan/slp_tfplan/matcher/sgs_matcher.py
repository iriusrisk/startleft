from typing import Dict, List

from dependency_injector.wiring import inject, Provide

from slp_tfplan.slp_tfplan.graph.relationships_extractor import RelationshipsExtractor
from slp_tfplan.slp_tfplan.matcher.resource_matcher import ResourceMatcher, ResourcesMatcherContainer
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM


class SGsMatcher:
    """
    This class is responsible for matching security groups.
    """

    @inject
    def __init__(self,
                 otm: TFPlanOTM, relationships_extractor: RelationshipsExtractor,
                 sgs_matcher: ResourceMatcher = Provide[ResourcesMatcherContainer.sgs_matcher]):
        # Data structures
        self.otm: TFPlanOTM = otm
        self.relationships_extractor: RelationshipsExtractor = relationships_extractor

        # Injected dependencies
        self.are_sgs_related = sgs_matcher.are_related

    def match(self) -> Dict[str, List[str]]:
        """
        Returns a list of Dict of security groups and their related security groups.
        :return: Dict of security groups and their related security groups.
        """
        sgs_relationships: Dict[str, List[str]] = {}

        for source_sg in self.otm.security_groups:
            sg_relationships = []

            for target_sg in self.otm.security_groups:
                if source_sg.id == target_sg.id:
                    continue

                if self.are_sgs_related(source_sg, target_sg, relationships_extractor=self.relationships_extractor):
                    sg_relationships.append(target_sg.id)

            if sg_relationships:
                sgs_relationships[source_sg.id] = list(set(sg_relationships))

        return sgs_relationships
