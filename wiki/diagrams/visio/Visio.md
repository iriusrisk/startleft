# Visio support
For Visio we have available this endpoint
```
POST /api/v1/startleft/diagram
Request Body:
    diag_file:                  Required. File that contains the diagram
    diag_type:                  Required. Type of the diagram File: VISIO
    id                          Required. ID of the new project
    name                        Required. Name of the new project
    default_mapping_file        Required. File that contains the default mapping file between the diagram resources and threat model resources
    custom_mapping_file         Optional. File that contains the custom user mapping file between the diagram resources and threat model resources
```

## Diagram file
The `diag_file` field must contain a valid vsdx file.

Startleft supports only the `vsdx` format for Visio. 

See [https://docs.microsoft.com/en-us/office/client-developer/visio/introduction-to-the-visio-file-formatvsdx](https://docs.microsoft.com/en-us/office/client-developer/visio/introduction-to-the-visio-file-formatvsdx)


## Default mapping file
The aim of this mapping file is to map the  Visio elements from templates such as AWS Visio elements.

e.g: 
```commandline
components:
  - label:  Amazon EC2
    type:   ec2
```

Visio has a template for AWS EC2 which its default label is ```Amazon EC2```.

We need to set on the default mapping file the label of the component: The default one ```Amazon EC2``` or our custom label if is not the default.

e.g: 
```commandline
components:
  - label:  My amazon ec2 component
    type:   ec2
```


## Custom mapping file
The aim of this mapping file is to map the Visio generic shapes from templates such circles, rectangles, etc.

Because a generic shape has no meaning from the thread modeling point of view, it's mandatory laleling them on the
custom-mapping file in order to map to OTM.

This custom file prevails over default one, meaning that if any of the mappings appears more than once,
the one from the custom mapping file will be use, instead of default mapping file one.

e.g:
```commandline
components:
  - label:  My DynamoDB in a circle
    type:   dynamodb
```

If a generic shape is not present on mapping file the shape won't be mapped.

