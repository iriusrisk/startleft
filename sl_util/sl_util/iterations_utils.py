# This weird while needs to be done because:
# - The foreach does not work if you remove an element from the list
# - The remove has to be invoked on the list to affect the object passed as a class attribute
def remove_from_list(collection: [],
                     filter_function,
                     remove_function=None) -> None:
    if collection is None:
        return
    i = 0
    while i < len(collection):
        element = collection[i]
        if filter_function(element):
            remove_function(element) if remove_function is not None else collection.remove(element)
        else:
            i += 1


def remove_duplicates(duplicated_list: []):
    unique_list = []

    for element in duplicated_list:
        if element not in unique_list:
            unique_list.append(element)

    return unique_list
