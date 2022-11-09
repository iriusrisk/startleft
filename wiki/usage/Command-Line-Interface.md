# Command Line Interface (CLI)

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