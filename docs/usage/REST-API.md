# REST API

## Usage
StartLeft can also be deployed as a standalone REST server if you prefer to communicate via API.
In this operation mode, StartLeft returns the OTM file in the HTTP response.
If you want to launch the application as a server:

```shell
$ startleft server --help
Usage: startleft server [OPTIONS]...

  Launches the REST server to generate OTMs from requests

Options:
  -p, --port INTEGER  StartLeft deployment port.
  --help              Show this message and exit.
```
If not specified, port 5000 will be used by default.

You can see and try the endpoints provided by opening the following URL in a web browser:
[http://localhost:5000/docs](http://localhost:5000/docs)

!!! note
    When executing `startleft server` the following command-line message indicates that StartLeft's REST API is ready:
    
    ```Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)```

### Additional options
You can also set general StartLeft options when using the API mode. More information on the [Command Line Interface](./Command-Line-Interface.md) page 
or with the command `startleft --help server`.

For example, to launch the server with a log level of DEBUG for testing purposes you can use the following command:

`startleft --log-level DEBUG server`

## Endpoints
This section describes all the available endpoints, their parameters, and example requests and responses. Refer to each 
specific format section for example files to use.

### Health
```
GET /health
```
This endpoint can be used to check the status of the application and its [version](../Versioning.md).

??? example "Example"
    === "Request"
        ``` shell
        curl localhost:5000/health
        ```
    === "Response"
        ``` json
        {
            "status": "OK",
            "version": "1.10.0",
            "components": {
                "StartLeft": "OK"
            }
        }
        ```

### IaC
```
POST /api/v1/startleft/iac
Request Body:
    iac_file:                   Required. File that contains the IaC definition. If you want to add more than one IaC file, you need to duplicate this tag as many times as files you want to upload.
    iac_type:                   Required. Type of the IaC file: [CLOUDFORMATION, TERRAFORM]
    id                          Required. ID of the new project
    name                        Required. Name of the new project
    mapping_file                Required. File that contains the mapping between IaC resources and threat model resources.
```
This endpoint accepts one or more IaC source files (currently [Cloudformation](../startleft-processors/iac/cft/CloudFormation-Quickstart.md) 
or [Terraform](../startleft-processors/iac/tf/Terraform-Quickstart.md)) and a mapping file, and generates an OTM with 
the resulting threat modeling content.

??? example "Example"
    === "Request"
        ``` shell
        curl --location \
        --request POST localhost:5000/api/v1/startleft/iac \
        --header "Content-Type: multipart/form-data" \
        --header "Accept: application/json" \
        --form iac_type="CLOUDFORMATION" \
        --form iac_file=@"./cft-1.json" \
        --form iac_file=@"./cft-2.json" \
        --form mapping_file=@"./cft-mapping.yaml" \
        --form id="cft-to-otm-example" \
        --form name="CFT to OTM example"
        ```
    === "Response (reduced for simplicity)"
        ``` json
        {
            "otmVersion": "0.1.0",
            "project": {
                "name": "CFT to OTM example",
                "id": "cft-to-otm-example"
            },
            "representations": [
                {
                    "name": "CloudFormation",
                    "id": "CloudFormation",
                    "type": "code"
                }
            ],
            "trustZones": [...],
            "components": [...],
            "dataflows": [...]
        }
        ```

### Diagram
```
POST /api/v1/startleft/diagram
Request Body:
    diag_file:                  Required. File that contains the diagram
    diag_type:                  Required. Type of the diagram file: VISIO
    id                          Required. ID of the new project
    name                        Required. Name of the new project
    default_mapping_file        Required. File that contains the default mapping file between the diagram resources and threat model resources
    custom_mapping_file         Optional. File that contains the custom user mapping file between the diagram resources and threat model resources
```
This endpoint accepts one diagram source file (currently only in [Visio](../startleft-processors/diagram/Visio-Quickstart.md) 
format), a mapping file, and an optional custom mapping file, and generates an OTM with the resulting threat modeling content.

??? example "Example"
    === "Request"
        ``` shell
        curl --location \
        --request POST localhost:5000/api/v1/startleft/diagram \
        --header "Content-Type: multipart/form-data" \
        --header "Accept: application/json" \
        --form diag_type="VISIO" \
        --form diag_file=@"./diagram.vsdx" \
        --form default_mapping_file=@"./base-visio-mappings.yaml" \
        --form custom_mapping_file=@"./additional-visio-mappings.yaml" \
        --form id="vsdx-to-otm-example" \
        --form name="VSDX to OTM example"
        ```
    === "Response (reduced for simplicity)"
        ``` json
        {
            "otmVersion": "0.1.0",
            "project": {
                "name": "VSDX to OTM example",
                "id": "vsdx-to-otm-example"
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
            "trustZones": [...],
            "components": [...],
            "dataflows": [...]
        }
        ```

### External threat model
```
POST /api/v1/startleft/external-threat-model
Request Body:
    source_file:                Required. File that contains the threat model
    source_type:                Required. Type of the threat model file: MTMT
    id                          Required. ID of the new project
    name                        Required. Name of the new project
    default_mapping_file        Required. File that contains the default mapping file between the source threat model resources and the resulting threat model resources
```
This endpoint accepts one threat modeling source file (currently only 
[Microsoft Threat Modeling Tool](../startleft-processors/external-threat-model/mtmt/MTMT-Quickstart.md)) and a mapping 
file, and generates an OTM with the resulting threat modeling content.

??? example "Example"
    === "Request"
        ``` shell
        curl --location \
        --request POST localhost:5000/api/v1/startleft/external-threat-model \
        --header "Content-Type: multipart/form-data" \
        --header "Accept: application/json" \
        --form source_type="MTMT" \
        --form source_file=@"./source.tm7" \
        --form default_mapping_file=@"./mtmt-mappings.yaml" \
        --form id="tm7-to-otm-example" \
        --form name="TM7 to OTM example"
        ```
    === "Response (reduced for simplicity)"
        ``` json
        {
            "otmVersion": "0.1.0",
            "project": {
            "name": "TM7 to OTM example",
            "id": "tm7-to-otm-example"
            },
            "representations": [
            {
                    "name": "Microsoft Threat Modeling Tool",
                    "id": "Microsoft Threat Modeling Tool",
                    "type": "threat-model"
                },
                {
                    "name": "tm7-to-otm-example Diagram Representation",
                    "id": "tm7-to-otm-example-diagram",
                    "type": "diagram",
                    "size": {
                        "width": 2000,
                        "height": 2000
                    }
                }
            ],
            "trustZones": [...],
            "components": [...],
            "dataflows": [...],
            "threats": [...],
            "mitigations": [...]
        }
        ```

## Error management
Refer to the [Errors Management](../development/Errors-Management.md) page to learn about the different error responses 
when StartLeft is operating in API mode.

## Uvicorn
It is also possible to launch StartLeft's server directly through <a href="https://www.uvicorn.org" target="_blank">Uvicorn</a>. 
This could be useful, for example, to deploy it in a container.

Example command:

``` shell
uvicorn startleft.startleft.api.fastapi_server:webapp --host 0.0.0.0 --port 5000 --log-level critical
```