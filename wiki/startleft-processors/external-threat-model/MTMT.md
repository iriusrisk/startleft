# MTMT support
For MTMT we have available this endpoint
```
POST /api/v1/startleft/etm
Request Body:
    source_file:                Required. File that contains the original Threat model
    source_type:                Required. Type of Diagram File: MTMT
    id                          Required. ID of the new project
    name                        Required. Name of the new project
    default_mapping_file        Required. File that contains the default mapping file between the diagram resources and threat model resources
```

## MTMT file
The `source_file` field must contain a valid tm7 file.

Startleft supports only the `tm7` format for Microsoft Threat Modeling Tool. 


## Default mapping file
The aim of this mapping file is to map the MTMT elements from templates such as AWS Visio elements.

e.g: 
```commandline
components:
  - label:  Amazon EC2
    type:   ec2
```
We need to set on the mapping file the label of the component.

e.g: 
```commandline
components:
  - label:  My amazon ec2 component
    type:   ec2
```
