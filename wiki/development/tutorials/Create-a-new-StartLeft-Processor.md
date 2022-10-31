# Create a new StartLeft Processor (SLP)

---
As you can see in the [architecture page](../Architecture.md) StartLeft Processors (SLPs) are the special kind of modules
where the conversion into OTM logic is actually implemented. All of them are based in the same interfaces, defined in the 
`slp_base` module. So, if you want to create a new SLP, you simply have to:
* Create the module with an implementation class for each `slp_base` interface.
* Implement freely your solution inside the module.
* Add your module to the StartLeft configuration associating it to an input format.

Below you have a guided tutorial for creating a new SLP for a very basic invented input format that you can use as a base
for building your own.

## Defining a sample input format

---
> **Note**: The SLPs are classified in IaC, Diagram or External Threat Model (ETM). However, it is only
> a logical division and the instructions defined in this tutorial are valid for creating SLPs of any kind.

To guide this tutorial, let's imagine a fictitious Infrastructure as Code format, that we will call _My Awesome Infrastructure
Source (MAIS)_. A sample file of this format could be something like:
```json
{
  "resources": [
    {
      "id": 1,
      "name": "My Server",
      "type": "server"
    }
  ]
}
```

We need to define a format for the mappings between the source file and OTM. An example of this mapping file could be:
```yaml
trustZones:
  - id: public-cloud
    name: Public Cloud
    default: true

components:
  - source_type: server
    otm_type: otm-server
```

So the resulting OTM for this example should be something like:
```json
{
  "otmVersion": "0.1.0",
  "project": {
    "name": "My Project",
    "id": "my-project"
  },
  "representations": [
    {
      "name": "My Awesome Infrastructure Source",
      "id": "My Awesome Infrastructure Source",
      "type": "code"
    }
  ],
  "trustZones": [
    {
      "id": "public-cloud",
      "name": "Public Cloud",
      "risk": {
        "trustRating": 10
      }
    }
  ],
  "components": [
    {
      "id": "1",
      "name": "My Server",
      "type": "otm-server",
      "parent": {
        "trustZone": "public-cloud"
      }
    }
  ],
  "dataflows": []
}
```

## Understanding the `slp_base` interfaces

---
The `OtmProcessor` class inside the `slp_base` module defines the conversion process using a template method, whose behavior depends on the implementations
of the rest of the interfaces in the module.
<p align="center"><img src="../../images/conversion-process.png"></p>

In order to implement our sample processor, we need to know the structure of the provided interfaces, that looks like this.
<p align="center"><img src="../../images/slp_base-interfaces.png"></p>

## Creating the module

---
For this tutorial, we are going to create a new SLP for parsing _My awesome input source (MAIS)_ files which is going to be called
`slp_mais`. First, we need to set up our development environment as explained in the [Quickstart Guide for Developers](../Quickstart-Guide-for-Developers.md).


### Build the module structure
> **Note**: Do not worry if at this point you get some errors from the IDE. We will create some required modules and classes later.

Every module must have a common structure and minimum files to work. So let's start by creating them. 

1. Create the module folder `slp_mais` under the root `startleft` repo folder:

2. Override the module importer for the module (for preventing forbidden imports among modules) by creating a `slp_mais/__init__.py` 
file with this content:
```python
###################################################################
# This folder is not actually intended to be a regular package    #
# HOWEVER, we need to keep this __init.py__ file in order to      #
# make it visible by other modules.                               #
# In future versions, this package should be moved to a lib so    #
# that it will be an independent module instead a "false" package #
###################################################################
# DON'T REMOVE: Module importer overwritten to prevent bidirectional dependencies
from _sl_build.secure_importer import override_module_importer
override_module_importer()

from .slp_mais import *

```

3. Create the production code package, creating a folder `slp_mais/slp_mais` folder with an`__init__.py` file that exports
  the processor we are going to create in the next steps:
```python
from .mais_processor import MAISProcessor
```

4. Create the test code module as a `slp_mais/tests` folder with an empty `__init__.py` inside it.

5. Create packages for unit and integration tests:
   * `slp_mais/tests/unit` with an empty `__init__.py` file inside it.
   * `slp_mais/tests/integration` with an empty `__init__.py` file inside it.
   
6. Create an empty `slp_mais/tests/resources` folder.

After following this steps, your module should like this:
<p align="center"><img src="../../images/basic-module-structure.png"></p>

### Add the MAIS type to the Provider types
Every source type supported by StartLeft must be included in the enums contained in `slp_base/slp_base/provider_type.py`. 
As we have stated before, MAIS is a fictitious IaC source, so we will add it to the `IacType` enum.
```python
from otm.otm.provider import Provider


class IacType(str, Provider):
    # [...]
    MAIS = ("MAIS", "My Awesome Infrastructure Source", "code")
```

### Implement `slp_base` interfaces
> **Note**: In order to simplify this tutorial, we will not implement any validation nor process loading or processing errors, but, for 
> a real implementation, yu must read the [errors management page](../Errors-Management.md) to know the errors you should 
> raise in each stage of the conversion process.

