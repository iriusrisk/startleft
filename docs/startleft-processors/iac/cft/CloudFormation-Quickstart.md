# CloudFormation Quickstart
## What is CloudFormation?

---
From the [official AWS CloudFormation page](https://aws.amazon.com/cloudformation/): 
> AWS CloudFormation is a service that gives developers and businesses an easy way to create a collection of related AWS 
and third-party resources, and provision and manage them in an orderly and predictable fashion.

From the StartLeft's perspective, a CloudFormation Template (CFT) is a file that defines a set of components with 
relationships among them which can be interpreted to create a threat model. 

## The `slp_cft` module

---
The `slp_cft` module is the StartLeft Processor responsible for converting CFT files into OTM. Its operation is based 
on a mapping file that enables the users to define the translations between the source AWS types and the expected 
output in the OTM file. 

Once you got familiarized with the basics explained on this page, you will need to know more about how to use and 
customize the behavior of the processor in order to configure your own conversions. For that, you should take a look 
at the [CloudFormation mapping page](CloudFormation-Mapping.md), where you will find all the information you need, from 
basic to advanced, to build your own CFT mapping files.

Apart from this, you may also find interesting the generic usage manuals for the [CLI](../../../usage/Command-Line-Interface.md) 
and [REST API](../../../usage/REST-API.md).

## A basic example

---

Let's suppose you have a CFT file with a single
[AWS::EC2:Instance](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html)
like this:

![img/ec2-cft.png](img/ec2-cft.png)

Whose source code is:

```json
{
    "AWSTemplateFormatVersion": "2010-09-09",
    "Metadata": {
        "AWS::CloudFormation::Designer": {
            "a7e8649b-4100-4217-8aff-3342e0afa392": {
                "size": {
                    "width": 60,
                    "height": 60
                },
                "position": {
                    "x": 120,
                    "y": 450
                },
                "z": 0,
                "embeds": []
            }
        }
    },
    "Resources": {
        "MyEC2Instance": {
            "Type": "AWS::EC2::Instance",
            "Properties": {},
            "Metadata": {
                "AWS::CloudFormation::Designer": {
                    "id": "a7e8649b-4100-4217-8aff-3342e0afa392"
                }
            }
        }
    }
}
```

And you want to translate it to OTM in order to import it into [IriusRisk](https://www.iriusrisk.com/), whose 
equivalent type for an EC2 instance is an `ec2` component and the expected resultant project should be like this:

![img/ec2-iriusrisk.png](img/ec2-iriusrisk.png)

In that case, you will need a mapping file which contains, at least, a TrustZone and the mapping for the EC2 
component. Notice that the standard requires that all the components must have a parent, in this case, the _Public 
Cloud_ TrustZone. This mapping file could be as simple as this:
```yaml
trustzones:
  - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
    name: Public Cloud
    type: b61d6911-338d-46a8-9f39-8dcd24abfe91

components:
  - id:     {$format: "{name}"}
    type:   ec2
    name:   {$path: "_key"}
    $source: {$root: "Resources|squash(@)[?Type=='AWS::EC2::Instance']"}
    parent: b61d6911-338d-46a8-9f39-8dcd24abfe91
    tags:
      - { $path: "Type" }

dataflows: []
```

The combination of this CFT and mapping file will result in the OTM file below, that contains the mapped TrustZone 
and component along with all the necessary metadata defined by the standard and that is ready to be imported into a 
threat modeling tool like IriusRisk.

```json
{
    "otmVersion": "0.1.0",
    "project": {
        "name": "My EC2 project",
        "id": "my-ec2-project"
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
            "type": "b61d6911-338d-46a8-9f39-8dcd24abfe91",
            "risk": {
                "trustRating": 10
            }
        }
    ],
    "components": [
        {
            "id": "b61d6911-338d-46a8-9f39-8dcd24abfe91.myec2instance",
            "name": "MyEC2Instance",
            "type": "ec2",
            "parent": {
                "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
            },
            "tags": [
                "AWS::EC2::Instance"
            ]
        }
    ],
    "dataflows": []
}
```


### CLI
> **Note**: Before continuing, make sure you have 
> [StartLeft properly installed](../../../Quickstart-Guide-for-Beginners.md) on your machine.

Save the files above in your file system with these names:

* `ec2-cft.json` for the CloudFormation Template file.
* `ec2-mapping.yaml` for the mapping file.

Now we are going to execute StartLeft for these files so that an `ec2.otm` file will be generated in our working 
directory with identical contents to the one above.
```shell
startleft parse \
	--iac-type CLOUDFORMATION \
	--mapping-file ec2-mapping.yaml \
	--output-file ec2.otm \
	--project-id "my-ec2-project" \
	--project-name "My EC2 project" \
	ec2-cft.json
```

### cURL
You can get the same result through the StartLeft's REST API. For that, in the first place we need to set up the 
server with the command:
```shell
startleft server
```

If you want to run the server in a specific port, you can do:
```shell
startleft server -p 8080
```


Then, execute the following command to retrieve the OTM file with your EC2 component:
```shell
curl --location --request POST 'localhost:5000/api/v1/startleft/iac' \
--header 'Content-Type: multipart/form-data' \
--header 'Accept: application/json' \
--form 'iac_type="CLOUDFORMATION"' \
--form 'iac_file=@"./ec2-cft.json"' \
--form 'mapping_file=@"./ec2-mapping.yaml"' \
--form 'id="my-ec2-project"' \
--form 'name="My EC2 project"'
```

## More examples

---
The infrastructure built with CloudFormation Templates may be as complex as you want. This is the reason because 
StartLeft, through the mapping files, is intended to be configurable, so you can extend or modify its behavior and/or 
create your own mappings on demand.

To help you to walk through more complex situations with larger CFT and mapping files, we have created a page with 
[explained CFT examples](CloudFormation-Examples.md) which may be useful for you as a base for building your own mapping 
files.