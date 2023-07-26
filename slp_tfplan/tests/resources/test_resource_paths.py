import os

path = os.path.dirname(__file__)

# generic
invalid_yaml = path + '/generic/invalid-yaml.yaml'

# tfplan/tfgraph
tfplan_elb = path + '/tfplan/elb-tfplan.json'
tfgraph_elb = path + '/tfplan/elb-tfgraph.gv'
tfplan_sgs = path + '/tfplan/sgs-tfplan.json'
tfgraph_sgs = path + '/tfplan/sgs-tfgraph.gv'
tfplan_official = path + '/tfplan/official-tfplan.json'
tfgraph_official = path + '/tfplan/official-tfgraph.gv'

# resources tfplan
ingress_cidr_from_property = path + '/tfplan/resources/ingress-cidr-from-property-tfplan-resources.json'
ingress_multiple_cidr_from_property = path + \
                                      '/tfplan/resources/ingress-multiple-cidr-from-property-tfplan-resources.json'
ingress_multiple_cidr_from_rule = path + '/tfplan/resources/ingress-multiple-cidr-from-rule-tfplan-resources.json'
ingress_multiple_security_groups = path + '/tfplan/resources/ingress-multiple-security-groups-tfplan-resources.json'


# mapping
terraform_iriusrisk_tfplan_aws_mapping = path + '/mapping/iriusrisk-tfplan-aws-mapping.yaml'

# otm
otm_expected_elb = f'{path}/otm/expected-elb.otm'
otm_expected_sgs = f'{path}/otm/expected-sgs.otm'
otm_expected_official = f'{path}/otm/expected-official.otm'

