## Command-Line
For help, just run `startleft` without arguments:

```
$ startleft
Usage: startleft [OPTIONS] COMMAND [ARGS]...

  Parse IaC files to the Open Threat Model format and upload them to IriusRisk

Options:
  -l, --log-level TEXT      Set the log level. Must be one of: crit, error,
                            warn, info, debug, none.
  --verbose / --no-verbose  Makes logging more verbose.
  --version                 Show the version and exit.
  --help                    Show this message and exit.

Commands:
  parse        Parses IaC files to the Open Threat Model format
  run          Parses IaC files to the Open Threat Model format and...
  search       Searches source files for the given query
  server       Launches the REST server to generate OTMs from requests
  threatmodel  Uploads an OTM file to IriusRisk
  validate     Validates a mapping or OTM file
```

You can also get help for the specific commands.

```
$ startleft run --help
Usage: startleft run [OPTIONS] [FILENAME]...

  Parses IaC files to the Open Threat Model and upload them to 
  IriusRisk

Options:
  -t, --type  [JSON|YAML|CloudFormation|HCL2|Terraform]
                                  Specify the source file type.
  -m, --map TEXT                  Map file to use when parsing source files
  -o, --otm TEXT                  OTM output file name
  -n, --name TEXT                 Project name
  --id TEXT                       Project ID
  --recreate / --no-recreate      Delete and recreate the product each time
  --irius-server TEXT             IriusRisk server to connect to
                                  (proto://server[:port])'
  --api-token  TEXT               IriusRisk API token
  --help                          Show this message and exit.
```

## API server

StartLeft can also be deployed as a standalone REST server if you prefer the communication via API.
In this operation mode, startleft gives back the OTM file in the HTTP response. 
If you want to use the server option on the application:

```
$ startleft server --help
Usage: startleft server [OPTIONS]...

  Launches the REST server to generate OTMs from requests

Options:
  --port INTEGER                  The port to deploy this application to
  --help                          Show this message and exit.

```

By executing `startleft server` it is possible to see the command-line messages finishing with the following:

```Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)```

so indicating Startleft's REST API is ready. You can see the endpoints provided by opening the following URL in a web browser: http://127.0.0.1:5000/docs

Available endpoints:
```
GET /health
```
```
POST /api/v1/startleft/cloudformation
Request Body:
    cft_file:                   Required. File that contains the CloudFormation Template
    id                          Required. ID of the new project
    name                        Required. Name of the new project
    mapping_file                Optional. File that contains the mapping between AWS components and IriusRisk components. Providing this file will completely override default values
```
