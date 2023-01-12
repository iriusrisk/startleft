Visio diagrams contain visual information about your infrastructure or threat model that may be useful to keep. 
During the parsing of the `vsdx` file, the `slp_visio` processor is able to extract this representation data and 
include it in the resultant OTM.

## Where is the representation data located?
We use two OTM structures to store the representation data:

* The **<a href="https://github.com/iriusrisk/OpenThreatModel#representations-object" target="_blank">Representation object</a>**
  is placed at the root level and contains information about the general representation of the Threat Model, for 
  instance, its type or the size of the canvas.
* The **<a href="https://github.com/iriusrisk/OpenThreatModel#representationelement-object" target="_blank">RepresentationElement object</a>**
  is placed at Component or TrustZone level and contains representation info of that element as its position and size.

## What representation data is included?
Position and size data extracted from the Visio file source are included. It is relevant to notice that no 
different types of shapes are supported and **all Components and TrustZones will be represented in the OTM as rectangles**.

![visio-representations.drawio (2).png](img/visio-representations.png)

### Position calculation
> :octicons-light-bulb-16: In the case of TrustZones, the parent element is the limit of the Visio diagram itself.

The `position` attribute of the 
<a href="https://github.com/iriusrisk/OpenThreatModel#representationelement-object" target="_blank"> OTM RepresentationElement object</a>
contains:

* `x`. Distance from the **LEFT** side of the parent element to the left side of the child element.
* `y`. Distance from the **TOP** of the parent element to the top of the child element. 

### Size calculation
The `size` attribute of the
<a href="https://github.com/iriusrisk/OpenThreatModel#representationelement-object" target="_blank"> OTM RepresentationElement object</a>
contains:

* `width`. It is the difference between the right `x` value minus the left one.
* `height`. It is the difference between the bottom `y` value minus the top one.

### Excluded representations
It is very important to consider that all the information included in the OTM is directly extracted from the 
Visio file and not calculated by the `slp_visio`. This means that some elements will never have representations in 
the OTM:

* The **boundary TrustZones** represents an ambiguous zone that is not explicitly defined in the source diagram, so 
  they will not have a representation object.
* The **default TrustZone** may contain elements from different places of the diagram and neither has any 
  representation info in the source Visio, so no representation object can be calculated.
* The **Components** without parent in the source Visio will be nested into the default TrustZone. Since this does 
  not have representation and the Components' position must be relative, they will not have representation.
* The **Dataflows** between elements must unequivocally identify their origin and target, so no representation 
  information is transferred to the OTM.

## How Visio representation data is processed?
The Visio position information and the OTM representation data do not exactly fit, so some transformations are required:

* **Diagram limits calculation**. Visio diagrams are unbounded, so it is necessary to find their boundaries in 
  some way. In that case, they are calculated using the position of the elements at their ends.
* **Origin translation**. Visio diagrams origin is located in the bottom left. Since the OTM representations origin 
  is on the top left, it is necessary to recalculate the `y` position from the diagram's top limit.
* **Precision and scale**. OTM representation values must be integers. However, Visio data is in float 
  precision, so it is rescaled and rounded. <u>The scale factor is expected to be parametrizable in the future</u>, but 
  for now, it is fixed to the IriusRisk scale (based on DrawIO). This means that each Visio representation parameter 
  is processed as follows:

```python
IRIUSRISK_SMALLEST_COMPONENT_SIZE = 82
VISIO_STENCILS_DEFAULT_SIZE = 0.5

SCALE_FACTOR: int = round(IRIUSRISK_SMALLEST_COMPONENT_SIZE / VISIO_STENCILS_DEFAULT_SIZE)
```


## An example
Let's take this Visio example:

![img_1.png](img/representations-example.png)


