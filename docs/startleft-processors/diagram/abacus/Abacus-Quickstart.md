## What is Abacus?

---
Integrating ABACUS, a premier enterprise architecture tool, with StartLeft's OTM (Open Threat Model) format enriches threat modeling with advanced automation. This synergy combines ABACUS's detailed architectural insights with StartLeft's streamlined threat modeling, offering a comprehensive security analysis framework.

### Leveraging ABACUS Models in StartLeft

ABACUS's extensive collection of predefined components and shapes enables intricate architectural designs. Through StartLeft, these elements are precisely translated into the OTM format, ensuring a smooth transition from architectural designs to detailed threat models. This integration highlights the structured modeling of ABACUS, making complex architectures easily interpretable in threat modeling contexts.

## The `slp_abacus` Module: Bridging Architectures with Threat Models

---

The `slp_abacus` module within StartLeft focuses on converting ABACUS files into OTM format, akin to its Drawio integration. This module facilitates the conversion of architectural diagrams into actionable threat models, thereby enhancing security planning.

### Hierarchical Mapping Process

The ABACUS to OTM conversion process involves a hierarchical approach to mappings, comprising:

- **Default Mapping File**: Includes generic mappings for widespread use across multiple projects, ensuring the standardization of ABACUS model components during OTM conversion.
- **Custom Mapping File**: Accommodates project-specific components from ABACUS diagrams, allowing for tailored and precise OTM translations that reflect unique architectural nuances.

Refer to the [REST API Manual](../../../usage/REST-API.md) for comprehensive instructions on utilizing StartLeft with ABACUS files.

## Supported Formats by StartLeft

---

StartLeft is capable of processing ABACUS diagrams in JSON format:

- **`*.json`**: Exports directly from ABACUS for conversion.

## Conversion Example: From ABACUS to OTM

---

Imagine converting an ABACUS diagram featuring a PoC Integrator, Webpage, Database, Static Content, Backend, and an Angular Client into a threat model. The process involves using a **default mapping file** to define mappings for these components, facilitating their translation into the OTM format:

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
```

The conversion results in an OTM file reflecting the original ABACUS diagram's components:

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

### Getting Started with Conversion

To begin the conversion process:

1. Download `abacus_merged.json` and the example default mapping file (`iriusrisk-abacus-mapping.yaml`) from the provided links.
2. Use StartLeft's REST API for conversion, starting the server with `startleft server` and submitting the ABACUS file and mapping file via a CURL request:

```shell
curl --location --request POST localhost:5000/api/v1/startleft/diagram --header "Content-Type: multipart/form-data" --header "Accept: application/json" --form diag_type="ABACUS" --form diag_file=@"./abacus_merged.json" --form default_mapping_file=@"./iriusrisk-abacus-mapping.yaml" --form id="abacus-basic-example" --form name="Abacus Basic Example"
```

This streamlined process ensures a smooth conversion of ABACUS architectures into comprehensive OTM threat models, leveraging StartLeft's REST API for efficient integration.
