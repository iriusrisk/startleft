# How to Create a Terraform mapping

---

A source mapping file (or 'mapping files' for short) describes how to find and map components, dataflows, and TrustZones in 
source file data structures.

This mapping file is divided into three sections which correspond to the main sections in an OTM file:

* trustzones
* components
* dataflows

To define the mapping behavior, a Domain-specific language has been created to abstract the internal data structure used by `slp_tf`,
providing a set of `$functions` containing the logic around a collection of JMESPath queries that are used.

Take a look at the
<a href="https://github.com/iriusrisk/startleft/blob/main/startleft/resources/schemas/iac_mapping_schema.json" target="_blank">JSONSchema</a>
file and the 
<a href="https://github.com/iriusrisk/OpenThreatModel" target="_blank">Open Threat Model</a> specification
for more details.

## How-to create a Basic Mapping File

---
This section is a Getting Started Guide for a basic mapping file configuration for terraform.

For a more in-deep explanation, there is available a [How Terraform Mapping File works](Terraform-how-mapping-file-works.md) page
and a complete guide about [Terraform Domain-specific language](Terraform-domain-specific-language.md).

#### Minimal mapping file configuration
Here appears a minimal mapping configuration example along with its explanation.
> :material-information-outline: Some mapping configuration is performed out-of-the box, 
> take a look to [How Terraform Mapping File works](Terraform-how-mapping-file-works.md) to more details

```yaml
trustzones: # (1)!
  - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91 # (2)!
    name: Public Cloud # (3)!
    $default: true # (4)!
    
  - id:   f0ba7722-39b6-4c81-8290-a30a248bb8d9
    name: Internet
    $source: {$singleton: # (5)!
                {$type: "aws_security_group", # (6)!
                 $props: "egress[0].cidr_blocks"} # (7)!
    }

components: # (8)!
  - type:        ec2 # (9)!
    $source: # (10)! 
      {$type: "aws_instance"} # (11)! 

  - type:        generic-client
    $source:     {$type: "aws_security_group",  # (12)!
                  $props: "egress[0].cidr_blocks"} 
    parent:      f0ba7722-39b6-4c81-8290-a30a248bb8d9 # (13)!
    tags: # (14)!
      - Outbound connection destination IP

dataflows: [] # (15)!
```

1. **trustzones section** here is defined as the TrustZone mapping behavior. At least one TrustZone is needed to be defined
2. set **trustzone[id]** value, which also can be used as a reference when setting the parent of a component `parent: public-cloud-01`
3. set **trustzone[name]** value
4. *Optional:* **default trustzone** to be used if a component does not define its parent
5. All the matching resources will be **unified** under a single TrustZone which will be created in case the `{$type: "aws_security_group", $props: "egress[0].cidr_blocks"}` query returns any element
6. **mapping functions** `$type` performs a search along the entire resource list to return the element with the matching type
7. **mapping functions** `$props` performs a search along the entire resource list to return the element with the matching props
8. **components section** here are defined the components mapping behavior
9. set **component[type]** value
10. **special mapping fields** `$source` set the selected resources as the object to be mapped
11. **mapping functions** `$type` performs a search along the entire resource list to return the element with the matching type
12. **mapping functions** performs a query combining `$type` and `$props` functions returning a list of $source to be mapped into a component for each existing Terraform resource that match those conditions 
13. *Optional:* set **component[parent]** as the *Internet TrustZone*
14. *Optional:* set **component[tag]** value
15. **dataflows section** is explained in details on [How Dataflow Mapping works](Terraform-how-dataflow-mapping-works.md)

##### Special mapping fields
These functions begin with a dollar sign ($) and do not directly contribute to the OTM output. 
Instead, they specify an action or behavior used to process the source files or generate the OTM output.

| $functions | Description                             | Applies to                         |
|------------|-----------------------------------------|------------------------------------|
| $default   | Specifies the TrustZone as default      | TrustZones                         |
| $source    | Specifies the source of the object type | Components, TrustZones & Dataflows |

> Here you can find the complete list of [special mapping fields](Terraform-domain-specific-language.md). 

##### Mapping functions
These functions are used as parameters of the mapping attributes for configuring its behavior. 

| $functions | Type   | Description                                                          | Consumes                 | Produces                                        |
|------------|--------|----------------------------------------------------------------------|--------------------------|-------------------------------------------------|
| $type      | filter | Finds a resource by its type                                         | The entire resource list | A resources list filtered by type               |
| $props     | filter | Finds a resource by its properties                                   | The entire resource list | A resources list filtered by the given props    |
| $singleton | group  | Specific objects to be unified under a single component or TrustZone | A given resources list   | A list of resources grouped by the given params |

> Here you can find the complete list of [Mapping functions](Terraform-domain-specific-language.md).


