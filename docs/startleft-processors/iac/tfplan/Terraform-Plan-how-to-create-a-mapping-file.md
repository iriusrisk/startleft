# Terraform Plan mapping


---

??? note "This mapping configuration only applies to Terraform Plan Processor."
    
    Please refer to another mapping file configuration documentation if needed. 
    You can locate each processor's documentation in the left menu under the "StartLeft Processors (SLP)" section. 

A source mapping file (or 'mapping file' for short) describes how to find and map components and 
Trust Zones in source file data structures.

This mapping file is divided into three sections:

* `trustzones`.
* `components`.
* `configuration`.

### Mapping Trust Zones

!!! note ""

    <a href="https://github.com/iriusrisk/OpenThreatModel#trustzones-object" target="_blank">Trust zones</a> 
    are the different areas within which components are located. They define how trustworthy an area is, 
    based on how accessible it is: the more accessible, the less trustworthy.

> The [OTM standard](../../../Open-Threat-Model-(OTM).md) defines that every component in the threat model must have a 
parent. 

Although this concept could be confusing as Terraform only defines Infrastructure, all the resources 
are situated inside a Public Cloud which is represented by a Trust Zone with a certain trustworthy level.

#### The Default Trust Zone
All the components existing as resources in the Terraform Plan will be associated with this Trust Zone.
This Trust Zone is marked as ```$default: True``` and its existence is mandatory

```yaml
  - type: public-cloud
    name: Public Cloud
    risk:
      trust_rating: 10
    $default: true
```

#### The Internet Trust Zone
This *Optional* Trust Zone is used to define the Internet Attack Surface, which contains all the
components outside the Public Cloud but with the ability to connect with it.

```yaml
  - type: internet
    name: Internet
    risk:
      trust_rating: 1
```

### Mapping Components
This processor can map all the resources inside the Terraform Plan file into components.
A mapping list must be defined in the `components` section to find and configure the mapping behavior.

#### Mapping by Resource Type

```yaml
  - label: aws_vpc
    type: vpc
```

!!! note ""

    This configuration sets all the resources of type `aws_vpc` to components of type `vpc`

#### Mapping by a list of Resource Types

```yaml
  - label: ["aws_lb", "aws_elb", "aws_alb"]
    type: load-balancer
```

!!! note ""

    This configuration sets all the resources of type `aws_lb` or `aws_elb` or `aws_alb` to components of type `load-balancer`

#### Mapping as a Singleton

```yaml
  - label: aws_cloudwatch_metric_alarm
    type: cloudwatch
    $singleton: true
```

!!! note ""

    This configuration maps all the available components of type `aws_cloudwatch_metric_alarm` to a 
    **unique component** of type `cloudwatch`

#### Mapping by a Regex

```yaml
  - label: {$regex: ^aws_api_gateway_\w*$}
    type: api-gateway
    $singleton: true
```

!!! note ""

    This configuration maps all the components whose type matches the regex `^aws_api_gateway\w*$`.
    It may be used along `$singleton` to create a **unique component** of type `api-gateway`

### Mapping Configuration

> All the configurations are optional.

#### Attack Surface

This configuration is used to define the Internet Attack Surface. 
It sets a `trustzone` containing the `client` which has dataflow connections with resources inside the Public Cloud.

```yaml
configuration:
  attack_surface:
    client: generic-client
    trustzone: internet
```

#### Skip

This configuration defines a list of resources that will never be mapped.

```yaml
configuration:
  skip:
    - aws_security_group
    - aws_db_subnet_group
```

#### Catch All

This configuration defines a default component to map all the resources not skipped or mapped.

```yaml
configuration:
  catch_all: empty-component
```
