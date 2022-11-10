# Command Line Interface (CLI)

---

## Commands Help

---
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
Usage: startleft parse [OPTIONS] SOURCE_FILE_1 SOURCE_FILE_2 ... SOURCE_FILE_N

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

## Validating a hand-crafted OTM

---

Validation is a CLI specific feature and the OTM validation is an special feature of StartLeft, because it does not 
have to do with any format, but it allows the users to validate OTM files generated in any way, even like in that 
case, manually.  

For example, the following short OTM file:

```yaml
otmVersion: 0.1.0

project:
  name: Manual ThreatModel
  id:   manual-threatmodel

trustZones:
  - id:   f0ba7722-39b6-4c81-8290-a30a248bb8d9
    name: Internet
    risk:
      trustRating: 1

  - id:   6376d53e-6461-412b-8e04-7b3fe2b397de
    name: Public
    risk:
      trustRating: 1

  - id:   2ab4effa-40b7-4cd2-ba81-8247d29a6f2d
    name: Private Secured
    risk:
      trustRating: 100

components:
  - id:     user
    name:   User
    type:   generic-client
    parent:
      trustZone: f0ba7722-39b6-4c81-8290-a30a248bb8d9

  - id:     web-server
    name:   Web server
    type:   web-application-server-side
    parent:
      trustZone: 6376d53e-6461-412b-8e04-7b3fe2b397de

  - id:     database
    name:   Database
    type:   postgresql
    parent:
      trustZone: 2ab4effa-40b7-4cd2-ba81-8247d29a6f2d

dataflows:
  - id:     client-connection
    name:   Client connection
    source:   user
    destination:   web-server

  - id:     database-connection
    name:   Database connection
    source:   web-server
    destination:     database
```

Can create this threat model in IriusRisk:

<p align="center"><img src="https://user-images.githubusercontent.com/78788891/154970903-61442af4-6792-4cd1-8dad-70fb347f5f4d.png"></p>

That remains in the following threats:
<p align="center"><img src="https://user-images.githubusercontent.com/78788891/154971033-5480f0b7-0d2f-4f53-83ef-b29c569fec86.png"></p>
