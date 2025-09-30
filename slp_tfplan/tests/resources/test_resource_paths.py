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
tfplan_aws_complete = path + '/tfplan/aws-complete-tfplan.json'
tfgraph_aws_complete = path + '/tfplan/aws-complete-tfgraph.json'

# resources tfplan
ingress_cidr_from_property = path + '/tfplan/resources/ingress-cidr-from-property-tfplan-resources.json'
ingress_multiple_cidr_from_property = path + \
                                      '/tfplan/resources/ingress-multiple-cidr-from-property-tfplan-resources.json'
ingress_multiple_cidr_from_rule = path + '/tfplan/resources/ingress-multiple-cidr-from-rule-tfplan-resources.json'
ingress_multiple_security_groups = path + '/tfplan/resources/ingress-multiple-security-groups-tfplan-resources.json'
aws_ingesting_click_logs = path + '/tfplan/resources/aws-ingesting-click-logs-using-terraform.gv'


# mapping
terraform_iriusrisk_tfplan_aws_mapping = path + '/mapping/iriusrisk-tfplan-aws-mapping.yaml'
terraform_singleton_mapping = path + '/mapping/singleton-mapping.yaml'
terraform_group_by_category_mapping = path + '/mapping/singleton-group-by-category-mapping.yaml'
terraform_plan_default_mapping = path + '/mapping/default-terraform-plan-mapping.yaml'

# otm
otm_expected_elb = f'{path}/otm/expected-elb.otm'
otm_expected_sgs = f'{path}/otm/expected-sgs.otm'
otm_expected_official = f'{path}/otm/expected-official.otm'
