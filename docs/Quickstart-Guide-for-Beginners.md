# Quickstart Guide for Beginners
The aim of this page is enabling you to get the StartLeft application installed in your machine so that you can execute
some commands, set up the REST API and, in summary, familiarize yourself with the usage of the tool.

## Prerequisites

---
* Install the **[latest version of Python](https://www.python.org/downloads/)**.
* Install **[pip3](https://pip.pypa.io/en/stable/installation/)**.
* Install **[git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).**

*During this guide some files will be downloaded or generated, so you can optionally create a folder to keep them
organized.*


> :bulb:  **_Linux-based OS are recommended to run StartLeft_**


??? "Extra requisites for Windows/OSX users"

    StartLeft uses <a href="https://github.com/ahupp/python-magic" target="_blank">python-magic</a> 
    interface to the libmagic file type identification library for validating file types.
    
    <ins>Prerequisites for Windows</ins>

     *"You'll need DLLs for libmagic usage on Windows. @julian-r maintains a pypi package with the DLLs, you can fetch it with:"*
    ```shell
    pip install python-magic-bin
    ```
    
    <ins>Prerequisites for OSX</ins>

     * When using Homebrew: `brew install libmagic`
     * When using macports: `port install file`



## Install StartLeft

---
Install the last stable version of the tool using pip:
```shell
pip install git+https://github.com/iriusrisk/startleft.git
```

Check your installation with the command:
```shell
startleft --version
```

That should return something like:
```shell
startleft, version <your-installed-version>
```

## The parse command

---
The `parse` is the main command of the StartLeft CLI that enables you to perform the whole process of conversion
to OTM by providing one or multiple source files and a mapping file. It presents slight variations depending on the type 
of input source that you can check in the [CLI](usage/Command-Line-Interface.md) section or in each specific processor 
documentation, but, to get an idea of its behavior, you can perform a conversion from an IaC file:

First of all, let's download one of the examples contained in the StartLeft's `examples/terraform` folder:

```shell
wget https://raw.githubusercontent.com/iriusrisk/startleft/main/examples/terraform/multinetwork_security_groups_with_lb.tf
```

This is a rich example where you can see in action some capabilities of StartLeft. It represents the Threat 
Model for
an architecture with two TrustZones and several VPCs which contain many types of AWS components.

Now, we need to download the mapping file where the configuration for parsing this source is located. In this case, 
we will download an example that maps to IriusRisk components. It is placed in the same `examples/terraform` folder:

```shell
wget https://raw.githubusercontent.com/iriusrisk/startleft/main/examples/terraform/iriusrisk-tf-aws-mapping.yaml
```

With this two files we are ready to execute the `parse` command in order to generate the Threat Model in OTM format:
```shell
startleft parse \
	--iac-type TERRAFORM \
	--mapping-file iriusrisk-tf-aws-mapping.yaml \
	--output-file multinetwork_security_groups_with_lb.otm \
	--project-name "Terraform MN Security Groups with LB" \
	--project-id "tf-mn-sg-lb" \
	multinetwork_security_groups_with_lb.tf
```

Finally, you can open the generated `multinetwork_security_groups_with_lb.otm` with your favourite text editor and check 
how a Threat Model has been automatically generated from the Terraform file. 

## The server command

---
Using StartLeft as a service is the most useful strategy for integrate it with other tools. The different ways of 
configuring this service are deeply described in the [Quickstart guide for Integrations](integration/Quickstart-Guide-for-Integrations.md) 
and [REST API](usage/REST-API.md) sections. However, you can begin to familiarize yourself with this mode by setting up the server 
through the CLI using the command:
```shell
startleft server
```
Then open a web browser, in [http://localhost:5000/docs](http://localhost:5000/docs) you will find a Swagger page with the documentation of the API.
It is completely functional, so you can just send requests from there to get used to the tool. 

## Auxiliary commands

---
In addition to `parse`, the CLI provides you with a group of utility commands that simplify a lot of the work with the 
files involved in the OTM conversions performed by StartLeft.

### help
Undoubtedly the most insightful command, it gives you information about everything you have available through the CLI.

It can be used in general:
```shell
startleft --help
```
Or for specific commands:
```shell
startleft parse --help
```

### validate
This command is able to perform validations over three types of files:
#### **IaC mapping files**
Described in depth in each processor's docs, they are used to create relationships between types in the source
and their expected equivalent in the OTM (i.e: an `aws_instance` type in Terraform matches the `ec2` type in IriusRisk).
If we take the same mapping file we have downloaded for the `parse` command, we can execute:
```shell
startleft validate --iac-mapping-file iriusrisk-tf-aws-mapping.yaml
```

#### **Diagram mapping files**
Also described in the processors' documentation, allows you to validate the format of mapping
files used for diagram conversions. 
    
Let's download the IriusRisk's Visio mapping file located in the `examples/visio` folder:
```shell
wget https://raw.githubusercontent.com/iriusrisk/startleft/main/examples/visio/iriusrisk-visio-aws-mapping.yaml
```
Now we can validate it using the following StartLeft command:
```shell
startleft validate --diagram-mapping-file iriusrisk-visio-aws-mapping.yaml
```

#### **OTM** 
These files may have been generated by StartLeft or handcrafted by any user. To see how to validate 
an OTM file, we can download an example from the `examples/manual` folder.
```shell
wget https://raw.githubusercontent.com/iriusrisk/startleft/main/examples/manual/manual.otm
```

And then validate it by executing:
```shell
startleft validate --otm-file manual.otm
```

#### All at once
Finally, the command is also able to execute multiple validations at the same time:
```shell
startleft validate \
    --otm-file manual.otm \
    --iac-mapping-file iriusrisk-tf-aws-mapping.yaml \
    --diagram-mapping-file iriusrisk-visio-aws-mapping.yaml
```

### search
This is an auxiliary utility only supported currently for IaC mapping files. Due to the complexity of these files, 
sometimes it is useful to test some expressions directly before including them in the final mapping file. 

For example, let's use the same Terraform file that we have downloaded for the `parse` command and perform a simple query:

```shell
startleft search \
    --iac-type TERRAFORM \
    --query "resource|get(@, 'aws_synthetics_canary')" \
    multinetwork_security_groups_with_lb.tf
```


