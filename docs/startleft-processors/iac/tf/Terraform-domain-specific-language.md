---
search:
  boost: 2 
---

---

There is an available Terraform Domain-Specific Language for easy mapping behavior configuration.
This Terraform-DSL can split into two sections: Special Mapping Fields and Mapping functions.

## SPECIAL MAPPING FIELDS
These functions begin with a dollar sign ($) and do not directly contribute to the OTM output. 
Instead, they specify an action or behavior used to process the source files or generate the OTM output.

| $functions   | Description                                                      | Applies to                         |
|--------------|------------------------------------------------------------------|------------------------------------|
| *$*default   | Specifies the TrustZone as default                               | TrustZones                         |
| *$*source    | Specifies the source of the object type                          | Components, TrustZones & Dataflows |
| *$*altsource | Specifies an alternative mapping when $source returns no object. | Components                         |
| *$*children  | Specifies whose components are their children                    | Components                         |


### *$*default
This **special mapping field** *default* specifies a TrustZone as the default trustzone for the components in case
those components don't define their parent.

**Applies to:** TrustZones

> :octicons-light-bulb-16: The components[].parent value is assigned by the attribute $default on the trustZones section.

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:        empty-component
        $source:     {$type:  "aws_internet_gateway"}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_internet_gateway" "InterneteGateway" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_internet_gateway-internetegateway
        name: InterneteGateway
        type: empty-component
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_internet_gateway
    dataflows: []
    ```

### *$*source
This **special mapping field** *source* specifies the origin of the object type to be mapped, its behavior is configured
by the Terraform-DSL mapping functions to go through all the Terraform Resource files for returning the matching elements.

**Applies to:** Components, TrustZones & Dataflows

> :octicons-light-bulb-16: This map specifies the source for the empty-component with the resources of type aws_internet_gateway

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:        empty-component
        $source:     {$type:  "aws_internet_gateway"}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_internet_gateway" "InterneteGateway" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_internet_gateway-internetegateway
        name: InterneteGateway
        type: empty-component
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_internet_gateway
    dataflows: []
    ```

### *$*altsource
This **special mapping field** *altsource* specifies an alternative mapping when $source returns nothing.

**Applies to:** Components

