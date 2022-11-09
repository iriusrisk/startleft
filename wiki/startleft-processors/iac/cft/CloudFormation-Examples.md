# CloudFormation Template examples

---

You can find some sample source files inside the `examples` directory:

* `examples/cloudformation` contains CloudFormation Template example files to convert into OTM format.
* `examples/cloudformation/split` contains a complete CloudFormation Template example file split into two different files.

To process this examples, it is mandatory to use the mapping files according to the file data type. 
You can find some sample mapping files inside the `examples` directory:
* `examples/cloudformation` contains mappings for Cloudformation files.
* `examples/terraform` contains mappings for Terraform files.
* `examples/visio` contains mappings for Visio files.

## CloudFormation
CloudFormation is the AWS tool which lets you model, provision, and manage AWS and third-party resources by treating 
infrastructure as code. Startleft's repository contains an example CloudFormation mapping file that enables you to 
generate threat models based on the OTM standard from both a single or multiple CloudFormation template files using 
a single command.

The following examples, which are located in the `examples/cloudformation` and `examples/cloudformation/split` 
directories, show you how to carry out the different stages of the process separately or in a single step.

### Security Groups on multinetwork with Load Balancer
This is a rich example when you can see in action some the capabilities of startleft. It represents the threat model for
an architecture with two trust zones and several _Virtual Private Networks_ which contain elements such as:
* [Elastic Load Balancer](https://aws.amazon.com/elasticloadbalancing/).
* [Elastic Container Service](https://aws.amazon.com/ecs/).
* [CloudWatch Canary](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Create.html).
* [VPC Endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html)
* [Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html#VPCSecurityGroups) mapped as dataflows.

The following command will parse the CloudFormation source file `multinetwork_security_groups_with_lb.json` creating a 
OTM file `multinetwork_security_groups_with_lb.otm` in the process.
```shell
startleft parse \
	--iac-type CLOUDFORMATION \
	--mapping-file iriusrisk-cft-mapping.yaml \
	--output-file multinetwork_security_groups_with_lb.otm \
	--project-name "CFT MN Security Groups with LB" \
	--project-id "cft-mn-sg-lb" \
	multinetwork_security_groups_with_lb.json
```

### Other examples
There are inside the startleft repositories some other CloudFormation files with different architectures that allows you 
to experiment with different mappings and options. For them, the same commands described before can be applied.
* `elb-no-waf`. This is the simplest example, including only a public cloud as a `TrustZone` with an AWS Elastic Load 
Balancer as a single component.
* `elb-with-waf`. Slight evolution of `elb-no-waf` by including another component, a Web Application Firewall, within 
the same `TrustZone` public cloud.  

### Split examples
In the `examples/cloudformation/split` directory we have split the `multinetwork_security_groups_with_lb.json` into two 
files which are `networks_cft_file.json` and `resources_cft_file.json`.
The following command will parse both CloudFormation source files creating a OTM file 
`multinetwork_security_groups_with_lb_from_multiple_files.otm` in the process.
```shell
startleft parse \
	--iac-type CLOUDFORMATION \
	--mapping-file iriusrisk-cft-mapping.yaml \
	--output-file multinetwork_security_groups_with_lb_from_multiple_files.otm \
	--project-name "CFT MN Security Groups with LB from multiple files" \
	--project-id "cft-mn-sg-lb-ml-fl" \
	networks_cft_file.json \
	resources_cft_file.json
```

