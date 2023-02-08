# Command Line Interface (CLI)

Serverless CLI mode is the original Startleft operation mode where:

* Startleft runs as a standalone application.

* Execution is performed via CLI in local machine.

* Input files are in local machine.

* Mapping file may be Startleft default or another user-defined may be specified.

## Command Help

---
For help, just run `startleft` without arguments:

```shell
$ startleft
Usage: startleft [OPTIONS] COMMAND [ARGS]...

  Parse IaC and other files to the Open Threat Model format

Options:
  -l, --log-level [CRIT|ERROR|WARN|INFO|DEBUG|NONE]
                                  Set the log level.
  -v, --verbose / -nv, --no-verbose
                                  Makes logging more verbose.
  --version                       Show the version and exit.
  --help                          Show this message and exit.

Commands:
  parse     Parses source files into Open Threat Model
  search    Searches source files for the given query
  server    Launches the REST server to generate OTMs from requests
  validate  Validates a mapping or OTM file

```
You can also get help for specific commands.

??? example "Example for `parse` command help"
    
    ```shell
        $ startleft parse --help
        Usage: startleft parse [OPTIONS] SOURCE_FILE...
        Parses source files into Open Threat Model
        
        Options:
          -t, --iac-type [CLOUDFORMATION|TERRAFORM]
                                          The IaC file type. NOTE: This argument is
                                          mutually exclusive with  arguments:
                                          [custom_mapping_file, etm_type,
                                          diagram_type, default_mapping_file].
          -g, --diagram-type [VISIO|LUCID]      
                                          The diagram file type. NOTE: This
                                          argument is mutually exclusive with
                                          arguments: [mapping_file, iac_type].
          -e, --etm-type [MTMT]           The etm file type. NOTE: This argument is
                                          mutually exclusive with  arguments:
                                          [mapping_file, diagram_type, iac_type].
                                          [required]
          -m, --mapping-file TEXT         Mapping file to parse the IaC file. NOTE:
                                          This argument is mutually exclusive with
                                          arguments: [etm_type, default_mapping_file,
                                          diagram_type, custom_mapping_file].
                                          [required]
          -d, --default-mapping-file TEXT
                                          Default mapping file to parse the diagram
                                          file. NOTE: This argument is mutually
                                          exclusive with  arguments: [mapping_file,
                                          iac_type]. [required]
          -c, --custom-mapping-file TEXT  Custom mapping file to parse the diagram
                                          file.
          -o, --output-file TEXT          OTM output file.
          -n, --project-name TEXT         Project name.  [required]
          -i, --project-id TEXT           Project id.  [required]
          --help                          Show this message and exit.
    ```

## Command Summary

The list of commands that can be used to work in CLI mode is detailed as follows:


| Command  | Description                                              | 
|----------|----------------------------------------------------------|
| parse    | Parses source files into Open Threat Model.              |
| validate | Validates a mapping or OTM file.                         |
| search   | Searches source files for the given query.               |
| server   | Launches the REST server to generate OTMs from requests. |



### Parse

This command is used for parsing source files into the Open Threat Model format.

The options that it supports are:

```shell
  -t, --iac-type [CLOUDFORMATION|TERRAFORM]
                                  The IaC file type. NOTE: This argument
                                  is mutually exclusive with  arguments:
                                  [custom_mapping_file,
                                  default_mapping_file, diagram_type].
                                  [required]
  -g, --diagram-type [VISIO|LUCID]      
                                  The diagram file type. NOTE: This
                                  argument is mutually exclusive with
                                  arguments: [mapping_file, iac_type].
                                  [required]
  -m, --mapping-file TEXT         Mapping file to parse the IaC file.
                                  NOTE: This argument is mutually
                                  exclusive with  arguments:
                                  [custom_mapping_file,
                                  default_mapping_file, diagram_type].
                                  [required]
  -d, --default-mapping-file TEXT
                                  Default mapping file to parse the
                                  diagram file. NOTE: This argument is
                                  mutually exclusive with  arguments:
                                  [mapping_file, iac_type]. [required]
  -c, --custom-mapping-file TEXT  Custom mapping file to parse the
                                  diagram file.
  -o, --output-file TEXT          OTM output file.
  -n, --project-name TEXT         Project name.  [required]
  -i, --project-id TEXT           Project id.  [required]
  --help                          Show this message and exit.

```
> :material-information-outline: Notice that the argument with the `IaC or diagram file name` to parse is not 
> preceded by a parameter 

