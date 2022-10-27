# Quickstart Guide for Developers

---

StartLeft is an Open Source project open to collaborators to extend or improve its functionality. Despite the fact that 
it was born as an internal IriusRisk project, there are some characteristic that makes it specially suitable to grown 
through the contributions of the community:
* The nature of the project, whose natural functional escalation is based on the support of new, independent, source formats.
* The conversion into OTM is based on configuration files that can also be created independently depending on the expected
  OTM use.
* The [modularized architecture](Architecture.md) enables collaborators to contribute to each format's processor without conflicts.

## How to contribute?

---
The IriusRisk team is currently the coordinator of the project and, ultimately, the responsible for validating the Pull Requests
created by the collaborators. All you need to know before start contributing is explained in the [Contributing.md](../../Contributing.md) 
file. Anyway, it is important to consider that, before creating your own fork or PR, you should check the 
[open issues](https://github.com/iriusrisk/startleft/issues) to assure that there is no one related with what you pretend to do.

## Set up the environment

---
There are no special requirements about a specific IDE or special steps to perform that makes StartLeft different from any
Python project. However, as PyCharm (or IntelliJ with the python plugin) is one of the most common python IDEs, some related 
facilities are provided related to it.

### Basic configuration
Regardless the IDE you use, we can generalize the cloning of the project and the creation and configuration of the python virtual 
environment.

First, we need to clone the project and move to its project:
```shell
git clone https://github.com/iriusrisk/startleft.git
cd startleft
```

Then, let's create and activate a virtual environment for StartLeft:
```shell
python3 -m venv ./venv
source venv/bin/activate
```

Now, install all the required dependencies, including the ones required for setup and test, in this virtual environment:
```shell
pip install -e ".[setup,test]"
```

If everything worked fine, you should be able to start the server inside this virtual environment and with no errors in 
shown in the logs:
```shell
startleft server
```

At this point, you have the project completely configured to start working with the IDE or editor you prefer.

### PyCharm/IntelliJ setup

#### Open the project
The project is already cloned and configured, so simply go to `File > Open...` and select the
project folder.

#### Configure the python interpreter
As we have already configured a virtual environment, PyCharm will recognize it and propose it as the project interpreter:

<p align="center"><img src="../images/interpreter.png"></p>

We only need to click on _Configure a Python interpreter..._ and accept the proposed one.

#### Import the run configurations
Since StartLeft is a quite complex project with different commands and test sets that can be launched independently, 
a set of portable and preconfigured run configurations are provided. So, the final configuration step is to import them
following the instructions detailed [here](Run-Configurations.md) and assure that you can execute StartLeft from your PyCharm.

## Architecture

---
With your development environment ready, it is strongly advised to take a look to the [architecture page](Architecture.md)
to familiarize yourself with the different modules, including their relationships and common internal structure. This is
specially relevant considering that forbidden imports between modules will remain in _python collect_ errors that prevent 
StartLeft to start and that may confuse you.

## Creating a new StartLeft Processor

---
Once you have the environment in place and a general idea about the organization of the code, we can already take a look 
to the most common use cases for StartLeft contributions through the documented tutorials.

A very interesting situation is when the user want to make StartLeft support a new format. In that case, you will need to 
know the interfaces you need to implement and the minimal configuration to expose it through the CLI and the REST API.

You can easily go through this creation process in this [tutorial page](tutorials/Create-a-new-StartLeft-Processor.md).
