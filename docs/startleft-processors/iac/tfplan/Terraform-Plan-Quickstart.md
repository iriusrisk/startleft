## What is Terraform Plan?

---
From the <a href="https://developer.hashicorp.com/terraform/cli/commands/plan" target="_blank">official Terraform page</a>: 
> The terraform plan command creates an execution plan, which lets you preview the changes that 
> Terraform plans to make to your infrastructure.
> 
> - Reads the current state of any already-existing remote objects to make sure that the Terraform state is up-to-date

From the StartLeft perspective, the Terraform Plan Processor (`slp_tfplan`) leverages the Terraform CLI capabilities
to generate a unique Terraform resource file with the final infrastructure and its configuration.

## The `slp_tfplan` module

---
The `slp_tfplan` module is the StartLeft Processor responsible for converting an existing Terraform execution plan 
(`tf-plan`) along with its graphic representation (`tf-graph`) into an OTM. 
This operation is based on a mapping file that enables the client to define the translations between the Terraform resources and the expected 
output in the OTM file. 

???+ abstract "How does it work?" 

    We rely on the Terraform CLI to deal with the complexity of a Terraform infrastructure deployment, which is summarized in two single files:

    - **Terraform Plan.** It contains all the resources along with its configuration. 
    - **Terraform Graph.** It contains the relationships between the resources.

    With these two files, we are able to compose a complete architecture diagram by parsing all the components and their relationships.


Once you got familiarized yourself with the basics explained on this page, you will need to know more about how to 
use and customize the behavior of the processor. To configure your conversions, you should take a look at 
[TFplan mapping page](Terraform-Plan-how-to-create-a-mapping-file.md), where you will find all the information you 
need, from basic to advanced, to build your mapping files.

Apart from this, you may also find interesting the generic usage manuals for the [CLI](../../../usage/Command-Line-Interface.md) 
and [REST API](../../../usage/REST-API.md).

## How to use it?

---
Firstly, it is necessary to generate the `tf-plan` and `tf-graph` files by the Terraform CLI.

???+ abstract "Generating my own Terraform files"

    :zero: Execute the Terraform init (only once):
    ```
    terraform init
    ```
    
    :one: Generate the Terraform plan file in JSON format:
    ```
    terraform plan -out=tf-plan
    terraform show -json tf-plan >> tf-plan.json
    ```
    
    :two: Generate the Terraform graph file:
    ```
    terraform graph -type=plan -plan=tf-plan >> tf-graph.gv
    ```

Next, you need to have a mapping file to configure the processor mapping behavior.
??? example "Terraform Plan Mapping File Example"

    > In the [TFplan mapping page](Terraform-Plan-how-to-create-a-mapping-file.md) you will find all the information you need, from 
    basic to advanced, to build your mapping files.

    ```yaml
    --8<-- "examples/tfplan/iriusrisk-tfplan-aws-mapping.yaml"
    ```

Now everything is set up. The last step is to execute the commands for IaC `TFPLAN` parsing to generate the OTM. 

### CLI
> **Note**: Before continue, make sure you have 
> [StartLeft properly installed](../../../Quickstart-Guide-for-Beginners.md) in your machine.

Save the files above in your file system with these names:

* `tf-plan.json` for the Terraform plan file.
* `tf-graph.gv` for the Terraform graph file.
* `ir-mappings.yaml` for the mapping file.

Now we are going to execute StartLeft for these files so that an `ec2.otm` file will be generated in our working 
directory.
```shell
startleft parse \
	--iac-type TFPLAN \
	--mapping-file ir-mappings.yaml \
	--output-file output.otm \
	--project-id "my-project" \
	--project-name "My project" \
	tf-plan.json tf-graph.gv
```

### cURL
You can get the same result through the StartLeft REST API. For that, first, we need to set up the
server with the command:
```shell
startleft server
```

Then, execute the following command to retrieve the OTM file:
```shell
curl --location --request POST localhost:5000/api/v1/startleft/iac \
--header "Content-Type: multipart/form-data" \
--header "Accept: application/json" \
--form iac_type="TFPLAN" \
--form iac_file=@"./tf-plan.json" \
--form iac_file=@"./tf-graph.gv" \
--form mapping_file=@"./ir-mappings.yaml" \
--form id="my-project" \
--form name="My project"
```

## More examples

---
The infrastructure built with Terraform may be as complex as you want. For that reason StartLeft, through the mapping files, 
is intended to be configurable, so you can extend or modify its behavior and/or create your mappings on demand.

To help you to walk through more complex situations with larger Terraform and mapping files, you can see all available
examples under the Terraform Examples section.