=== "CLI execution"
    ```shell
    startleft parse \
	--iac-type TERRAFORM \
	--mapping-file iriusrisk-tf-aws-mapping.yaml \
	--output-file multinetwork_security_groups_with_lb.otm \
	--project-name "Terraform MN Security Groups with LB" \
	--project-id "tf-mn-sg-lb" \
	multinetwork_security_groups_with_lb.tf
    ```
=== "Output"
    ```shell
    Parsing source files into OTM
    Parsing IaC source files into OTM
    Validating Terraform file
    Mapping file size is valid
    Loading schema file 'iac_tf_mapping_schema.json'
    Mapping files are valid
    Mapping files are valid
    Mapping file size is valid
    Loading mapping data
    Adding trustzones
    Added 2 trustzones successfully
    Adding components
    Added 22 components successfully
    Adding dataflows
    Added 22 dataflows successfully
    Loading schema file 'otm_schema.json'
    OTM file schema is valid
    OTM file has consistent IDs
    OTM file validated successfully
    Writing OTM file to 'multinetwork_security_groups_with_lb.otm'
    ```
=== "File"
    ```json
    {
      "otmVersion": "0.1.0",
      "project": {
        "name": "Terraform MN Security Groups with LB",
        "id": "tf-mn-sg-lb"
      },
      "representations": [
        {
          "name": "Terraform",
          "id": "Terraform",
          "type": "code"
        }
      ],
      "trustZones": [
        {
          "id": "b61d6911-338d-46a8-9f39-8dcd24abfe91",
          "name": "Public Cloud",
          "risk": {
            "trustRating": 10
          }
        },
        {
          "id": "f0ba7722-39b6-4c81-8290-a30a248bb8d9",
          "name": "Internet",
          "risk": {
            "trustRating": 10
          }
        }
      ],
      "components": [
        {
          "id": "b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_vpc-customvpc",
          "name": "CustomVPC",
          "type": "vpc",
          "parent": {
            "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
          },
          "tags": [
            "aws_vpc"
          ]
        },
        {
          "id": "b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_vpc-customvpc.aws_subnet-privatesubnet1",
          "name": "PrivateSubnet1",
          "type": "empty-component",
          "parent": {
            "component": "b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_vpc-customvpc"
          },
          "tags": [
            "aws_subnet"
          ]
        }
        [...] Reduced for simplicity
    ```
You can also parse more than one IaC file as in this other example:

=== "CLI execution"
    ```shell
    startleft parse \
    --iac-type CLOUDFORMATION \
    --project-name "cft_multiple_files_project" \
    --project-id cft_multiple_files_project_id \
    --mapping-file iriusrisk-cft-mapping.yaml \
    networks_cft_file.json \
    resources_cft_file.json
    ```
=== "Output"
    ```shell
    Parsing source files into OTM
    Parsing IaC source files into OTM
    Validating CloudFormation file
    Mapping file size is valid
    Loading schema file 'iac_cft_mapping_schema.json'
    Mapping files are valid
    Mapping files are valid
    Mapping file size is valid
    Loading mapping data
    Adding trustzones
    Added 2 trustzones successfully
    Adding components
    Added 22 components successfully
    Adding dataflows
    Added 22 dataflows successfully
    Loading schema file 'otm_schema.json'
    OTM file schema is valid
    OTM file has consistent IDs
    OTM file validated successfully
    Writing OTM file to 'threatmodel.otm'
    ```
=== "File"
    ```json
    {
      "otmVersion": "0.1.0",
      "project": {
        "name": "cft_multiple_files_project",
        "id": "cft_multiple_files_project_id"
      },
      "representations": [
        {
          "name": "CloudFormation",
          "id": "CloudFormation",
          "type": "code"
        }
      ],
      "trustZones": [
        {
          "id": "b61d6911-338d-46a8-9f39-8dcd24abfe91",
          "name": "Public Cloud",
          "risk": {
            "trustRating": 10
          }
        },
        {
          "id": "f0ba7722-39b6-4c81-8290-a30a248bb8d9",
          "name": "Internet",
          "risk": {
            "trustRating": 10
          }
        }
      ],
      "components": [
        {
          "id": "b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc",
          "name": "CustomVPC",
          "type": "vpc",
          "parent": {
            "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
          },
          "tags": [
            "AWS::EC2::VPC"
          ]
        },
        {
          "id": "b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1",
          "name": "PrivateSubnet1",
          "type": "empty-component",
          "parent": {
            "component": "b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc"
          },
          "tags": [
            "AWS::EC2::Subnet"
          ]
        },
    [...] Reduced for simplicity
    ```
