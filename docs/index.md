# What is StartLeft?

---

**StartLeft** is an automation tool for **generating Threat Models** written in the [Open Threat Model (OTM)](Open-Threat-Model-(OTM).md) 
format **from a variety of different sources** such as IaC files, diagrams or projects exported from 
Threat Modeling tools.

## Why StartLeft?

---

Automation and integration are the core goals of StartLeft. It was born as an internal project of 
<a href="https://www.iriusrisk.com/" target="_blank">IriusRisk</a>, whose leading threat 
modelling tool allows the users to build a complete Threat Model of an application only by depicting its architecture in a diagram.
However, there is a bunch of formats in which the architecture (or directly the TM) can be defined. This led
<a href="https://www.iriusrisk.com/" target="_blank">IriusRisk</a> to create and share with the community two key 
resources:

* **[Open Threat Model (OTM)](Open-Threat-Model-(OTM).md)**, a standardized and vendor-agnostic way to represent Threat Models 
    to make them easily portable between platforms.
* **StartLeft**, a tool for automating the conversion from different sources into OTM.

In some cases, StartLeft acts only as a format translator, like in case of diagrams or Threat Model sources, but it has also
specific and configurable logic for generating Threat Models (TMs) from Infrastructure as Code (IaC) files, which 
brings a great advantage reducing the necessary knowledge and manual work required for translating infrastructure 
into TM, as well as enabling the users to make amazing things like integrating the generation of the TM in a CI/CD 
pipeline of the actual IaC file.

StartLeft is currently an Open Source application powered by
<a href="https://www.iriusrisk.com/" target="_blank">IriusRisk</a>, that is already using it as an intermediate 
service for all the imports of new projects from external sources.


## What input sources are supported?

---

Split by type, the currently supported input formats are:

* **Infrastructure as Code (IaC)**:
    * <a href="https://aws.amazon.com/cloudformation/resources/templates/" target="_blank">CloudFormation (CFT)</a>.
    * <a href="https://www.terraform.io/" target="_blank">Terraform (TF)</a>.

* **Diagram**:
    * Microsoft Visio (including diagrams exported from Lucidchart).
    * Drawio

* **Threat Model**:
    * Microsoft Threat Modeling Tool (MTMT).


## How can I try it?

---

Simply install the tool and play with its Command Line Interface. You can also set up a REST API with a single command
and consume it with any REST client such as Postman. Anyway, **the best way to start is by following the 
[Quickstart guide for beginners](Quickstart-Guide-for-Beginners.md)**.

## How can I integrate it?

---

One of the most interesting aspects of StartLeft is that it is easily integrable within processes that may need to generate
Threat Models. **The different ways of integrating StartLeft are described in the 
[Quickstart guide for integrations](integration/Quickstart-Guide-for-Integrations.md)**.

## How can I contribute?

---

StartLeft is an Open Source application whose modularized architecture based on processors is specially focused
on simplifying the collaboration for any developer. **If you want to contribute, check out the 
[Quickstart guide for developers](development/Quickstart-Guide-for-Developers.md) and the 
<a href="https://github.com/iriusrisk/startleft/blob/main/CONTRIBUTING.md" target="_blank">CONTRIBUTING.md</a> file**.


