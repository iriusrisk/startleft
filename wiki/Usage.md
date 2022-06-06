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
Usage: startleft parse [OPTIONS] SOURCE_FILE...

  Parses source files into Open Threat Model

Options:
  -t, --iac-type [CLOUDFORMATION|TERRAFORM]
                                  The IaC file type. NOTE: This argument is
                                  mutually exclusive with  arguments:
                                  [diagram_type, custom_mapping_file,
                                  default_mapping_file]. [required]
  -g, --diagram-type [VISIO]      The diagram file type. NOTE: This argument
                                  is mutually exclusive with  arguments:
                                  [mapping_file, iac_type]. [required]
  -m, --mapping-file TEXT         Mapping file to parse the IaC file. NOTE:
                                  This argument is mutually exclusive with
                                  arguments: [diagram_type,
                                  custom_mapping_file, default_mapping_file].
                                  [required]
  -d, --default-mapping-file TEXT
                                  Default mapping file to parse the diagram
                                  file. NOTE: This argument is mutually
                                  exclusive with  arguments: [mapping_file,
                                  iac_type]. [required]
  -c, --custom-mapping-file TEXT  Custom mapping file to parse the diagram
                                  file.
  -o, --output-file TEXT          OTM output file.
  -n, --project-name TEXT         Project name.  [required]
  -i, --project-id TEXT           Project id.  [required]
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
    custom_mapping_file         Required. File that contains the custom user mapping file between the diagram resources and threat model resources
```
> See Visio usage on [diagrams/visio/Visio.md](diagrams/visio/Visio.md) 