There are different combinations that we can use, but we have to take into account the above required arguments. An 
example of a diagram parse is shown below.


=== "CLI execution"
    ```shell
    startleft parse \
    --diagram-type VISIO \
    --default-mapping-file iriusrisk-visio-aws-mapping.yaml \
    --output-file visio-basic-example.otm \
    --project-name "VISIO Basic Example" \
    --project-id "vs-bs-ex" \
    visio-basic-example.vsdx
    ```
=== "Output"
    ```shell
    Parsing source files into OTM
    Parsing diagram source files into OTM
    Validating visio file
    Mapping file size is valid
    Loading schema file 'diagram_mapping_schema.json'
    Mapping files are valid
    Mapping files are valid
    Mapping file size is valid
    Loading mapping data
    Loading schema file 'otm_schema.json'
    OTM file schema is valid
    OTM file has consistent IDs
    OTM file validated successfully
    Writing OTM file to 'visio-basic-example.otm'
    ```
=== "File"
    ```json
    {
      "otmVersion": "0.1.0",
      "project": {
        "name": "VISIO Basic Example",
        "id": "vs-bs-ex"
      },
      "representations": [
        {
          "name": "Visio",
          "id": "Visio",
          "type": "diagram",
          "size": {
            "width": 1000,
            "height": 1000
          }
        }
      ],
      "trustZones": [
        {
          "id": "b61d6911-338d-46a8-9f39-8dcd24abfe91",
          "name": "Public Cloud",
          "risk": {
            "trustRating": 10
          }
        },
        {
          "id": "2ab4effa-40b7-4cd2-ba81-8247d29a6f2d",
          "name": "Private Secured",
          "risk": {
            "trustRating": 10
          }
        }
      ],
      "components": [
        {
          "id": "12",
          "name": "My EC2",
          "type": "ec2",
          "parent": {
            "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
          }
        },
        {
          "id": "30",
          "name": "Private Database",
          "type": "rds",
          "parent": {
            "trustZone": "2ab4effa-40b7-4cd2-ba81-8247d29a6f2d"
          }
        }
      ],
      "dataflows": [
        {
          "id": "34",
          "name": "998dcc87-ab45-4ac5-9e6a-62d08ce73a20",
          "source": "12",
          "destination": "30"
        }
      ]
    }
    ```

#### Differences between parsing Diagram and IaC files

We have seen that there are some differences when parsing diagram and IaC files. Here we will detail what 
they are and how to proceed.

| Option                     | Description                                     | Diagram  | IaC      | Example                                  |
|----------------------------|-------------------------------------------------|----------|----------|------------------------------------------|
| None                       | The IaC / diagram file to parse.                | Required | Required | multinetwork_security_groups_with_lb.tf  |
| -t, --iac-type             | The IaC file type.                              | -        | Required | TERRAFORM                                |
| -g, --diagram-type         | The diagram file type.                          | Required | -        | VISIO                                    |
| -m, --mapping-file         | Mapping file to parse the IaC file.             | -        | Required | iriusrisk-tf-aws-mapping.yaml            |
| -d, --default-mapping-file | Default mapping file to parse the diagram file. | Required | -        | iriusrisk-visio-aws-mapping.yaml         |
| -c, --custom-mapping-file  | Custom mapping file to parse the  diagram file. | Optional | -        | custom-visio-aws-mapping.yaml            |
| -o, --output-file          | OTM output file.                                | Optional | Optional | visio-basic-example.otm                  |
| -n, --project-name         | Project name.                                   | Required | Required | "VISIO Basic Example"                    |
| -i, --project-id           | Project id.                                     | Required | Required | "vs-bs-ex"                               |

If we want to parse an `IaC` file, we should specify:

* The IaC file we want to parse.
* The IaC type.
* The mapping file we want to use to parse the IaC file.
* The project name.
* The project id.
* Optionally the name of the OTM output file.

