# What is StartLeft?
**StartLeft** is a tool for **generating threat models** written in the [Open Threat Model](Open-Threat-Model-(OTM).md) 
format **from a variety of different sources** such as IaC files, diagrams or projects exported from 
threat modelling tools.

### What input sources are supported?
Split by type, the currently supported input formats are:
* **Infrastructure as Code (IaC)**:
  * CloudFormation (CFT).
  * Terraform (TF).
* **Diagram**:
  * Visio.
* **Threat Model**:
  * Microsoft Threat Modelling Tool (MTMT).


## How can I try it?
Simply install the tool and play with its Command Line Interface. You can also set up a REST API with a single command
and consume it with any REST client as Postman. Anyway, **the best way to start is following the 
[Quickstart guide for beginners](quickstart/Quickstart-Guide-for-Beginners.md)**.

## How can I integrate it?
One of the most interesting aspects of StartLeft is that it is easily integrable within processes that may need to generate
threat models. For example, [IriusRisk](https://www.iriusrisk.com/) uses StartLeft as a service for creating OTM files as an intermediate state of the
external sources importing process. **The different ways of integrating StartLeft are described in the 
[Quickstart guide for integrations](quickstart/Quickstart-Guide-for-Integrations.md)**.

## How can I contribute?
StartLeft is an Open Source application whose modularized architecture based on processors is specially focused
on simplifying the collaboration for any developer. **If you want to contribute, check out the 
[Quickstart guide for developers](quickstart/Quickstart-Guide-for-Developers.md) and the [Contributing file](Contributing.md)**. 
