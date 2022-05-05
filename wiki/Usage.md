## Command-Line
For help, just run `startleft` without arguments:

```
$ startleft
Usage: startleft [OPTIONS] COMMAND [ARGS]...

  Parse IaC and other files to the Open Threat Model format and upload them to
  IriusRisk

Options:
  -l, --log-level [CRIT|ERROR|WARN|INFO|DEBUG|NONE]
                                  Set the log level.
  -v, --verbose / -nv, --no-verbose
                                  Makes logging more verbose.
  --version                       Show the version and exit.
  --help                          Show this message and exit.

Commands:
  parse        Parses IaC source files into Open Threat Model
  search       Searches source files for the given query
  server       Launches the REST server to generate OTMs from requests
  validate     Validates a mapping or OTM file
```

You can also get help for the specific commands.

```
$ startleft run --help
Usage: startleft run [OPTIONS] IAC_FILE...

  Parses an IaC file into an Open Threat Model (OTM) and uploads it to
  IriusRisk

Options:
  -t, --iac-type [CLOUDFORMATION|TERRAFORM]
                                  The IaC file type.  [required]
  -m, --mapping-file TEXT         Mapping file to parse the IaC file.
  -o, --output-file TEXT          OTM output file.
  -n, --project-name TEXT         Project name.  [required]
  -i, --project-id TEXT           Project id.  [required]
  -r, --recreate / -nr, --no-recreate
                                  Delete and create a new project/Update the
                                  project on IriusRisk.
  -s, --irius-server TEXT         IriusRisk server.
  -a, --api-token TEXT            IriusRisk API token.
  --help                          Show this message and exit.
```

## API server

StartLeft can also be deployed as a standalone REST server if you prefer the communication via API.
In this operation mode, Startleft gives back the OTM file in the HTTP response. 
If you want to use the server option on the application:

```
$ startleft server --help
Usage: startleft server [OPTIONS]...

  Launches the REST server to generate OTMs from requests

Options:
  -p, --port INTEGER  Startleft deployment port.
  --help              Show this message and exit.
```

By executing `startleft server` it is possible to see the command-line messages finishing with the following:

```Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)```

so indicating Startleft's REST API is ready. You can see the endpoints provided by opening the following URL in a web browser: http://127.0.0.1:5000/docs

Available endpoints:
```
GET /health
```
```
POST /api/v1/startleft/iac
Request Body:
    iac_file:                   Required. File that contains the IaC definition
    iac_type:                   Required. Type of the IaC File: CLOUDFORMATION
    id                          Required. ID of the new project
    name                        Required. Name of the new project
    mapping_file                Required. File that contains the mapping between IaC resources and threat model resources.
```
