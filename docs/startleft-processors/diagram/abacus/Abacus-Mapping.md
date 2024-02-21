
# ABACUS Mapping  Guide

**Important**: This guide is specific to the ABACUS Processor. If you're working with a different processor, please consult the appropriate documentation available in the "StartLeft Processors (SLP)" section accessible from the left navigation menu.

## Overview

This document provides instructions for configuring mapping files for the ABACUS Processor. Mapping files are essential for identifying and assigning components and trust zones within an ABACUS source file.

Mapping files are organized into two main sections:

- **Trust Zones**
- **Components**

Both sections utilize the same syntax and functions for defining mappings.

## How Mapping Works

When an ABACUS model is processed, each element—along with its name and internal ABACUS type—is loaded. The mapping files then adjust the component types to match those expected in the OTM file. Absent a matching type, the element is assigned a default type of `empty-component`.

### Mapping Hierarchy

Mapping files can be either default or custom, with the following precedence rules:

1. **Custom Mappings:** Take precedence over default mappings.
2. **Name-based Mappings:** Have priority over type-based mappings.
3. **Trust Zone Mappings:** Override component mappings.

### Defining Mappings

Mappings can be established by name or type, using a variety of functions to facilitate this process.

#### Exact Match Mapping

For direct matches between the mapping file `label` and the component name or type:

```yaml
- label: abacus.application
  type: application
```

#### Regex Mapping

To match components or trust zones using regular expressions:

```yaml
- label: { $regex: ^abacus.application\_.*$ }
  type: application
```

#### List Mapping

To map multiple names or types to a single type in the OTM file:

```yaml
- label:
    - abacus.server
    - abacus.database
    - abacus.network
  type: infrastructure
```

### Default Trust Zone Handling

Per the OTM standard [OTM standard](../../../Open-Threat-Model-(OTM).md), each component must be associated with a parent trust zone. For elements in the ABACUS model not nested within a trust zone, a default trust zone specified in the mapping file will be used as their parent in the OTM.

```yaml
- label: Data Center
  type: data-center
  default: true
```

**Note**: It's possible to create multiple instances of this default Trust Zone. For example, if there's an actual component named "Data Center" in the ABACUS model, it will be recognized as a Trust Zone in the OTM. Additionally, if there are unassociated components, a new default Trust Zone of the same type will be created to encompass them.
