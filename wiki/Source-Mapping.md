A source mapping file (or 'mapping files' for short) describe how to find components, dataflows, and trustzones in source file data structures.

To accomplish this, a mapping file contains additional logic around a collection of JMESPath queries which are used.
Also, some exclusive Startleft actions based upon JMESPath may be used in mapping files to solve the most complex mappings.

Source mapping files are made up of three main sections corresponding the main sections in an OTM file, plus an optional lookup section described below:

* trustZones
* components
* dataflows

Each contains a list of 0 or more objects that describe how to find the respective object in the source file, and each object has a number of required and optional fields. 

Take a look at the [JSONSchema](https://github.com/iriusrisk/startleft/blob/main/startleft/data/mapping_schema.json) file for more details.

## JMESPath Queries

Special $action fields begin with a dollar sign ($) and do not directly contribute to the OTM output. Instead, they specify an action and behaviour used to process the source files or generate the OTM output. 

This table describes each special $actions.

| $action          | Description                                                                                                                                                                                                                                                                                     | Example                                                                                                                                                                                                                                                                                                     |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| $source          | Specifies the source of the object type                                                                                                                                                                                                                                                         | $source: {$root: "Resources&#124;squash(@)[?Type=='AWS::EC2::VPC']"}                                                                                                                                                                                                                                        |
| $root            | JMESPath search through the entire source file data structure                                                                                                                                                                                                                                   | $root: "Resources&#124;squash(@)[?Type=='AWS::EC2::VPC']"                                                                                                                                                                                                                                                   |
| $path            | JMESPath search through the object identified in the $source. A default value is optional by using the $searchParams structure                                                                                                                                                                  | $path: "Type" <br/>$path: "Properties.VpcId.Ref"<br/>$path: {$searchParams:{ searchPath: "Properties.SubnetId.Ref", defaultValue: "b61d6911-338d-46a8-9f39-8dcd24abfe91"}}                                                                                                                                  |
| $findFirst       | JMESPath search through the list of objects identified in the $source and returning the first successful match. A default value is optional by using the $searchParams structure                                                                                                                | $findFirst: ["Properties.FunctionName.Ref", "Properties.FunctionName"] <br/> $findFirst: {$searchParams:{ searchPath: ["Properties.SubnetId.Ref","Properties.SubnetId"], defaultValue: "b61d6911-338d-46a8-9f39-8dcd24abfe91"}}                                                                             |
| $format          | A named format string based on the output of other $special fields. Note, only to be used for id fields.                                                                                                                                                                                        | $format: "{name}"                                                                                                                                                                                                                                                                                           |
| $catchall        | A sub-field of $source, specifying a default search for all other objects not explicitly defined                                                                                                                                                                                                | $catchall: {$root: "Resources&#124;squash(@)"}                                                                                                                                                                                                                                                              |
| $skip            | A sub-field of $source, specifying specific objects to skip if not explicitly defined                                                                                                                                                                                                           | $skip: {$root: "Resources&#124;squash(@)[?Type=='AWS::EC2::Route']"}                                                                                                                                                                                                                                        |
| $singleton       | A sub-field of $source, specifying specific objects to be unified under a single component or trustzone                                                                                                                                                                                         | $singleton: { $root: "Resources&#124;squash(@)[?Type=='AWS::SecretsManager::Secret']"}                                                                                                                                                                                                                      |
| $numberOfSources | When using singleton, allows you to set different values for output name or tags when the number of sources for the same mapping are single or multiple                                                                                                                                         | $numberOfSources: {oneSource:{$path: "_key"}, multipleSource:{ $format: "CD-ACM (grouped)" }}                                                                                                                                                                                                               |
| $altsource       | Specifies an alternative mapping when $source returns no object.                                                                                                                                                                                                                                | $altsource:<br/>       - $mappingType: {$root: "Resources&#124;squash(@)[?Type=='AWS::EC2::VPCEndpoint']"}<br/>         $mappingPath: {$path: "Properties.ServiceName"}<br/>         $mappingLookups:<br/>           - regex: ^(.*)s3$<br/>             name: S3 from VPCEndpoint<br/>             type: s3 |
| $lookup          | Allows you to look up the output of a $special field against a key-value lookup table                                                                                                                                                                                                           | $lookup:   {path: "Properties.Subnets[]&#124;map(&values(@), @)[]&#124;map(&re_sub('[:]', '-', @), @)"}                                                                                                                                                                                                     |
| $hub             | Only for dataflow's "source" and "destination" fields. Especially created for building dataflows from Security Group structures without generating components from them. Allows to define abstract contact points for larger end-to-end final dataflows                                         | destination: {$hub: {$path: "Properties.GroupId"}}                                                                                                                                                                                                                                                          |
| $ip              | When defining a component's "name" field as $ip, will generate a singleton component for representing an external IP but without limitations of singleton for this case, so the "type" for the defined mapping definition with $ip (i.e. generic-terminal) will not be catalogued as singleton. | name: { $ip: { $path: "Properties.SecurityGroupEgress[0].CidrIp" } }                                                                                                                                                                                                                                        |


For more information on how to create a JMESPath search query, checkout the website: https://jmespath.org/

## Hardcoded values

In addition to using $source and other special $actions, you can also just hardcode values which will be taken and mapped as is. For example, you may want to specify a default trustzone which wouldn't be found anywhere in the source files. You can do this easily just by adding it to a mapping file:

```
trustzones:
  - id:   default-zone
    name: Default
```
For mapping trustzones to IriusRisk trustzones, `id` field must take internal IriusRisk values depending on the type of trustzone.
These values are defined in the internal CloudFormation mapping file.

## Lookup table

Just in case there are some inconsistencies in naming conventions used, and you need to be able to translate one name into another, a simple lookup key-value table section can be added to the mapping file.

For example, if we have a situation where a subnet name is written using a short naming convention, but is actually referred to via a longer name elsewhere, we can use the $lookup action.

```
parent:
  $lookup: {$path: "Properties.Subnets[]|map(&values(@), @)[]|map(&re_sub('[:]', '-', @), @)"}
```

If the above query returns a subnet called `shortnameA`, then it will be looked up in the below table:

```
lookup:
  shortnameA: amuchlongernameA
  shortnameB: amuchlongernameB
```

To give a final value of `amuchlongernameA`.

## Additional JMESPath functions

Parsing of IaC files may be sometimes complex, so that the built-in JMESPath described above are not enough. For that cases,
a set of custom functions has been created to simplify and make more powerful the creation of mapping files.

### re_sub
The `re_sub` function replaces the occurrences of `pattern` with `replace` in the given `string`. 

```python
def _func_re_sub(self, pattern, replace, origin_string)
```

For example, we may want to replace colon characters with hyphens such as in `re_sub('[:]', '-', 'stack:subnet')`.

### squash
The `squash` function takes a nested object of objects, and squashes them into a list of objects, injecting the parent "key" to the child object as "_key".

```python
def _func_squash(self, obj)
```

This function is specially useful for Cloudformation mapping files. These have a root `Resources` object whose 
top level keys are the resource names which have the resource objects as values. This structure is hard to iterate over 
without losing the important name key. So you can use squash it and refer to the name through the `_key` field. 

```yaml
name:    {$path: "_key"}
$source: {$root: "Resources|squash(@)[?Type=='AWS::EC2::Subnet']"}
```

### tail
The `tail` function returns the characters of a given `string` from the `count` index onwards. It is equivalent to
python's `string[count:]`.

```python
def _func_tail(self, string, count)
```

### get

The `get` function takes a dictionary array of components whose root key is the **type** of the component. The other argument
is a component type to filter the array. It returns a component dictionary whose root key is the **name** of the component
that also includes a `Type` and a `_key` keys with the component type and the component name respectively.

```python
def _func_get(self, obj_arr, component_type)
```

This function is mainly used for Terraform mappings in order to retrieve components by their type. An example of its use
is: `resource|get(@, 'aws_subnet')`.

### get_starts_with

This function is equivalent to `get`, but instead of using the `component_type` argument to perform an exact filter, the target
component type must starts with it.

```python
def _func_get_starts_with(self, obj_arr, component_type)
```

### split

The `split` function is the equivalent to the python's one. It breaks a given string based on a given separator and returns
the resulting array of strings. It is equivalent to python's `split` function. 

```python
def _func_split(self, string, separator)
```

For instance, this function is used in Terraform mappings to retrieve the name of a referenced component, whose naming
structure is `component-type.component-name.some-field`. In this case, the name is retrieved as: `split(component, '.')[1]`.