??? success "Correct example for IaC"
    ```shell
    startleft parse \
    --iac-type TERRAFORM \
    --mapping-file iriusrisk-tf-aws-mapping.yaml \
    --output-file elb.otm \
    --project-name "Terraform ELB example" \
    --project-id "tf-elb-ex" \
    elb.tf
    ```
??? failure "Incorrect example for IaC"
    
    ```shell
    startleft parse \
    --iac-type TERRAFORM \
    --default-mapping-file iriusrisk-tf-aws-mapping.yaml \
    --project-name "Terraform ELB example" \
    --project-id "tf-elb-ex" \
    elb.tf
    ```
    The --mapping-file option is missed and the diagram --default-mapping-file option is added to parse an IaC file.

On the other hand, if we want to parse a `diagram` file, we should specify the following options:

* The diagram file we want to parse.
* The diagram's type.
* The default mapping file we want to use to parse the diagram file.
* Optionally, the custom mapping file that we have created to parse the diagram file.
* The project's name.
* The project id.
* Optionally the name of the OTM output file.

??? success "Correct example for diagram"
    ```shell
    startleft parse \
    --diagram-type VISIO \
    --default-mapping-file iriusrisk-visio-aws-mapping.yaml \
    --output-file aws-with-tz-and-vpc.otm \
    --project-name "Aws with tz and vpt" \
    --project-id "vs-aws-tz-vpc" \
    aws-with-tz-and-vpc.vsdx
    ```    

??? failure "Incorrect example for diagram"
    ```shell
    startleft parse \
    --diagram-type VISIO \
    --custom-mapping-file iriusrisk-visio-aws-mapping.yaml \
    --project-name "Aws with tz and vpt" \
    --project-id "vs-aws-tz-vpc" \
    aws-with-tz-and-vpc.vsdx
    ```
    The --default-mapping-file option is missed.

### Validate

Validation is a CLI-specific feature and is used to validate both OTM and mapping files.  

OTM validation is a special feature of StartLeft, as it does not apply to any format and instead allows users 
to validate OTM files generated in any way, including manually. 

!!! example
    The following short OTM file, can create this threat model in IriusRisk and generates 
    the following threats

    === "OTM file"
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

    === "IriusRisk Threat Model"

        <p align="center"><img src="https://user-images.githubusercontent.com/78788891/154970903-61442af4-6792-4cd1-8dad-70fb347f5f4d.png"></p>

    === "Threats"

        <p align="center"><img src="https://user-images.githubusercontent.com/78788891/154971033-5480f0b7-0d2f-4f53-83ef-b29c569fec86.png"></p>


As the mapping files are different for IaC and diagram, 
there are different options for each of them. The full set of options are:

```shell
Usage: startleft validate [OPTIONS]

  Validates a mapping or OTM file

Options:
  -i, --iac-mapping-file TEXT     IaC mapping file to validate.
  -d, --diagram-mapping-file TEXT
                                  Diagram mapping file to validate.
  -e, --etm-mapping-file TEXT     External Threat Model mapping file to
                                  validate.
  -o, --otm-file TEXT             OTM input file.
  --help                          Show this message and exit.
```
> :material-information-outline: We can use this command only to validate one file at once

=== "CLI execution"
    ```shell
    startleft validate \
    --otm-file threatmodel.otm 
    ```
=== "Output"
    ```shell
    Validating OTM file
    Loading schema file '/otm/resources/schemas/otm_schema.json'
    OTM file schema is valid
    OTM file has consistent IDs
    OTM file validated successfully
    ```
An example with a mapping file:

=== "CLI execution"
    ```shell
    startleft validate \
    --diagram-mapping-file iriusrisk-visio-aws-mapping.yaml
    ```
=== "Output"
    ```shell
    Validating Diagram mapping files
    Mapping file size is valid
    Loading schema file '/slp_visio/resources/schemas/diagram_mapping_schema.json'
    Mapping files are valid
    Mapping files are valid
    ```

### Search

This command runs a <a href="https://jmespath.org/" target="_blank">JMESPath search query</a> against 
the provided source file and outputs the matching results. It is only available for `IaC` source files 
and the full set of options are:

