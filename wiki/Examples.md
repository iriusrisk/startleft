You can find some example source files inside the `examples` directory:

* `examples/cloudformation` contains CloudFormation Template example files to convert into OTM format.
* `examples/terraform` contains Terraform example files to convert into OTM format.
* `examples/manual` contains the OTM example file detailed in [Hand Crafted OTM](#hand-crafted-OTM).


## CloudFormation
CloudFormation is the AWS tool which lets you model, provision, and manage AWS and third-party resources by treating 
infrastructure as code. Startleft's repository contains a default CloudFormation mapping file that enables you to 
generate threat models based on the OTM standard from a CloudFormation template file using 
a single command.

The following examples, which are located in the `examples/cloudformation` directory, show you how to carry out the 
different stages of the process separately or in a single step. They also demonstrate how to use a custom mapping file 
in order to generate OTM resources that fulfill exactly your needs.

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
	--iac-type cloudformation \
	--output-file multinetwork_security_groups_with_lb.otm \
	--project-name "CFT MN Security Groups with LB" \
	--project-id "cft-mn-sg-lb" \
	multinetwork_security_groups_with_lb.json
```
It is also possible to include your own mapping file, thus overriding the default internal CloudFormation mapping file:
```shell
startleft parse \
	--iac-type cloudformation \
	--mapping-file my_cloudformation_mapping_file.yaml \
	--output-file multinetwork_security_groups_with_lb.otm \
	--project-name "CFT MN Security Groups with LB" \
	--project-id "cft-mn-sg-lb" \
	multinetwork_security_groups_with_lb.json
```

### Other examples
There are inside the startleft repository some other CloudFormation files with different architectures that allows you 
to experiment with different mappings and options. For them, the same commands described before can be applied.
* `elb-no-waf`. This is the simplest example, including only a public cloud as a `TrustZone` with an AWS Elastic Load 
Balancer as a single component.
* `elb-with-waf`. Slight evolution of `elb-no-waf` by including another component, a Web Application Firewall, within 
the same `TrustZone` public cloud.  

## Terraform HCL2

StartLeft supports parsing Terraform source files. An example is provided in the `examples/terraform` directory.

```shell
startleft run \
	--iac-type hcl2 \
	--output-file elb.otm \
	--project-name "Terraform ELB" \
	--project-id "terraform-elb" \
	--recreate \
	elb.tf
```

## Hand crafted OTM

You can also write an OTM file without parsing any IaC source files. This is useful if you want to create a threat model 
in your IDE and validate it before uploading it to a Threat Modeling platform like IriusRisk. For example, the following short OTM file:

```yaml
otmVersion: 0.1.0

project:
  name: Manual ThreatModel
  id:   manual-threatmodel

trustZones:
  - id:   f0ba7722-39b6-4c81-8290-a30a248bb8d9
    name: Internet
    risk:
      trustRating: 1

  - id:   6376d53e-6461-412b-8e04-7b3fe2b397de
    name: Public
    risk:
      trustRating: 1

  - id:   2ab4effa-40b7-4cd2-ba81-8247d29a6f2d
    name: Private Secured
    risk:
      trustRating: 100

components:
  - id:     user
    name:   User
    type:   generic-client
    parent:
      trustZone: f0ba7722-39b6-4c81-8290-a30a248bb8d9

  - id:     web-server
    name:   Web server
    type:   web-application-server-side
    parent:
      trustZone: 6376d53e-6461-412b-8e04-7b3fe2b397de

  - id:     database
    name:   Database
    type:   postgresql
    parent:
      trustZone: 2ab4effa-40b7-4cd2-ba81-8247d29a6f2d

dataflows:
  - id:     client-connection
    name:   Client connection
    source:   user
    destination:   web-server

  - id:     database-connection
    name:   Database connection
    source:   web-server
    destination:     database
```

Can create this threat model in IriusRisk:

![manual_threat_model](https://user-images.githubusercontent.com/78788891/154970903-61442af4-6792-4cd1-8dad-70fb347f5f4d.png)

![manual_threats](https://user-images.githubusercontent.com/78788891/154971033-5480f0b7-0d2f-4f53-83ef-b29c569fec86.png)

The otm is provided as example.
