---

Parsing of IaC files may be sometimes complex, so that the built-in JMESPath described above are not enough. For that cases,
a set of custom functions has been created to simplify and make more powerful the creation of mapping files.

## JMESPath functions

### re_sub
The `re_sub` function replaces the occurrences of `pattern` with `replace` in the given `string`.

```python
def _func_re_sub(self, pattern, replace, origin_string)
```

For example, we may want to replace colon characters with hyphens such as in `re_sub('[:]', '-', 'stack:subnet')`.

### squash_terraform
The `squash_terraform` function takes a nested object of objects, and squashes them into a list of objects, injecting 
the parent "key" to the child object as "_key".

```python
def _func_squash_terraform(self, obj)
```

These have a root `Resources` object whose top level keys are the resource names which have the resource objects as 
values. This structure is hard to iterate over without losing the important name key. So you can use squash it and 
refer to the name through the `_key` field.

```yaml
name:    {$path: "_key"}
$source: {$root: "Resources|squash_terraform(@)[?Type=='aws_instance']"}
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

The `get` function is mainly used for Terraform mappings in order to retrieve components by their type. An example of its use
is: `resource|get(@, 'aws_subnet')`.

### get_starts_with

This function is equivalent to `get`, but instead of using the `component_type` argument to perform an exact filter, the
target component type must starts with it.

```python
def _func_get_starts_with(self, obj_arr, component_type)
```

### split

The `split` function is the equivalent to the python's one. It breaks a given string based on a given separator and
returns the resulting array of strings. It is equivalent to python's `split` function.

```python
def _func_split(self, string, separator)
```

For instance, this function is used in Terraform mappings to retrieve the name of a referenced component, whose naming
structure is `component-type.component-name.some-field`. In this case, the name is retrieved
as: `split(component, '.')[1]`.

### get_module_terraform

The `get_module_terraform` function takes a dict array of Terraform modules (not resources) and a component type,
which is the key to filter the array comparing against 'source' module property. Returns an OTM component dict
whose root key is the name of the component that also includes a Type and a _key keys with the module type (AWS type)
and the module name (custom name) respectively.

```python
def _func_get_module_terraform(self, modules, module_type)
```