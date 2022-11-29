# MTMT elements position

---

StartLeft takes the position information from the border boundaries
in order to represent the elements in the OTM at the same canvas position
than the original.

For this purpose we have:
 - The [Representation](https://github.com/iriusrisk/OpenThreatModel/blob/main/README.md#diagram)
for the OTM
 - The [RepresentationElement](https://github.com/iriusrisk/OpenThreatModel/blob/main/README.md#representation-element-for-diagram)
for the components and trust zones

## OTM
In the representations of the OTM we are going to have a diagram representation, because
MTMT has diagram relevant information, such the canvas size. 
```json
{
    "otmVersion": "0.1.0",
    "project": {
        "name": "Example Project",
        "id": "example-project"
    },
    "representations": [
        {
            "name": "Microsoft Threat Modeling Tool",
            "id": "Microsoft Threat Modeling Tool",
            "type": "threat-model"
        },
        {
            "name": "example-project Diagram Representation",
            "id": "example-project-diagram",
            "type": "diagram",
            "size": {
                "width": 2000,
                "height": 2000
            }
        }
    ]}
```

#### Representation fields
- `name`: The name of this representation
- `id`: The unique id of this representation. This field will be the reference for the 
trustzones and components representations
- `type`: The representation supported type. See [representation-supported-types](https://github.com/iriusrisk/OpenThreatModel/blob/main/README.md#representation-supported-types)
- `size`: The canvas width and height


## Trustzones

The `representations` element has two properties for the position info:

- `size`
- `position`

```json
   {
  "representations": [
    {
      "name": "Cloud Representation",
      "id": "acafa4b0-f94d-4077-8a42-74b959bd0796-representation",
      "representation": "example-project-diagram",
      "size": {
        "width": 535,
        "height": 488
      },
      "position": {
        "x": 734,
        "y": 88
      }
    }
  ]
}
```

### Trustzone representation fields
 - `name`: The name of this representation
 - `id`: The unique id of this representation
 - `representation`: The id of the OTM representation explained before
 - `size`: The width and height of the trust zone
 - `position`: The position relative to the canvas

This applies for the border boundaries trust zones.

The trust zones delimited by a MTMT line boundary won't have representations because 
its source size is undefined.


## Components

Into the OTM components we have the `representations` property too, with the same
fields as the trust zone.

The difference between the component representation and the trust zone representation
is the position.

While at the trustzones the position is relative to the canvas, 
in the components the position is relative to the parent trust zone.
Here an example:

```json
{
  "components": [
    {
      "id": "53245f54-0656-4ede-a393-357aeaa2e20f",
      "name": "Accounting PostgreSQL",
      "type": "CD-MICROSOFT-AZURE-DB-POSTGRESQL",
      "parent": {
        "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
      },
      "properties": {
        "Name": "Accounting PostgreSQL",
        "Out Of Scope": "false",
        "Azure Postgres DB Firewall Settings": "Select",
        "Azure Postgres DB TLS Enforced": "Select"
      },
      "representations": [
        {
          "name": "Accounting PostgreSQL Representation",
          "id": "53245f54-0656-4ede-a393-357aeaa2e20f-representation",
          "representation": "example-project-diagram",
          "size": {
            "width": 100,
            "height": 100
          },
          "position": {
            "x": 334,
            "y": 45
          }
        }
      ]}
    ]}
```
