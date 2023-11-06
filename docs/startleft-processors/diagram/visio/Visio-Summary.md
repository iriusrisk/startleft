# What is Visio Summary?

---

> Visio Summary is a tool available at our Command Line Interface for retrieving useful info from VSDX files.

This tool can retrieve all the shapes' information available (type, name) 
and their candidate OTM type by emulating the parse method. 

You can find [here](../../../usage/Command-Line-Interface.md#summary) a complete explanation of this CLI function.

## Summary Options
This summary tool can be executed with multiple configurations:


### without mapping file
---
!!! note ""

    The summary retrieves all the availables shapes in the VSDX files without their candidate OTM type.

=== "CLI execution"
    ```shell
    startleft summary \
    --diagram-type VISIO \
    examples/visio/aws-with-tz-and-vpc.vsdx
    ```

### by `file path`
---
!!! note ""

    The summary is executed against a unique Visio file.

=== "CLI execution"
    ```shell
    startleft summary \
    --diagram-type VISIO \
    --default-mapping-file examples/visio/iriusrisk-visio-aws-mapping.yaml \
    examples/visio/aws-with-tz-and-vpc.vsdx
    ```

### by `multiple file path`
---
!!! note ""

    The summary is executed against multiple Visio files. 

=== "CLI execution"
    ```shell
    startleft summary \
    --diagram-type VISIO \
    --default-mapping-file examples/visio/iriusrisk-visio-aws-mapping.yaml \
    examples/visio/aws-with-tz-and-vpc.vsdx examples/visio/visio-basic-example.vsdx
    ```

### by `folder path`
---
!!! note ""

    The summary is executed against a folder path that contains `.vsdx` in it. 

=== "CLI execution"
    ```shell
    startleft summary \
    --diagram-type VISIO \
    --default-mapping-file examples/visio/iriusrisk-visio-aws-mapping.yaml \
    examples/visio/
    ```

### by `multiple folder path`
---
!!! note ""

    The summary is executed against multiple folder path that contains `.vsdx` in it. 

=== "CLI execution"
    ```shell
    startleft summary \
    --diagram-type VISIO \
    --default-mapping-file examples/visio/iriusrisk-visio-aws-mapping.yaml \
    examples/visio/folder1 examples/visio/folder2
    ```

## Summary Output Example

```
| SOURCE      | SOURCE_ELEMENT_TYPE | SOURCE_ELEMENT_NAME   | OTM_MAPPED_TYPE |
|-------------|---------------------|-----------------------|-----------------|
| file_1.vsdx |                     | Public Cloud          |                 |
| file_1.vsdx |                     | Custom VPC            |                 |
| file_1.vsdx |                     | Private Secured Cloud |                 |
| file_1.vsdx | Amazon CloudWatch   | Amazon CloudWatch     | cloudwatch      |
| file_1.vsdx | Amazon CloudWatch   | Custom log system     | cloudwatch      |
| file_1.vsdx | Amazon EC2          | Amazon EC2            | ec2             |
| file_1.vsdx | Amazon EC2          | Custom machine        | ec2             |
| file_1.vsdx | Database            | Private Database      | rds             |
| file_2.vsdx |                     | Private Secured Cloud |                 |
| file_2.vsdx |                     | Public Cloud          |                 |
| file_2.vsdx |                     | My Custom VPC         |                 |
| file_2.vsdx |                     | My Custom Machine     |                 |
| file_2.vsdx | Amazon EC2          | My EC2                | ec2             |
| file_2.vsdx | Database            | Private Database      | rds             |
```