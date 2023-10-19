from slp_tfplan.slp_tfplan.matcher.components_and_sgs_matcher import ComponentsAndSGsMatcher
from slp_tfplan.slp_tfplan.matcher.resource_matcher import ResourcesMatcherContainer
from slp_tfplan.slp_tfplan.matcher.sg_and_sgrules_matcher import SGAndSGRulesMatcher
from slp_tfplan.slp_tfplan.matcher.sgs_matcher import SGsMatcher
from slp_tfplan.slp_tfplan.matcher.strategies.match_strategy import MatchStrategyContainer

MatchStrategyContainer().wire(packages=[__name__])

ResourcesMatcherContainer().wire(modules=[
    ComponentsAndSGsMatcher.__module__,
    SGsMatcher.__module__,
    SGAndSGRulesMatcher.__module__
])