??? tip "OTM parsing result"

    If we parse it into OTM, the result would be something like this:

    ```json
      {
          "otmVersion": "0.1.0",
          "project": {
              "name": "VISIO",
              "id": "VISIO"
          },
          "representations": [
              { // (1)!
                  "name": "VISIO Diagram Representation",
                  "id": "VISIO-diagram",
                  "type": "diagram",
                  "size": { // (2)!
                      "width": 1826,
                      "height": 1207
                  }
              }
          ],
          "trustZones": [
              {
                  "id": "b61d6911-338d-46a8-9f39-8dcd24abfe91",
                  "name": "Public Cloud",
                  "risk": {
                      "trustRating": 10
                  },
                  "representations": [
                      { // (3)!
                          "name": "Public Cloud Representation",
                          "id": "67-representation", // (4)!
                          "representation": "VISIO-diagram",
                          "size": {
                              "width": 661,
                              "height": 551
                          },
                          "position": {
                              "x": 328,
                              "y": 328
                          }
                      }
                  ]
              },
              { // (5)!
                  "id": "2ab4effa-40b7-4cd2-ba81-8247d29a6f2d",
                  "name": "Private Secured",
                  "risk": {
                      "trustRating": 10
                  }
              }
          ],
          "components": [
              {
                  "id": "49",
                  "name": "Custom VPC",
                  "type": "empty-component",
                  "parent": {
                      "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
                  },
                  "representations": [
                      {
                          "name": "Custom VPC Representation",
                          "id": "49-representation",
                          "representation": "VISIO-diagram",
                          "size": { // (6)!
                              "width": 246,
                              "height": 256
                          },
                          "position": { // (7)!
                              "x": 361,
                              "y": 31
                          }
                      }
                  ]
              },
              {
                  "id": "1",
                  "name": "Amazon EC2",
                  "type": "ec2",
                  "parent": {
                      "component": "49"
                  },
                  "representations": [
                      { // (8)!
                          "name": "Amazon EC2 Representation",
                          "id": "1-representation",
                          "representation": "VISIO-diagram",
                          "size": {
                              "width": 82,
                              "height": 82
                          },
                          "position": { 
                              "x": 82,
                              "y": 25
                          }
                      }
                  ]
              },
              { // (9)!
                  "id": "30",
                  "name": "Private Database",
                  "type": "rds",
                  "parent": {
                      "trustZone": "2ab4effa-40b7-4cd2-ba81-8247d29a6f2d"
                  }
              },
              {
                  "id": "41",
                  "name": "Custom log system",
                  "type": "cloudwatch",
                  "parent": {
                      "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
                  },
                  "representations": [
                      { // (10)!
                          "name": "Custom log system Representation",
                          "id": "41-representation",
                          "representation": "VISIO-diagram",
                          "size": {
                              "width": 82,
                              "height": 82
                          },
                          "position": {
                              "x": 443,
                              "y": 370
                          }
                      }
                  ]
              },
              {
                  "id": "69",
                  "name": "Custom enterprise GW",
                  "type": "api-gateway",
                  "parent": {
                      "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
                  },
                  "representations": [
                      { // (11)!
                          "name": "Custom enterprise GW Representation",
                          "id": "69-representation",
                          "representation": "VISIO-diagram",
                          "size": {
                              "width": 171,
                              "height": 171
                          },
                          "position": {
                              "x": 28,
                              "y": 128
                          }
                      }
                  ]
              }
          ],
          "dataflows": [ // (12)!
              {
                  "id": "17",
                  "name": "fe940e8c-f9ec-4a58-a555-5ef4119e97b6",
                  "source": "1",
                  "destination": "41"
              },
              {
                  "id": "34",
                  "name": "0b3f1707-1a91-44b8-bb06-5bfd7617e315",
                  "source": "1",
                  "destination": "30"
              },
              {
                  "id": "70",
                  "name": "16f21508-d45f-4beb-aa59-7189264e5385",
                  "source": "69",
                  "destination": "1"
              }
          ]
      } 
    ```

    1. A diagram representation for the Visio source.
    2. The size of the diagram is based on its components.
    3. Absolute position based on the main diagram canvas.
    4. Reference to the diagram representation id.
    5. No representation for boundary TrustZone.
    6. The dimensions are based in the width and height of the rectangle.
    7. Relative position to the parent TrustZone.
    8. Relative representation to the parent VPC.
    9. No representation because it belongs to a boundary TrustZone.
    10. Relative representation to the parent TrustZone.
    11. Relative representation to the parent TrustZone calculated from its rectangle envelope.
    12. No representations for Dataflows.

