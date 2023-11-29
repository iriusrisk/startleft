## Mapping file legacy format 

Due to a backward compatibility StartLeft accepts the legacy mapping file format.
For the current mapping file format, please read [Visio-Mapping](../visio/Visio-Mapping.md)



Unlike the new mapping file format, the legacy one had the **id** field,
 with the identifier of the trust zone type.

Legacy format example:
```yaml
trustzones:
  - label:  Public Cloud
    type:   Public Cloud
    id:     b61d6911-338d-46a8-9f39-8dcd24abfe91
```

When a shape is found in the Visio file whose **name** matches the mapping's **label**, then a Trustzone is created
in the OTM with these fields:
- **id** is the original id in the Visio file
- **name** is the original name in the Visio file
- **type** is the mapping's **id**, if present. If not, will be the mapping's **type**

In the above example the resultant OTM would contain a TrustZone like this:
```json
{
  "trustZones": [
    {
      "id": "47",
      "name": "My Public Cloud",
      "type": "b61d6911-338d-46a8-9f39-8dcd24abfe91",
      "risk": {
        "trustRating": 10
      }
    }
  ]
}
```