We already know the main structure of the conversion process, so we can create our own implementation classes in the production 
code package (`slp_mais/slp_mais`).

#### MAISValidator (ProviderValidator)
Create the `mais_validator.py` file with the `MAISValidator` class implementing `ProviderValidator`. 
```python
import logging

from slp_base import ProviderValidator

logger = logging.getLogger(__name__)


class MAISValidator(ProviderValidator):

    def __init__(self, mais_data):
        super(MAISValidator, self).__init__()
        self.mais_data = mais_data

    def validate(self):
        logger.info('Validating MAIS file')
```

#### MAISLoader (ProviderLoader)
Create the `mais_loader.py` file with the `MAISLoader` class implementing `ProviderLoader`:

```python
import json
import logging

from slp_base.slp_base.provider_loader import ProviderLoader

logger = logging.getLogger(__name__)


class MAISLoader(ProviderLoader):

    def __init__(self, mais_source):
        self.mais_source = mais_source
        self.mais = {}
        
    def load(self):
        logging.getLogger('Loading MAIS source...')
        self.mais = json.loads(self.mais_source)

    def get_mais(self) -> {}:
        return self.mais
```

#### MAISMappingValidator (MappingValidator)
Create the `mais_mapping_validator.py` file with the `MAISMappingValidator` class implementing `MappingValidator`:
```python
import logging

from slp_base import MappingValidator


logger = logging.getLogger(__name__)


class MAISMappingValidator(MappingValidator):
    def __init__(self, mais_mapping_file):
        self.mais_mapping_file = mais_mapping_file

    def validate(self):
        logger.info('Validating MAIS mapping file')
```

#### MAISMappingLoader (MAISMappingLoader)
Create the `mais_mapping_loader.py` file with the `MAISMappingLoader` class implementing `MAISMappingLoader`:

```python
import yaml
import logging

from slp_base import MappingLoader

logger = logging.getLogger(__name__)


class MAISMappingLoader(MappingLoader):

    def __init__(self, mapping_data: bytes):
        self.mapping_data = mapping_data
        self.mais_mapping = {}

    def load(self):
        logger.info("Loading MAIS mapping file...")
        self.mais_mapping = yaml.load(self.mapping_data, Loader=yaml.SafeLoader)

    def get_mais_mapping(self):
        return self.mais_mapping
```

#### MAISParser (ProviderParser)
Create `mais_parser.py` file with the `MAISParser` class implementing `ProviderParser`. It will need to contain, 
  at least, the minimum information to parse the source and create the OTM, this is:
   * The ID of the OTM project.
   * The name of the OTM project.
   * The MAIS source.
   * The MAIS mappings.

Here is included almost trivial logic for processing our imaginary format, but this is the class where
you would need to actually implement your custom conversion process.
   
```python
from otm.otm.otm import OTM, Trustzone, Component
from otm.otm.otm_builder import OtmBuilder
from slp_base.slp_base.provider_parser import ProviderParser
from slp_base.slp_base.provider_type import IacType


class MAISParser(ProviderParser):

    def __init__(self, project_id: str, project_name: str, source, mais_mapping):
        self.project_id = project_id
        self.project_name = project_name
        self.source = source
        self.mais_mapping = mais_mapping

    def build_otm(self) -> OTM:
        return OtmBuilder(self.project_id, self.project_name, IacType.MAIS) \
            .add_components(self.__parse_components()) \
            .add_trustzones(self.__parse_trustzones()) \
            .build()

    def __parse_trustzones(self) -> [Trustzone]:
        default_trustzone = self.__get_default_trustzone()
        return [Trustzone(default_trustzone['id'], default_trustzone['name'])]

    def __parse_components(self) -> [Component]:
        component_mappings = self.mais_mapping['components']
        types_mappings = dict(zip(
            [cm['source_type'] for cm in component_mappings],
            component_mappings))

        otm_components = []
        for mais_component in self.source['resources']:
            source_type = mais_component['type']
            if source_type not in types_mappings:
                continue

            otm_components.append(Component(
                id=str(mais_component['id']),
                name=mais_component['name'],
                type=types_mappings[source_type]['otm_type'],
                parent=self.__get_default_trustzone()['id'],
                parent_type='trustZone'
            ))

        return otm_components

    def __get_default_trustzone(self) -> dict:
        return next(filter(lambda tz: 'default' in  tz and tz['default'], self.mais_mapping['trustZones']))
    
```
#### MAISProcessor (OtmProcessor)
Finally, we are going to create the main class, the `MAISProcessor`, in a `mais_processor.py` file for implementing the 
`OtmProcessor` interface. This class must implement methods for retrieving instances of all the other classes created above:
```python
from slp_base import MappingLoader, MappingValidator
from slp_base import OtmProcessor
from slp_base import ProviderValidator
from slp_base.slp_base.provider_loader import ProviderLoader
from slp_base.slp_base.provider_parser import ProviderParser
from slp_mais.slp_mais.mais_loader import MAISLoader
from slp_mais.slp_mais.mais_mapping_loader import MAISMappingLoader
from slp_mais.slp_mais.mais_mapping_validator import MAISMappingValidator
from slp_mais.slp_mais.mais_parser import MAISParser
from slp_mais.slp_mais.mais_validator import MAISValidator


class MAISProcessor(OtmProcessor):

    def __init__(self, project_id: str, project_name: str, sources: [bytes], mappings: [bytes]):
        self.project_id = project_id
        self.project_name = project_name
        self.source = sources[0]
        self.mappings = mappings[0]
        self.loader = None
        self.mapping_loader = None

    def get_provider_validator(self) -> ProviderValidator:
        return MAISValidator(self.source)

    def get_provider_loader(self) -> ProviderLoader:
        self.loader = MAISLoader(self.source)
        return self.loader

    def get_mapping_validator(self) -> MappingValidator:
        return MAISMappingValidator(self.mappings)

    def get_mapping_loader(self) -> MappingLoader:
        self.mapping_loader = MAISMappingLoader(self.mappings)
        return self.mapping_loader

    def get_provider_parser(self) -> ProviderParser:
        mais = self.loader.get_mais()
        mais_mapping = self.mapping_loader.get_mais_mapping()
        return MAISParser(self.project_id, self.project_name, mais, mais_mapping)
```

