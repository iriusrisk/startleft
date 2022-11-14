# Terraform examples

## Sources
You can find some sample source files inside the `examples` directory:

* `examples/terraform` contains Terraform example files to convert into OTM format.
* `examples/terraform/split` contains a complete Terraform example file split into two different files.

To process this examples, it is mandatory to use the mapping files according to the file data type.
You can find some sample mapping files inside the `examples/terraform` directory.

## Examples

StartLeft supports parsing Terraform source files. Some examples are provided in the `examples/terraform` and
`examples/terraform/split` directories.

```shell
startleft parse \
	--iac-type TERRAFORM \
	--mapping-file iriusrisk-tf-aws-mapping \
	--output-file elb.otm \
	--project-name "Terraform ELB" \
	--project-id "terraform-elb" \
	elb.tf
```
