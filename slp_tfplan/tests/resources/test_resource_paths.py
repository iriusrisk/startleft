import os

path = os.path.dirname(__file__)

# generic
invalid_yaml = path + '/generic/invalid-yaml.yaml'

# tfplan
tfplan_elb = path + '/tfplan/elb-tfplan.json'
tfplan_graph_elb = path + '/tfplan/elb-tfgraph.gv'
tfplan_sgs = path + '/tfplan/sgs-tfplan.json'
tfplan_graph_sgs = path + '/tfplan/sgs-tfgraph.gv'
tfplan_official = path + '/tfplan/official-tfplan.json'
tfplan_graph_official = path + '/tfplan/official-tfgraph.gv'

# mapping
terraform_iriusrisk_tfplan_aws_mapping = path + '/mapping/iriusrisk-tfplan-aws-mapping.yaml'

# otm
tfplan_graph_elb_expected = f'{path}/otm/expected_tfplan_tfgraph_elb.otm'
tfplan_graph_sgs_expected = f'{path}/otm/expected_tfplan_tfgraph_sgs.otm'
tfplan_graph_official_expected = f'{path}/otm/expected_tfplan_tfgraph_official.otm'

