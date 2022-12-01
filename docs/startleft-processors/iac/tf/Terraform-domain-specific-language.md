# Terraform Domain-Specific Language

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
| *$*children  | Specifies which components are their children                    | Components                         |


### $default
This **special mapping field** *default* specifies a TrustZone as the default trustzone for the components in case
those components don't define their own parent.

**Applies to:** TrustZones

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
    ```