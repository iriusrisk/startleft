## What is Lucidchart?

From <a href="https://www.lucidchart.com/" target="_blank">official Lucidchart page</a>:
> Lucidchart is the intelligent diagramming application that brings teams together to make better decisions and 
> build the future.

## Parsing particularities

Lucidchart does not have its own extension for exporting. Instead of that, it enables their users to download 
their diagrams in several ways. One of them is VSDX, which is the Microsoft Visio format supported by StartLeft. 
**All the Visio documentation about mapping and parsing logic applies for Lucidchart**. However, there are a couple 
of considerations that are important to know.

About the mappings:

* The structure of the mapping file is exactly the same that for the Microsoft Visio files.
* The stencils are different in Microsoft Visio and Lucidchart, so you need to compose different mappings for each of 
  them.
* The internal name of the Lucidchart stencil shapes does not match the one shown in the application. In the
  <a href="https://github.com/iriusrisk/startleft/blob/main/examples/lucidchart/iriusrisk-lucid-aws-mapping.yaml" target="_blank">mapping file</a>
  provided in the StartLeft examples folder, you can find a list of AWS components' internal names.

About the parsing logic:

* Boundary TrustZones are not currently supported for Lucidchart.
* Dataflows are calculated based on their position, what means that they do not necessarily need to _touch_ origin 
  or target shapes, but they have some tolerance.

## An example

In this example, we can see a Lucidchart diagram which includes different types of elements.

* Generic shapes like the _Internet_ TrustZone or the _Custom VPC_.
* Generic stencil shapes like the _Client_ and the _Mobile client_.
* AWS stencil shapes like the _Amazon CloudWatch_ or the _Amazon EC2_.
* Azure stencil shapes like the _SQLDatabaseAzure2021_.
* Several dataflows among the shapes.

Notice also that all the components in the diagram are nested inside others. All of them belong to a TrustZone, but, 
for example, the _Amazon EC2_ is also nested inside the _Custom VPC_. This hierarchy, as is done for Microsoft Visio, 
will be respected in the resultant OTM.

![img_1.png](img/lucid-example.png)

If we compose a default mapping file for all the stencil shapes:

??? abstract "default-mapping.yaml"

    ```yaml
    trustzones:
    - label:  Public Cloud
      type:   Public Cloud
      id:     b61d6911-338d-46a8-9f39-8dcd24abfe91
    
    - label:  Private Secured Cloud
      type:   Private Secured
      id:     2ab4effa-40b7-4cd2-ba81-8247d29a6f2d
    
    - label: AWSCloudAWS2021
      type: Public Cloud
      id: b61d6911-338d-46a8-9f39-8dcd24abfe91
    
    components:
    
    ## Visio Lucid names
    - label: ClientAWS19
      type: generic-client
    
    - label: AmazonCognitoAWS19
      type: cognito
    
    - label: AmazonEC2AWS2021
      type: ec2
    
    - label: SQLDatabaseAzure2021
      type: CD-MICROSOFT-AZURE-SQL-DB
    
    - label: DatabaseBlock
      type: other-database
    
    - label: AmazonSimpleStorageServiceS3AWS19
      type: s3
    
    - label: AWSIdentityandAccessManagement_IAMAWS19
      type: iam
    
    - label: AWSCloudTrailAWS19
      type: cloudtrail
    
    - label: AWSCloudTrailAWS2021
      type: cloudtrail
    
    - label: AmazonAPIGateway_purpleAWS19
      type: api-gateway
    
    - label: AWSGeneral_UserAWS19
      type: empty-component
    
    - label: ImageSearchBlock2
      type: empty-component
    
    - label: ElasticLoadBalancingELLoadBalancer2017
      type: empty-component
    
    - label: AmazonEC2AutoScalingAWS2021
      type: empty-component
    
    - label: AWSFargateAWS19
      type: empty-component
    
    - label: AmazonDynamoDBAWS19
      type: empty-component
    
    - label: AWSCertificateManagerAWS19
      type: empty-component
    
    - label: AWSCodePipelineAWS19
      type: empty-component
    
    - label: AWSCodeBuildAWS19
      type: empty-component
    
    - label: AmazonCloudWatchAWS19
      type: cloudwatch
    
    - label: AmazonCloudWatchAWS2021
      type: cloudwatch
    
    - label: AWSCodeStarAWS19
      type: empty-component
    
    - label: AmazonECR2017
      type: empty-component


    dataflows: [ ]
    ```

Then, we can map the generic shapes by name in a custom mapping file:

??? abstract "custom-mapping.yaml"
    
    ```yaml
    trustzones: 
      - label:  Internet
        type:   internet
        id:     f0ba7722-39b6-4c81-8290-a30a248bb8d9
        
    components:
        
      - label: Web browser
        type: generic-client
        
      - label: Android
        type: android-device-client

    dataflows: []
    ```

The expected result for this case should be an OTM like this:

