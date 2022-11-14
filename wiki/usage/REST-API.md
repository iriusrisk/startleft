# REST API

StartLeft can also be deployed as a standalone REST server if you prefer the communication via API.
In this operation mode, StartLeft gives back the OTM file in the HTTP response.
If you want to use the server option on the application:

```
$ startleft server --help
Usage: startleft server [OPTIONS]...

  Launches the REST server to generate OTMs from requests

Options:
  -p, --port INTEGER  StartLeft deployment port.
  --help              Show this message and exit.
```

By executing `startleft server` it is possible to see the command-line messages finishing with the following:

```Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)```

so indicating StartLeft's REST API is ready. You can see the endpoints provided by opening the following URL in a 
web browser: http://127.0.0.1:5000/docs

Available endpoints:
```
GET /health
```
```
POST /api/v1/startleft/iac
Request Body:
    iac_file:                   Required. File that contains the IaC definition. If you want to add more than one IaC file, you need to duplicate this tag as many times as files you want to upload.
    iac_type:                   Required. Type of the IaC File: [CLOUDFORMATION, TERRAFORM]
    id                          Required. ID of the new project
    name                        Required. Name of the new project
    mapping_file                Required. File that contains the mapping between IaC resources and threat model resources.
```
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
 