Reference to [Mapping an AltSource](Terraform-how-mapping-file-works.md#mapping-an-altsource) for deeper explanation

### *$*children
This **special mapping field** *children* specifies whose components are their children on the OTM, 
it will set the parent attribute of those components on the OTM.

**Applies to:** Components

Reference to [Mapping a Children](Terraform-how-mapping-file-works.md#mapping-a-children) for deeper explanation

## MAPPING FUNCTIONS

These functions are used as parameters of the mapping attributes for configuring its behavior. 

| $functions         | Type      | Description                                                                                                                                                                                                                                                                                    |
|--------------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *$*type            | filter    | Finds a resource by its type                                                                                                                                                                                                                                                                   |
| *$*name            | filter    | Finds a resource by its name                                                                                                                                                                                                                                                                   |
| *$*props           | filter    | Finds a resource by its properties                                                                                                                                                                                                                                                             |
| *$*regex           | filter    | Specifies a custom regex to be matched against the resource attribute                                                                                                                                                                                                                          |
| *$*root            | filter    | JMESPath search through the entire source file data structure                                                                                                                                                                                                                                  |
| *$*path            | accessor  | JMESPath search through the object identified in the $source. A default value is optional by using the $searchParams structure                                                                                                                                                                 |
| *$*findFirst       | selector  | JMESPath search through the list of objects identified in the $source and returns the first successful match. A default value is optional by using the $searchParams structure                                                                                                                 |
| *$*searchParams    | selector  | Specifies a default value for $path or $findFirst mapping functions                                                                                                                                                                                                                            |
| *$*singleton       | group     | Specific objects to be unified under a single component or TrustZone                                                                                                                                                                                                                           |
| *$*numberOfSources | selector  | When using singleton, allows you to set different values for output name or tags when the number of sources for the same mapping is single or multiple                                                                                                                                         |
| *$*format          | formatter | A named format string based on the output of other $special fields.                                                                                                                                                                                                                            |
| *$*module          | filter    | Search through the module section matching by source's attribute                                                                                                                                                                                                                               |
| *$*skip            | filter    | A sub-field of $source, specifying specific objects to skip if not explicitly defined                                                                                                                                                                                                          |
| *$*catchall        | filter    | A sub-field of $source, specifying a default search for all other objects not explicitly defined                                                                                                                                                                                               |
| *$*lookup          | selector  | Allows you to look up the output of a $special field against a key-value lookup table                                                                                                                                                                                                          |
| *$*hub             | connector | Only for dataflow's "source" and "destination" fields. Specially created for building dataflows from Security Group structures without generating components from them. Allows defining abstract contact points for larger end-to-end final dataflows                                          |
| *$*ip              | group     | When defining a component's "name" field as $ip, will generate a singleton component for representing an external IP but without limitations of singleton for this case, so the "type" for the defined mapping definition with $ip (i.e. generic-terminal) will not be catalogued as singleton |

### *$*type
This **mapping function** *type* returns resources by its `resource_type` attribute on the [Terraform Source Dictionary](Terraform-how-mapping-file-works.md#terraform-source-dictionary).
This function can be used combined with $name and $props to create a more complete query  

| Type   | Consumes            | Produces                          | Configuration params                                                                          | 
|--------|---------------------|-----------------------------------|-----------------------------------------------------------------------------------------------|
 | filter | A list of resources | A resources list filtered by type | Can be configured with a string, a list of strings or using the ***$*regex mapping function** | 
 
> :octicons-light-bulb-16: This map specifies the component rds by the resources of type in  (aws_db_instance, aws_rds_cluster)

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:       rds
        $source:    {$type: ["aws_db_instance", "aws_rds_cluster"]}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_db_instance" "mysql" {}
    resource "aws_rds_cluster" "aurora-cluster-demo" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_db_instance-mysql
        name: mysql
        type: rds
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_db_instance
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_rds_cluster-aurora_cluster_demo
        name: aurora-cluster-demo
        type: rds
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_rds_cluster
    dataflows: []
    ```

### *$*name
This **mapping function** *name* returns resources by its `resource_name` attribute on the [Terraform Source Dictionary](Terraform-how-mapping-file-works.md#terraform-source-dictionary).
This function can be used combined with $type and $props to create a more complete query  

| Type   | Consumes            | Produces                          | Configuration params                                                                          | 
|--------|---------------------|-----------------------------------|-----------------------------------------------------------------------------------------------|
 | filter | A list of resources | A resources list filtered by name | Can be configured with a string, a list of strings or using the ***$*regex mapping function** | 
 
> :octicons-light-bulb-16: This map specifies the component rds by the resources with name mysql

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:       rds
        $source:    {$name: "mysql"}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_db_instance" "mysql" {}
    resource "aws_rds_cluster" "aurora-cluster-demo" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_db_instance-mysql
        name: mysql
        type: rds
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_db_instance
    dataflows: []
    ```

### *$*props
This **mapping function** *props* returns resources by its `resource_properties` attribute on the [Terraform Source Dictionary](Terraform-how-mapping-file-works.md#terraform-source-dictionary).
This function can be used combined with $type and $name to create a more complete query  

| Type   | Consumes            | Produces                                    | Configuration params                                                                          | 
|--------|---------------------|---------------------------------------------|-----------------------------------------------------------------------------------------------|
 | filter | A list of resources | A resources list filtered by its properties | Can be configured with a string, a list of strings or using the ***$*regex mapping function** | 
 
> :octicons-light-bulb-16: This map specifies the component generic-client by the resources with type aws_security_group
> having the property egress[0].cidr_blocks present in resource_properties

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:        generic-client
        $source:     {$type: "aws_security_group", $props: "egress[0].cidr_blocks"}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_security_group" "webserver" {
      egress {
        cidr_blocks      = ["0.0.0.0/0"]
      }
    }
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_security_group-webserver
        name: webserver
        type: generic-client
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_security_group
    dataflows: []
    ```

### *$*regex
This **mapping function** *regex* allows configuring a custom regex to be matched against the resource attribute.
This function can be used as a parameter for $type, $name and $props.  

| Type   | Consumes            | Produces                                           | Configuration params | 
|--------|---------------------|----------------------------------------------------|----------------------|
 | filter | A list of resources | A resources list which attribute matches the regex | A valid regex        |

> :octicons-light-bulb-16: This map specifies the component api-gateway by the resources with type 
> matching the regex `^aws_api_gateway_\w*$`

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:        api-gateway
        $source:     {$type: {$regex: ^aws_api_gateway_\w*$}}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_api_gateway_rest_api" "rest_api" {}
    resource "aws_api_gateway_authorizer" "api_authorizer" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_api_gateway_rest_api-rest_api
        name: rest_api
        type: api-gateway
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_api_gateway_rest_api
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_api_gateway_authorizer-api_authorizer
        name: api_authorizer
        type: api-gateway
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_api_gateway_authorizer
    dataflows: []
    ```

### *$*root
This **mapping function** *root* allows to search through the entire source file data structure by using 
<a href="https://jmespath.org/" target="_blank">JMESPath</a>.

| Type   | Consumes               | Produces                                        | Configuration params | 
|--------|------------------------|-------------------------------------------------|----------------------|
 | filter | The entire source file | A resources list filtered by the JMESpath query | A JMESpath query     |

> :octicons-light-bulb-16: When using *$*root, it may be useful to use Additional JMESPath functions.
> This map specifies the component vpc by using the get JMESPath functions

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:        vpc
        $source:     {$root: "resource|get(@, 'aws_vpc')"}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_vpc" "CustomVPC" {
      cidr_block  = var.vpcCidrblock
    }
    ```
=== "OTM"

    ```yaml
    ---
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_vpc-customvpc
        name: CustomVPC
        type: vpc
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_vpc
    dataflows: []
    ```

### *$*path
This **mapping function** *path* allows getting the values from the object identified in the $source by using 
<a href="https://jmespath.org/" target="_blank">JMESPath</a>. A default value is optional by using the $searchParams structure

| Type     | Consumes           | Produces                                | Configuration params                        | 
|----------|--------------------|-----------------------------------------|---------------------------------------------|
 | accessor | The $source object | An attribute list filtered by the query | A JMESpath query or $searchParams structure |

> :octicons-light-bulb-16: This map specifies the component empty-component which name is retrieved by
> the $source attribute `resouce_properties.cidr_block`

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:        empty-component
        name:        {$path: "resource_properties.cidr_block"}
        $source:     {$type: "aws_subnet"}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_subnet" "PrivateSubnet1" {
      vpc_id     = aws_vpc.CustomVPC.id
      cidr_block = "10.0.2.0/24"
    }
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_subnet-privatesubnet1
        name: 10.0.2.0/24
        type: empty-component
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_subnet
    dataflows: []
    ```
 
### *$*findFirst
This **mapping function** *findFirst* search through the list of objects identified in the $source 
and returning the first successful match. A default value is optional by using the $searchParams structure

| Type      | Consumes           | Produces           | Configuration params                                                 | 
|-----------|--------------------|--------------------|----------------------------------------------------------------------|
 | formatter | The $source object | A string attribute | list of objects identified in the $source or $searchParams structure |

> :octicons-light-bulb-16: This map specifies a component rds whose name is configured by a list of attributes

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:        empty-component
        name:        {$findFirst: ["resource_properties.cidr_block", "resource_name"]}
        $source:     {$type: "aws_subnet"}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_subnet" "PrivateSubnet1" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_subnet-privatesubnet1
        name: PrivateSubnet1
        type: empty-component
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_subnet
    dataflows: []
    ```
 
### *$*searchParams
This **mapping function** *searchParams* specifies a default value for $path or $findFirst mapping functions.

| Type     | Consumes                          | Produces           | Configuration params                         | 
|----------|-----------------------------------|--------------------|----------------------------------------------|
 | selector | The $path or $findFirst functions | A string attribute | The searchPath or defaultValue configuration |

> :octicons-light-bulb-16: This map specifies a component rds whose tag is retrieved from `resource_properties.engine`
> with `rds` as default value.

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:       rds
        $source:    {$type: ["aws_db_instance", "aws_rds_cluster"]}
        tags:
         - {$path: {$searchParams: {
                        searchPath: "resource_properties.engine", 
                        defaultValue: "rds"}}}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_db_instance" "mysql" {
        engine               = "mysql" 
    }
    resource "aws_rds_cluster" "aurora-cluster-demo" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_db_instance-mysql
        name: mysql
        type: rds
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - mysql
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_rds_cluster-aurora_cluster_demo
        name: aurora-cluster-demo
        type: rds
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - rds
    dataflows: []
    ```

### *$*singleton
This **mapping function** *singleton* allows objects to be unified under a single component or TrustZone.
When exists multiples objects, the name and tag values change as configured on the 
[Component Template Pattern](Terraform-how-mapping-file-works.md#mapping-a-component)

| Type  | Consumes            | Produces                                        | Configuration params           | 
|-------|---------------------|-------------------------------------------------|--------------------------------|
 | group | A list of resources | A list of resources grouped by the given params | Mapping Function configuration |

> :octicons-light-bulb-16: This map specifies a unique component CD-SYSTEMS-MANAGER 
> by any number of resources whose name starts with `aws_ssm_`. 

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:        CD-SYSTEMS-MANAGER
        $source:     {$singleton: {$type: {$regex: ^aws_ssm_\w*$}}}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_ssm_parameter" "ssm_parameter" {}
    resource "aws_ssm_document" "ssm_document" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_ssm_parameter-ssm_parameter
        name: CD-SYSTEMS-MANAGER (grouped)
        type: CD-SYSTEMS-MANAGER
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - ssm_parameter (aws_ssm_parameter)
          - ssm_document (aws_ssm_document)
    dataflows: []
    ```
 
### *$*numberOfSources
This **mapping function** *numberOfSources* allows you to set different values for output name or tags 
when the number of sources for the same mapping is single or multiple.

| Type  | Consumes           | Produces           | Configuration params                                  | 
|-------|--------------------|--------------------|-------------------------------------------------------|
 | group | The $source object | A string attribute | oneSource and multipleSource configuration attributes |

```python
multipleSource if $singleton && (numberOfSources > 1) else oneSource
```

> :octicons-light-bulb-16: This map specifies a unique component CD-SYSTEMS-MANAGER 
> and set its name by `CD-SYSTEMS-MANAGER (grouped)` when found more than one resource. 

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:        CD-SYSTEMS-MANAGER
        name:        {$numberOfSources: {
                        oneSource: {$path: "resource_name"}, 
                        multipleSource: {$format: "{type} (grouped)"}}}
        $source:     {$singleton: {$type: {$regex: ^aws_ssm_\w*$}}}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_ssm_parameter" "ssm_parameter" {}
    resource "aws_ssm_document" "ssm_document" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_ssm_parameter-ssm_parameter
        name: CD-SYSTEMS-MANAGER (grouped)
        type: CD-SYSTEMS-MANAGER
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - ssm_parameter (aws_ssm_parameter)
          - ssm_document (aws_ssm_document)
    dataflows: []
    ```
 
### *$*format
This **mapping function** *format* returns a formatted version of the string, using values from $source 
and the `name` or `type` mapper attributes. These substitutions are identified by braces ('{' and '}')

| Type      | Consumes                                                   | Produces           | Configuration params               | 
|-----------|------------------------------------------------------------|--------------------|------------------------------------|
 | formatter | The $source object and `name` and `type` mapper attributes | A string attribute | The string formatter configuration |

> :octicons-light-bulb-16: This map specifies a component rds whose name is configured by a complex string

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:       rds
        name:       {$format: "{type} created by resource {resource_name} of type {resource_type}"}
        $source:    {$type: "aws_db_instance"}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_db_instance" "mysql" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_db_instance-mysql
        name: rds created by resource mysql of type aws_db_instance
        type: rds
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_db_instance
    dataflows: []
    ```
 
### *$*module
This **mapping function** *module* searches through the module section matching by source's attribute.

| Type   | Consumes          | Produces                                      | Configuration params         | 
|--------|-------------------|-----------------------------------------------|------------------------------|
 | filter | A list of modules | A modules list filtered by source's attribute | The source's attribute value |

> :octicons-light-bulb-16: This map specifies a component rds by the module `terraform-aws-modules/rds/aws`

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type: rds
        $source: {$module: "terraform-aws-modules/rds/aws"}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    module "db" {
      source  = "terraform-aws-modules/rds/aws"
    }
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.db
        name: db
        type: rds
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - terraform-aws-modules/rds/aws
    dataflows: []
    ```
 
### *$*skip
This **mapping function** *skip* specifying specific objects to skip if not explicitly defined

| Type   | Consumes            | Produces                              | Configuration params           | 
|--------|---------------------|---------------------------------------|--------------------------------|
 | filter | A list of resources | A resources list of resources to skip | Mapping Function configuration |

> :octicons-light-bulb-16: This map specifies the component rds by the resources of type in  (aws_db_instance, aws_rds_cluster)
> but skipping the resource with name `mysql-secret`

=== "Mapping file"
    ```yaml
    trustzones:
      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        $default: true
    components:
      - type:       rds
        $source:    {$type: ["aws_db_instance", "aws_rds_cluster"]}
      - type:       skip_mysql-secret
        $source:    {$skip: {$name: "mysql-secret"}}
    dataflows: []
    ```
=== "Resource File"

    ```terraform
    resource "aws_db_instance" "mysql" {}
    resource "aws_db_instance" "mysql-secret" {}
    resource "aws_rds_cluster" "aurora-cluster-demo" {}
    ```
=== "OTM"

    ```yaml
    otmVersion: 0.1.0
    project:
      name: name
      id: id
    representations:
      - name: Terraform
        id: Terraform
        type: code
    trustZones:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91
        name: Public Cloud
        risk:
          trustRating: 10
    components:
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_db_instance-mysql
        name: mysql
        type: rds
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_db_instance
      - id: b61d6911-338d-46a8-9f39-8dcd24abfe91.aws_rds_cluster-aurora_cluster_demo
        name: aurora-cluster-demo
        type: rds
        parent:
          trustZone: b61d6911-338d-46a8-9f39-8dcd24abfe91
        tags:
          - aws_rds_cluster
    dataflows: []
    ```
 
### *$*catchall

This **mapping function** *catchall* specifying a default search for all other objects not explicitly defined

> A section explaining how to use *$*catchall will be available soon.

[//]: # (| Type   | Consumes            | Produces                              | Configuration params           | )

[//]: # (|--------|---------------------|---------------------------------------|--------------------------------|)

[//]: # ( | filter | A list of resources | A resources list of resources to skip | Mapping Function configuration |)

[//]: # ()
[//]: # ()
[//]: # (> :octicons-light-bulb-16: This map specifies the component rds by the resources of type in  &#40;aws_db_instance, aws_rds_cluster&#41;)

[//]: # (> but skipping the resource with name `mysql-secret`)


[//]: # (=== "Mapping file")

[//]: # ()
[//]: # (    ```yaml)

[//]: # (    trustzones:)

[//]: # (      - id:   b61d6911-338d-46a8-9f39-8dcd24abfe91)

[//]: # (        name: Public Cloud)

[//]: # (        $default: true)

[//]: # (    components:)

[//]: # (      - type:       rds)

[//]: # (        $source:    {$type: ["aws_db_instance"]})

[//]: # (      - type:       empty-component)

[//]: # (        $source:    {$catchall: {$root: "resource|squash_terraform&#40;@&#41;"}})

[//]: # (    dataflows: [])

[//]: # (    ```)

[//]: # (=== "Resource File")

[//]: # ()
[//]: # (    ```terraform)

[//]: # (    resource "aws_db_instance" "mysql" {})

[//]: # (    resource "aws_rds_cluster" "aurora-cluster-demo" {})

[//]: # (    ```)

[//]: # ()
[//]: # (=== "OTM")

[//]: # ()
[//]: # (    ```yaml)

[//]: # (    ```)

### *$*lookup
This **mapping function** *lookup* allows you to look up the output of a $special field against a key-value lookup table.


??? tip "Example for lookup"

    Just in case there are some inconsistencies in naming conventions used, and you need to be able to translate one name into another, a simple lookup key-value table section can be added to the mapping file.
    For example, if we have a situation where a subnet name is written using a short naming convention, but is actually referred to via a longer name elsewhere, we can use the $lookup action.
    
    ```yaml
    parent:
      $lookup: {$path: "Properties.Subnets[]|map(&values(@), @)[]|map(&re_sub('[:]', '-', @), @)"}
    ```
    
    If the above query returns a subnet called `shortnameA`, then it will be looked up in the below table:
    
    ```yaml
    lookup:
      shortnameA: amuchlongernameA
      shortnameB: amuchlongernameB
    ```
    
    To give a final value of `amuchlongernameA`.

### *$*hub
This **special mapping field** *hub* allows defining abstract contact points for larger end-to-end final dataflows.
Only for dataflow's "source" and "destination" fields. Specially created for building dataflows from 
Security Group structures without generating components from them.

> A section explaining how to use *$*hub will be available soon.

### *$*ip
When defining a component's "name" field as $ip, will generate a singleton component for representing an external 
IP but without limitations of singleton for this case, so the "type" for the defined mapping definition with $ip 
(i.e. generic-terminal) will not be catalogued as singleton

> A section explaining how to use *$*ip will be available soon.