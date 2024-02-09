# ABACUS Mapping

---

??? note "This mapping configuration only applies to the ABACUS Processor."

    Please refer to another mapping file configuration documentation if needed. 
    You can locate each processor's documentation in the left menu under the "StartLeft Processors (SLP)" section.

A source mapping file (or 'mapping file' for short) describes how to find and map components and
trust zones in the source ABACUS file.

This mapping file is divided into two sections. The syntax and available functions used to define trust zone and
component mappings are identical.

* `trustzones`.
* `components`.

## How mapping works?

Every element in the ABACUS model is loaded by the ABACUS processor along with its name and internal ABACUS type.

Once the elements are loaded, the mapping files are used to change the type of the components to the one expected in the
OTM file. If no coincidence is found, a default type (`empty-component`) is set.

### Mapping preference

There are two mapping files, the default and the custom ones. Inside them, there are trust zone and component mappings.
The elements in the ABACUS files can be mapped by its type or name. The preference is the following:

1. Custom mappings prevail over default mappings.
2. Name matches during mapping prevail over type matches.
3. Trust zone mappings prevail over component mappings.

### Mapping functions

Both for components or trust zones, there are different ways to define mappings. A set of functions are available to
simplify the creation of the mapping file. These functions work for mapping by name or type.

#### Mapping by exact match

The simplest case, when the `label` in the mapping file matches exactly the component name or type.

```yaml
  - label: abacus.application
    type: application

```

#### Mapping by a Regex

Instead of searching for an exact match, a regex can be used to leverage the mapping capabilities.

```yaml
  - label: { $regex: ^abacus.application\_.*$ }
    type: application
```

#### Mapping by list

It is used when a group of name or types must be mapped to the same type in the OTM.

```yaml
  - label:
      - abacus.server
      - abacus.database
      - abacus.network
    type: infrastructure
```

### The Default Trust Zone

The [OTM standard](../../../Open-Threat-Model-(OTM).md) defines that every component in the threat model must have a
parent.
Frequently, the original ABACUS model has elements that are not nested inside any parent.
In those cases, the trust zone set as a default in the mapping file is included in the OTM as their parent.

```yaml
  - label: Data Center
    type: data-center
    default: true
```

!!! note "" Notice that this Trust Zone can be created more than once.
If there is a component in the original ABACUS model called "Data Center",
a Trust Zone object will be created in the OTM. Then, if there are some missing components,
a default Trust Zone of the same type will be created again to gather them.