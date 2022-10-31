from slp_tf.slp_tf.parse.mapping.jmespath.tf_custom_jmespath import jmespath_search


def __find_first_search(search_path_root, source):
    for search_path in search_path_root:
        search_result = jmespath_search(search_path, source)
        if search_result is not None:
            return search_result


def __search_with_default(obj, source, action):
    try:
        search_params = obj[action]["$searchParams"]

        if "searchPath" in search_params:
            if action == "$path":
                search_result = jmespath_search(search_params["searchPath"], source)
            elif action == "$findFirst":
                search_result = __find_first_search(search_params["searchPath"], source)
            else:
                return []

            if search_result is None:
                return search_params.get("defaultValue", [])
            else:
                return search_result
        else:
            return []
    except:
        return []


def __multiple_source_search(tf_source_model, source, obj):
    single_value = None
    multiple_value = None
    if "multipleSource" in obj["$numberOfSources"]:
        multiple_value = tf_source_model.search(obj["$numberOfSources"]["multipleSource"], source)
    if "oneSource" in obj["$numberOfSources"]:
        single_value = tf_source_model.search(obj["$numberOfSources"]["oneSource"], source)
    return single_value, multiple_value


def root(mapping_source, **kwargs):
    """
    JMESPath search through the entire source file data structure
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source_model_data: The completely TF dictionary
    :return: The jmespath search of the $root value
    """
    source_model_data = kwargs.get("source_model_data", None)
    return jmespath_search(mapping_source["$root"], source_model_data)


def skip(mapping_source, **kwargs):
    """
    A sub-field of $source, specifying specific objects to skip if not explicitly defined
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
        tf_source_model: The TerraformSourceModel needed due the nature of recursive mapping function
    :return: The TerraformSourceModel search of the $skip value
    """
    tf_source_model = kwargs.get("tf_source_model")
    source = kwargs.get("source")
    return tf_source_model.search(mapping_source["$skip"], source)


def parent(mapping_source, **kwargs):
    """
    Search the parent ID in a specific array of parent IDs
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
        tf_source_model: The TerraformSourceModel needed due the nature of recursive mapping function
    :return: The TerraformSourceModel search of the $parent value
    """
    tf_source_model = kwargs.get("tf_source_model")
    source = kwargs.get("source")
    return tf_source_model.search(mapping_source["$parent"], source)


def singleton(mapping_source, **kwargs):
    """
    A sub-field of $source, specifying specific objects to be unified under a single component or trustzone
    :param mapping_source:  The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
        tf_source_model: The TerraformSourceModel needed due the nature of recursive mapping function
    :return: The TerraformSourceModel search of the $singleton value
    """
    tf_source_model = kwargs.get("tf_source_model")
    source = kwargs.get("source")
    return tf_source_model.search(mapping_source["$singleton"], source)


def catchall(mapping_source, **kwargs):
    """
    A sub-field of $source, specifying a default search for all other objects not explicitly defined
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
        tf_source_model: The TerraformSourceModel needed due the nature of recursive mapping function
    :return: The TerraformSourceModel search of the $catchall value
    """
    tf_source_model = kwargs.get("tf_source_model")
    source = kwargs.get("source")
    return tf_source_model.search(mapping_source["$catchall"], source)


def hub(mapping_source, **kwargs):
    """
    Only for dataflow's 'source' and 'destination' fields. Especially created for
    building dataflows from Security Group structures without generating components from them.
    Allows to define abstract contact points for larger end-to-end final dataflows
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
        tf_source_model: The TerraformSourceModel needed due the nature of recursive mapping function
    :return: The TerraformSourceModel search of the $hub value
    """
    tf_source_model = kwargs.get("tf_source_model")
    source = kwargs.get("source")
    return tf_source_model.search(mapping_source["$hub"], source)


def ip(mapping_source, **kwargs):
    """
    When defining a component's 'name' field as $ip, will generate a singleton component
    for representing an external IP but without limitations of singleton for this case,
    so the 'type' for the defined mapping definition with $ip (i.e. generic-terminal)
    will not be catalogued as singleton.
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
        tf_source_model: The TerraformSourceModel needed due the nature of recursive mapping function
    :return: The TerraformSourceModel search of the $ip value
    """
    tf_source_model = kwargs.get("tf_source_model")
    source = kwargs.get("source")
    return tf_source_model.search(mapping_source["$ip"], source)


def lookup(mapping_source, **kwargs):
    """
    Allows you to look up the output of a $special field against a key-value lookup table
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
        tf_source_model: The TerraformSourceModel needed due the nature of recursive mapping function
    :return: Find in the key-value lookup table by the $lookup attribute
    """
    tf_source_model = kwargs.get("tf_source_model")
    source = kwargs.get("source")
    keys = tf_source_model.search(mapping_source["$lookup"], source)
    if isinstance(keys, str):
        return tf_source_model.lookup[keys]
    elif isinstance(keys, list):
        results = []
        for key in keys:
            results.append(tf_source_model.lookup[key])
        return results


def path(mapping_source, **kwargs):
    """
    JMESPath search through the object identified in the $source.
    A default value is optional by using the $searchParams structure
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
    :return: Search through the object identified in the $source
    """
    source = kwargs.get("source")
    if "$path" in mapping_source:
        if "$searchParams" in mapping_source["$path"]:
            return __search_with_default(mapping_source, source, "$path")
        else:
            return jmespath_search(mapping_source["$path"], source)


def format(mapping_source, **kwargs):
    """
    A named format string based on the output of other $special fields. Note, only to be used for id fields
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
    :return: String based on the output of other $special fields
    """
    source = kwargs.get("source")
    return mapping_source["$format"].format(**source)


def find_first(mapping_source, **kwargs):
    """
    JMESPath search through the list of objects identified in the $source and returning the first successful match.
    A default value is optional by using the $searchParams structure
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
    :return: Returns the first successful match
    """
    source = kwargs.get("source")
    if "$searchParams" in mapping_source["$findFirst"]:
        return __search_with_default(mapping_source, source, "$findFirst")
    else:
        return __find_first_search(mapping_source["$findFirst"], source)


def number_of_sources(mapping_source, **kwargs):
    """
    When using singleton, allows you to set different values for output name or tags
    when the number of sources for the same mapping are single or multiple
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source: A section of the TF dictionary
        tf_source_model: The TerraformSourceModel needed due the nature of recursive mapping function
    :return: Tuple with the values defined in the oneSource and multipleSource attributes
    """
    tf_source_model = kwargs.get("tf_source_model")
    source = kwargs.get("source")
    return __multiple_source_search(tf_source_model, source, mapping_source)
