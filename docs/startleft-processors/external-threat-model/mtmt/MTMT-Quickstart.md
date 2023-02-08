# MTMT Quickstart

---
## What is MTMT?

---
From the [official Microsoft Threat Model Tool page](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool):
> The Threat Modeling Tool is a core element of the Microsoft Security Development Lifecycle (SDL). 
> It allows software architects to identify and mitigate potential security issues.

From the point of view of StartLeft, a MTMT file is an external threat model (external because is not OTM) input source
which has information about:

 - The diagram: With stencils, TrustZones and dataflows, their relationships and their visual representation.
 - The threats.
 - The mitigations.

In Starleft we have available the slp_mtmt processor to import a MTM file.

## The `slp_mtmt` processor

---
The `slp_mtmt` module is the StartLeft Processor responsible for processing MTMT files into OTM. Its operation is based
on a mapping file that enables the users to define the translations between:

- The source stencils types and the OTM components output.
- The source TrustZones and the OTM TrustZones output.

Once you got familiarized with the basics explained in this page, you will need to know more about how to use the
processor in order to create the mapping file for a successful conversion from MTMT to OTM. 
For that, you should take a look to this page:

* Detailed information about how to build your own mapping files in the
  [MTMT mapping page](MTMT-Mapping.md).

## A basic example

---
This is a very basic threat model example from MTMT that you can use as source_file to test the endpoint

![](img/MTMT_example.png)

>***You can find the source 
> [MTMT_example.tm7](https://github.com/iriusrisk/startleft/tree/feature/OPT-479/examples/mtmt/MTMT_example.tm7) 
> file inside the examples directory***

## MTMT support

---
For MTMT we have available this endpoint
```
POST /api/v1/startleft/external-threat-model
Request Body:
    source_file:                Required. File that contains the original threat model
    source_type:                Required. Type of source file: MTMT
    id:                         Required. ID of the new project
    name:                       Required. Name of the new project
    default_mapping_file:       Required. File that contains the default mapping file between the diagram resources and threat model resources
```

### MTMT file
The `source_file` field must contain a valid tm7 file.

StartLeft supports only the `tm7` format for Microsoft Threat Modeling Tool. 


### Default mapping file
The aim of this mapping file is to map the MTMT elements from templates such as the Azure template.
To know how to build your own mapping-file, please read [MTMT-Mapping](MTMT-Mapping.md)

### CLI
> **Note**: Before continue, make sure you have
> [StartLeft properly installed](../../../Quickstart-Guide-for-Beginners.md) in your machine.

First of all, retrieve all the necessary files:

* Download the `MTMT_example.tm7` and `mtmt_default_mapping_example.yaml files` from [here](https://github.com/iriusrisk/startleft/blob/main/examples/mtmt).

Now we are going to execute StartLeft for these files so that a `basic-mtmt-example.otm` file will be generated in 
our working directory.

```shell
startleft parse \
	--etm-type MTMT \
	--default-mapping-file mtmt_default_mapping_example.yaml \
	--output-file basic-mtmt-example.otm \
	--project-id "my-mtmt" \
	--project-name "My MTMT Basic Example" \
	MTMT_example.tm7
```
#### cURL
For work with the API, in first place we need to have [StartLeft properly installed](../../../Quickstart-Guide-for-Beginners.md)

After that, set up the server with the command:
```shell
startleft server
```

If you want to run the server in a specific port, you can do:
```shell
startleft server -p 8080
```


Then, execute the following command to retrieve the OTM file with your MTMT file:
```shell
curl --location --request POST localhost:5000/api/v1/startleft/external-threat-model \
--header "Content-Type: multipart/form-data" \
--header "Accept: application/json" \
--form source_type="MTMT" \
--form source_file=@"./MTMT_example.tm7" \
--form default_mapping_file=@"./mtmt_default_mapping_example.yaml" \
--form id="my-mtmt-project" \
--form name="My MTMT project"
```

## Position of the elements
For details about how we map the position of the elements, please read 
[MTMT-elements-position.md](MTMT-elements-position.md). 
