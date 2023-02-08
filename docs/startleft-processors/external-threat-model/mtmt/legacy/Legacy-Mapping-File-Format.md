## Mapping file legacy format

Due to a backward compatibility StartLeft accepts the legacy mapping file format.
For the current mapping file format, please read [MTMT-Mapping](../MTMT-Mapping.md)



Unlike the new mapping file format, the legacy one had the **id** field,
with the identifier of the trust zone type.

Legacy format example:
```yaml
trustzones:
  - label:  Generic Trust Border Boundary
    type:   Public Cloud
    id:     6376d53e-6461-412b-8e04-7b3fe2b397de
```

When we found a `Generic Trust Border Boundary` in the MTMT file, then a Trustzone is created
in the OTM with these fields:
- **id** is the original id in the MTMT file
- **name** is the original name in the MTMT file
- **type** is the mapping's **id**, if present. If not, will be the mapping's **type**

In the above example the resultant OTM would contain a TrustZone like this:
```json
  {"trustZones": [
  {
    "id": "7537441a-1c03-48c0-b9c8-f82d5906c139",
    "name": "Internet",
    "type": "6376d53e-6461-412b-8e04-7b3fe2b397de",
    "risk": {
      "trustRating": 10
    },
    "properties": {
      "Name": "Internet"
    }
  }]}
```