Once you have created all the implementations, your slp_module package should appear like this:
<p align="center"><img src="../../images/complete-module-structure.png"></p>

### Testing the SLP
We have already implemented all the necessary classes to perform the conversion from MAIS to OTM, so let's create a test
to verify they are working fine.

#### Create the test resources
We are going to create a single happy path test using the resources from the 
[Defining a sample input format](#Defining-a-sample-input-format) section. So, inside the `slp_mais/tests/resources` folder:

1. Copy the MAIS source file with the name `mais-sample.json`.
2. Copy the mapping file with the name `mapping-sample.yaml`.
3. Copy the expected OTM resulting file with the name `expected-otm.otm`.


#### Implement the test
Now we can create a simple test that verifies that the conversion process is working fine for the basic files created above. For that,
create a `test_mais_processor.py` file inside the `slp_mais/slp_mais/tests/integration` folder:
```python
import os
from sl_util.sl_util.file_utils import get_data
from slp_base.tests.util.otm import validate_and_diff
from slp_mais.slp_mais.mais_processor import MAISProcessor

SAMPLE_PROJECT_ID = 'my-project'
SAMPLE_PROJECT_NAME = 'My Project'

resources_path = f'{os.path.dirname(__file__)}/../resources'


class TestMAISProcessor:

    def test_single_component_mais_file_ok(self):
        # GIVEN a simple MAIS file with a single component
        mais_file = get_data(f'{resources_path}/mais-sample.json')

        # AND a MAIS mapping file that defines a mapping for that component
        mapping_file = get_data(f'{resources_path}/mapping-sample.yaml')

        # AND an expected OTM result
        expected_otm = f'{resources_path}/expected-otm.otm'

        # WHEN MAISProcessor::process is invoked
        otm = MAISProcessor(
            project_id=SAMPLE_PROJECT_ID,
            project_name=SAMPLE_PROJECT_NAME,
            sources=[mais_file],
            mappings=[mapping_file]
        ).process()


        # THEN a valid OTM file matching expected is generated
        assert validate_and_diff(otm, expected_otm, []) == {}

```

The whole module appears now like this:

<p align="center"><img src="../../images/module-with-tests-structure.png"></p>


**You are done! Execute the test and verify that the conversion process is happily performed!**

## Configuring and exposing the SLP
At this point we already have our processor up and running, so it is time to expose it. For that, 
no code is needed, and you only need to perform the configuration steps below.

## Configure the module
1. Go to the `_sl_build/modules.py` class, where you can find the modules' configuration.
2. In the `PROCESSORS` variable, add `slp_mais` as `forbidden_dependency` for all the existent SLP modules.
3. Create a new entry in the array with the configuration for our `slp_mais` module:
```python
    {
        'name': 'slp_mais', 
        'type': 'processor', 
        'provider_type': 'MAIS',
        'forbidden_dependencies': ['startleft', 'slp_cft', 'slp_tf', 'slp_visio', 'slp_mtmt']
     }
```
 
## Try it on the REST API
Launch the REST API as explained in the [Quickstart Guide for Developers](../Quickstart-Guide-for-Developers.md)
and check the Swagger page in [http://localhost:5000/docs](http://localhost:5000/docs). You can see that the MAIS IaC
type is already available in the `POST /iac` endpoint:

<p align="center"><img src="../../images/iac-mais.png"></p>

If you try to perform the request with the sample source and mapping files used across this tutorial, you can see that 
the server is returning the expected OTM as a response.
