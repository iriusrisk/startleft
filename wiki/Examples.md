You can find some example source files inside the `examples` directory:

* `examples/cloudformation` contains CloudFormation Template example files to convert into OTM format.

* `examples/manual` contains the OTM example file detailed in [Hand Crafted OTM](#hand-crafted-OTM).

* `examples/terraform` contains a Terraform example file to convert into OTM format. 

## Cloudformation

### ELB without a WAF

The following command will parse the cloudformation source file `elb-no-waf.json` creating a OTM file `elb-no-waf.otm` in the process.

```
startleft parse --type cloudformation --otm elb-no-waf.otm --name "CFT ELB No Waf" --id "cft-elb-no-waf" elb-no-waf.json
```
It is also possible to include your own mapping file or files, thus overriding the default internal cloudformation mapper file:
```
startleft parse --type cloudformation --map cloudformation_mapping_file_1.yaml --map cloudformation_mapping_file_2.yaml --otm elb-no-waf.otm --name "CFT ELB No Waf" --id "cft-elb-no-waf" elb-no-waf.json
```
The next command takes the OTM file and generates an IriusRisk threat model which is uploaded to the server.
```
startleft threatmodel --recreate elb-no-waf.otm
```

For convenience, `parse` and `threatmodel` can be `run` in one go:
```
startleft run --type cloudformation --otm elb-no-waf.otm --name "CFT ELB No Waf" --id "cft-elb-no-waf" --recreate elb-no-waf.json
```
Of course, it is also possible to parse by using custom mapping files with `run`:
```
startleft run --type cloudformation --map defaults_map.yaml --map cloudformation_map.yaml --otm elb-no-waf.otm --name "CFT ELB No Waf" --id "cft-elb-no-waf" --recreate elb-no-waf.json
```
Note: with `threatmodel` or `run` commands it is mandatory to include the IriusRisk API token and IriusRisk URL via environment variables or as command-line arguments, as shown in [Command Line Client](#command-line-client). 
### ELB with a WAF

This example can be run in the same way, but this Cloudformation also includes a WAF.

Parsing the Cloudformation template file:

```
startleft parse --type cloudformation --otm elb-with-waf.otm --name "CFT ELB With Waf" --id "cft-elb-with-waf" elb-with-waf.json
```

Uploading OTM file to IriusRisk:

```
startleft threatmodel --recreate elb-with-waf.otm
```

Or both commands in one step:

```
startleft run --type cloudformation --otm elb-with-waf.otm --name "CFT ELB With Waf" --id "cft-elb-with-waf" --recreate elb-with-waf.json
```

### Security Groups Example

An example that includes AWS Load Balancer, Service, Canary and VPCEndpoint components with their Security Groups.
```
startleft run --type cloudformation --otm security-groups.otm --name "Security Groups Example" --id "security-groups-example" --recreate cloudformation_for_security_group_tests.json
```



## Terraform HCL2

StartLeft can also parse Terraform source files and an example is provided in the `examples` directory.

```
startleft run --type hcl2 --otm elb.otm --name "Terraform ELB" --id "terraform-elb" --recreate elb.tf
```

## Hand crafted OTM

You can also write an OTM file without parsing any IaC source files. This is useful if you want to create a threat model in your IDE and have the diagram etc. generated for you. For example, the following short OTM file:

```
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

Will create this threat model in IriusRisk:

![manual_threat_model](https://user-images.githubusercontent.com/78788891/154970903-61442af4-6792-4cd1-8dad-70fb347f5f4d.png)

![manual_threats](https://user-images.githubusercontent.com/78788891/154971033-5480f0b7-0d2f-4f53-83ef-b29c569fec86.png)

The example is provided and can be run using this command:

```
startleft threatmodel --recreate manual.otm
```