```shell
  -t, --iac-type [CLOUDFORMATION|TERRAFORM]
                                  The IaC file type.  [required]
  -q, --query TEXT                JMESPath query to run against the IaC file.
  --help                          Show this message and exit.
```
> :material-information-outline: Notice that the argument with the `IaC file name` is not 
> preceded by a parameter 

??? example "`Terraform` example"

    === "CLI execution"
        ```shell
        startleft search \
        --iac-type TERRAFORM \
        --query "resource|[?resource_type=='aws_vpc']" \
        multinetwork_security_groups_with_lb.tf
        ```
    === "Output"
        ```shell
        [...] Reduced for simplicity
        --- Results ---
        [
          {
            "aws_vpc": {
              "CustomVPC": {
                "cidr_block": "${var.vpcCidrblock}"
              }
            },
            "resource_type": "aws_vpc",
            "resource_name": "CustomVPC",
            "resource_properties": {
              "cidr_block": "${var.vpcCidrblock}"
            },
            "Type": "aws_vpc",
            "_key": "CustomVPC",
            "Properties": {
              "cidr_block": "${var.vpcCidrblock}"
            }
          }
        ]
        ```
    === "File"
        ```terraform
        variable "vpcCidrblock" {
          type    = list
          default = ["10.0.0.0/16"]
        }
        variable "ingressCidrblock" {
          type    = list
          default = ["0.0.0.0/0"]
        }
        
        resource "aws_vpc" "CustomVPC" {
          cidr_block  = var.vpcCidrblock
        }
        
        resource "aws_subnet" "PrivateSubnet1" {
          vpc_id     = aws_vpc.CustomVPC.id
          cidr_block = "10.0.2.0/24"
        }
        resource "aws_subnet" "PrivateSubnet2" {
          vpc_id     = aws_vpc.CustomVPC.id
          cidr_block = "10.0.3.0/24"
        }
        [...] Reduced for simplicity
        ```

??? example "`Cluodformation` example"

    === "CLI execution"
        ```shell
        startleft search \
        --iac-type CLOUDFORMATION \
        --query "Resources|squash(@)[?Type=='AWS::ElasticLoadBalancingV2::LoadBalancer']" \
        multinetwork_security_groups_with_lb.json
        ```
    === "Output"
        ```shell
        [...] Reduced for simplicity
        --- Results ---
        [
          {
            "Type": "AWS::ElasticLoadBalancingV2::LoadBalancer",
            "Properties": {
              "LoadBalancerAttributes": [
                {
                  "Key": "deletion_protection.enabled",
                  "Value": "false"
                }
              ],
              "Scheme": "internal",
              "SecurityGroups": [
                {
                  "Fn::GetAtt": [
                    "ServiceLBSecurityGroup",
                    "GroupId"
                  ]
                }
              ],
              "Subnets": [
                {
                  "Fn::ImportValue": "ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet1SubnetXYZ"
                },
                {
                  "Fn::ImportValue": "ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet2SubnetABC"
                }
              ],
              "Type": "application"
            },
            "_key": "ServiceLB"
          }
        ]

        ```
    === "File"
        ```json
        [...] Reduced for simplicity
        "ServiceLB": {
          "Type": "AWS::ElasticLoadBalancingV2::LoadBalancer",
          "Properties": {
            "LoadBalancerAttributes": [
              {
                "Key": "deletion_protection.enabled",
                "Value": "false"
              }
            ],
            "Scheme": "internal",
            "SecurityGroups": [
              {
                "Fn::GetAtt": [
                  "ServiceLBSecurityGroup",
                  "GroupId"
                ]
              }
            ],
            "Subnets": [
              {
                "Fn::ImportValue": "ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet1SubnetXYZ"
              },
              {
                "Fn::ImportValue": "ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet2SubnetABC"
              }
            ],
            "Type": "application"
          }
        },
        ```
### Server

This is the latest Startleft operation mode where it runs as a server with its own `REST API endpoints` that 
receive one or more IaC files, process them and give back the OTM file in the response. The available options are:

```shell
    -p, --port INTEGER  Startleft deployment port.
    --help              Show this message and exit.
```

=== "CLI execution"
    ```shell
    startleft server \
    --port 5000
    ```
=== "Output"
    ```shell
    INFO    cli - Startleft version: 1.10.0
    INFO    server - Started server process []
    INFO    on - Waiting for application startup.
    INFO    on - Application startup complete.
    INFO    server - Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)
    ```