??? abstract "lucidchart.otm"

    ```json
    {
      "otmVersion": "0.1.0",
      "project": {
          "name": "Lucid Example",
          "id": "lucid-example"
      },
      "representations": [{
          "name": "Visio",
          "id": "Visio",
          "type": "diagram",
          "size": {
              "width": 1000,
              "height": 1000
          }
      }],
      "trustZones": [{
          "id": "b61d6911-338d-46a8-9f39-8dcd24abfe91",
          "name": "Public Cloud",
          "risk": {
              "trustRating": 10
          }
      }, {
          "id": "2ab4effa-40b7-4cd2-ba81-8247d29a6f2d",
          "name": "Private Secured Cloud",
          "risk": {
              "trustRating": 10
          }
      }, {
          "id": "f0ba7722-39b6-4c81-8290-a30a248bb8d9",
          "name": "Internet",
          "risk": {
              "trustRating": 10
          }
      }],
      "components": [{
          "id": "7",
          "name": "Custom VPC",
          "type": "empty-component",
          "parent": {
              "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
          }
      }, {
          "id": "9",
          "name": "My EC2",
          "type": "ec2",
          "parent": {
              "component": "7"
          }
      }, {
          "id": "12",
          "name": "My CloudWatch",
          "type": "cloudwatch",
          "parent": {
              "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
          }
      }, {
          "id": "17",
          "name": "My API Gateway",
          "type": "api-gateway",
          "parent": {
              "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
          }
      }, {
          "id": "26",
          "name": "My CloudTrail",
          "type": "cloudtrail",
          "parent": {
              "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
          }
      }, {
          "id": "29",
          "name": "My Simple Storage Service (S3)",
          "type": "s3",
          "parent": {
              "trustZone": "b61d6911-338d-46a8-9f39-8dcd24abfe91"
          }
      }, {
          "id": "38",
          "name": "Web browser",
          "type": "generic-client",
          "parent": {
              "trustZone": "f0ba7722-39b6-4c81-8290-a30a248bb8d9"
          }
      }, {
          "id": "44",
          "name": "Android",
          "type": "android-device-client",
          "parent": {
              "trustZone": "f0ba7722-39b6-4c81-8290-a30a248bb8d9"
          }
      }, {
          "id": "47",
          "name": "SQL Database",
          "type": "CD-MICROSOFT-AZURE-SQL-DB",
          "parent": {
              "trustZone": "2ab4effa-40b7-4cd2-ba81-8247d29a6f2d"
          }
      }, {
          "id": "53",
          "name": "My DynamoDB",
          "type": "dynamodb",
          "parent": {
              "trustZone": "2ab4effa-40b7-4cd2-ba81-8247d29a6f2d"
          }
      }],
      "dataflows": [{
          "id": "32",
          "name": "EC2 Logs",
          "source": "9",
          "destination": "12"
      }, {
          "id": "33",
          "name": "GW/EC2",
          "source": "17",
          "destination": "9"
      }, {
          "id": "34",
          "name": "Log trace",
          "source": "17",
          "destination": "26"
      }, {
          "id": "35",
          "name": "Customer data",
          "source": "17",
          "destination": "29"
      }, {
          "id": "43",
          "name": "f7ef1b0f-2a7a-4822-9aa8-59affc9bf309",
          "source": "38",
          "destination": "17"
      }, {
          "id": "46",
          "name": "114deaf6-bb2d-407a-a68a-1fccb3d56ed7",
          "source": "44",
          "destination": "17"
      }, {
          "id": "56",
          "name": "User data",
          "source": "17",
          "destination": "53"
      }, {
          "id": "57",
          "name": "App data",
          "source": "17",
          "destination": "47"
      }]
    } 
    ```

That imported in a tool like IriusRisk looks like this:
![img_2.png](img/lucid-iriusrisk-example.png)

### cURL
> :warning: Lucidchart parsing is only supported currently through the REST API. CLI parsing will be probably 
> available in the medium term.

To try this example on your machine, first, you need to put in place the necessary files:

* Download the Lucidchart example above from
  <a href="https://github.com/iriusrisk/startleft/blob/main/examples/lucidchart/lucid-aws-with-tz-and-vpc.vsdx" target="_blank">here</a>.
* Save the default mapping above with the name `default-mapping.yaml`.
* Save the custom mapping above with the name `custom-mapping.yaml`.

Finally, execute the following command to retrieve the OTM file:

```shell
curl --location --request POST localhost:5000/api/v1/startleft/diagram \
--header "Content-Type: multipart/form-data" \
--header "Accept: application/json" \
--form diag_type="LUCID" \
--form diag_file=@"./lucid-aws-with-tz-and-vpc.vsdx" \
--form default_mapping_file=@"./default-mapping.yaml" \
--form custom_mapping_file=@"./custom-mapping.yaml" \
--form id="my-lucidchart-example" \
--form name="My Lucidchart Example"
```