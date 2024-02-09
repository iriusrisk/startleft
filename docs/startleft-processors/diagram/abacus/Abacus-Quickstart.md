## ABACUS Integration with StartLeft for OTM Conversion

---

[ABACUS](https://www.avolutionsoftware.com/abacus/) is a robust enterprise architecture tool that supports comprehensive
modeling, analysis, and roadmapping capabilities. Integrating ABACUS models into the OTM (Open Threat Model) format
allows for enhanced threat modeling processes, benefiting from StartLeft's automation features. This integration
leverages the strengths of both platforms: ABACUS's detailed enterprise architecture insights and StartLeft's threat
modeling capabilities.

### ABACUS Models

ABACUS provides a wide range of predefined shapes and components designed for detailed architectural designs. With
StartLeft, these components can be accurately mapped into an OTM format, facilitating a seamless transition from
architectural plans to threat models. This process notably benefits from ABACUS's structured modeling approach,
translating complex architectures into comprehensive threat models with ease.

## The `slp_abacus` Module

---
The `slp_abacus` module is a dedicated component within StartLeft, tasked with converting ABACUS files into the OTM
format. Like its Drawio counterpart, this module simplifies the transition from architectural diagrams to actionable
threat models, enhancing security planning processes.

### Mapping Introduction

Similar to the Drawio process, the conversion from ABACUS to OTM includes a hierarchical approach to processing mapping
files:

* **Default mapping file**: Contains universal mappings applicable across various projects. This file is crucial for
  standardized components present in ABACUS models, facilitating their reuse in OTM conversion.
* **Custom mapping file**: Allows for the inclusion of project-specific components outlined within the ABACUS diagrams.
  Custom mappings ensure a personalized and accurate conversion to the OTM format, accounting for unique architectural
  elements.

For detailed guidance on leveraging StartLeft for ABACUS files, refer to
the [REST API Manual](../../../usage/REST-API.md).

## Accepted Formats

---
StartLeft processes ABACUS diagrams in the following formats:

- **_`*.json`_** - The JSON file exported from the ABACUS tool.

## A Basic Example

---
Consider an enterprise architecture diagram created in ABACUS that includes components such as a PoC Integrator,
Webpage, Database, Static Content, Backend, and an Angular Client.

You aim to transition this detailed architecture into a threat model using IriusRisk, necessitating the conversion of
the ABACUS diagram into the OTM format.

For this purpose, you prepare a **default mapping file** encompassing mappings for varied components highlighted in the
ABACUS model:

```yaml
trustzones:
  - label: Public Cloud
    type: b61d6911-338d-46a8-9f39-8dcd24abfe91
    default: true

components:
  - label: SST PoC Integrator
    type: CD-MSG-BROKER
  - label: SST PoC Webpage
    type: compact-server-side-web-application
  - label: SST PoC Database
    type: other-database
  - label: SST PoC Static Content
    type: CD-CONTENT-DELIVERY-NETWORK
  - label: SST PoC Backend
    type: back-end-server
  - label: Angular v12.0.0
    type: web-client
  - label: SST PoC Webpage
    type: compact-server-side-web-application

```

The result of sending to StartLeft this diagram with this default mapping file would be an OTM with all the components
we
had in the original Drawio source:
<details>
  <summary>basic-abacus-example.otm</summary>

```json
{
  "otmVersion": "0.2.0",
  "project": {
    "name": "Abacus Basic Example",
    "id": "abacus-basic-example"
  },
  "representations": [
    {
      "name": "example-project Diagram Representation",
      "id": "example-project-diagram",
      "type": "diagram",
      "size": {
        "width": 1000,
        "height": 1000
      }
    }
  ],
  "trustZones": [
    {
      "id": "0dc3a5c4-64af-490d-b72a-a591dc79a9d3",
      "name": "Public Cloud",
      "type": "b61d6911-338d-46a8-9f39-8dcd24abfe91",
      "risk": {
        "trustRating": 10
      }
    }
  ],
  "components": [
    {
      "id": "258636",
      "name": "SST PoC Webpage",
      "type": "compact-server-side-web-application",
      "parent": {
        "trustZone": "0dc3a5c4-64af-490d-b72a-a591dc79a9d3"
      }
    },
    {
      "id": "258642",
      "name": "SST PoC Integrator",
      "type": "CD-MSG-BROKER",
      "parent": {
        "trustZone": "0dc3a5c4-64af-490d-b72a-a591dc79a9d3"
      }
    },
    {
      "id": "258646",
      "name": "SST PoC Backend",
      "type": "back-end-server",
      "parent": {
        "trustZone": "0dc3a5c4-64af-490d-b72a-a591dc79a9d3"
      }
    },
    {
      "id": "258650",
      "name": "SST PoC Database",
      "type": "other-database",
      "parent": {
        "trustZone": "0dc3a5c4-64af-490d-b72a-a591dc79a9d3"
      }
    },
    {
      "id": "258665",
      "name": "SST PoC Static Content",
      "type": "CD-CONTENT-DELIVERY-NETWORK",
      "parent": {
        "trustZone": "0dc3a5c4-64af-490d-b72a-a591dc79a9d3"
      }
    },
    {
      "id": "259247",
      "name": "SST PoC Webpage",
      "type": "compact-server-side-web-application",
      "parent": {
        "trustZone": "0dc3a5c4-64af-490d-b72a-a591dc79a9d3"
      }
    },
    {
      "id": "259258",
      "name": "SST PoC Webpage",
      "type": "compact-server-side-web-application",
      "parent": {
        "trustZone": "0dc3a5c4-64af-490d-b72a-a591dc79a9d3"
      }
    },
    {
      "id": "258632",
      "name": "Angular v12.0.0",
      "type": "web-client",
      "parent": {
        "trustZone": "0dc3a5c4-64af-490d-b72a-a591dc79a9d3"
      }
    }
  ],
  "dataflows": []
}
```

</details>



First of all, retrieve all the necessary files:

* Download the `abacus_merged.json`
  from [here](https://github.com/iriusrisk/startleft/blob/main/examples/abacus/abacus_merged.json).
* Save the example Abacus file above with the name `abacus_merged.json`.

* Download the `iriusrisk-abacus-mapping.yaml`
  from [here](https://github.com/iriusrisk/startleft/blob/main/examples/abacus/iriusrisk-abacus-mapping.yaml).
* Save the default mapping above with the name `iriusrisk-abacus-mapping.yaml`.

You can get the same result if through the StartLeft's REST API. For that, in first place we need to set up the
server with the command:

```shell
startleft server
```

If you want to run the server in a specific port, you can do:

```shell
startleft server -p 8080
```

Then, execute the following command to retrieve the OTM file:

```shell
curl --location --request POST localhost:5000/api/v1/startleft/diagram \
--header "Content-Type: multipart/form-data" \
--header "Accept: application/json" \
--form diag_type="ABACUS" \
--form diag_file=@"./abacus_merged.json" \
--form default_mapping_file=@"./iriusrisk-abacus-mapping.yaml" \
--form id="abacus-basic-example" \
--form name="Abacus Basic Example"
```