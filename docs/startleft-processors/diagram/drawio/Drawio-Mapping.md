# Drawio mapping


---

??? note "This mapping configuration only applies to Drawio Processor."

    Please refer to another mapping file configuration documentation if needed. 
    You can locate each processor's documentation in the left menu under the "StartLeft Processors (SLP)" section. 

A source mapping file (or 'mapping file' for short) describes how to find and map components and
trust zones in the source Drawio file.

This mapping file is divided into two sections. The syntax and available functions used to define trust zone and 
component mappings are identical.

* `trustzones`.
* `components`.

## How mapping works?
Every shape in the diagram is loaded by the Drawio processor along with its name and internal Drawio type. Extracting 
the type is a key part of the parsing process and is explained in deep [here](Drawio-Calculating-Shape-Type.md).

Once the shapes are loaded, the mapping files are used to change the type of the components to the one expected in the 
OTM file. If no coincidence is found, a default type (`empty-component`) is set.

### Mapping preference
There are two mapping files, the default and the custom ones. Inside them, there are trust zone and component mappings.
The shapes in the Drawio files can be mapped by its type or name. The preference is the following:

1. Custom mappings prevails over default mappings.
2. Name matches during mapping prevails over type matches.
3. Trust zone mappings prevails over component mappings.
    
### Mapping functions
Both for components or trust zones, there are different ways to define mappings. A set of functions are available to 
simplify the creation of the mapping file. These functions work for mapping by name or type.

#### Mapping by exact match
The simplest case, when the `label` in the mapping file matches exactly the component name or type.

```yaml
  - label: aws.s3
    type: s3
```

#### Mapping by a Regex
Instead of searching for an exact match, a regex can be used to leverage the mapping capabilities.

```yaml
  - label: {$regex: ^aws.s3\_.*$}
    type: s3
```

#### Mapping by list
It is used when a group of name or types must be mapped to the same type in the OTM.

```yaml
  - label:
      - aws.ec2
      - aws.ec2_c6a_instance
      - aws.ec2_c6gn_instance
      - aws.ec2_c6i_instance
      - aws.ec2_c6in_instance
    type: ec2
```

#### (Optional) Set the component name as a tag
If you specify the optional `name` in the mapping, its value will be added as a tag in the OTM component.

```yaml
  - label:  aws.s3
    type:   s3
    name:   AWS S3 Bucket
```

The OTM component will include, among others, the following attributes:

- `type`: The type defined in the mapping file
- `name`: The original name of the shape from the source file
- `tags`: The name specified in the mapping file

```json
{
  "type": "s3",
  "name": "My Bucket",  
  "tags": ["AWS S3 Bucket"]
}
```


### The Default Trust Zone
The [OTM standard](../../../Open-Threat-Model-(OTM).md) defines that every component in the
threat model must have a parent. Frequently, the original Drawio diagram has components that are not nested inside any
parent. In those cases, the trust zone set as a default in the mapping file is included in the OTM as their parent.

```yaml
  - label: Public Cloud
    type: public-cloud
    default: true
```

!!! note ""
    Notice that this Trust Zone can be created more than once. If there is a component in the original diagram called
    "Public Cloud", a Trust Zone object will be created in the OTM. Then, if there are some missing components, a
    default Trust Zone of the same type will be created again to gather them.