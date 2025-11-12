"""
General helper functions useful for building the configuration.
"""

from typing import TypeVar 


T = TypeVar("T")


def get_for_era(objects: dict[str | tuple[str], T], era: str, default: T = None) -> T:
    """
    Return objects in dictionary `objects` for the respective for the respective `era`.

    The keys in `objects` can either be single strings representing an era or tuples of strings
    representing a collection of eras. The objects can have an arbitrary type `T`.

    The `objects` dictionary can be structured as follows:

    ```python
    {
        ("2016preVFP", "2016postVFP", "2017", "2018"): ProducerRun2,
        "2022preEE": Producer2022preEE,
        "2022postEE": Producer2022postEE,
    }
    ```
    If the `default` argument is specified, the function returns this value if no matching item has
    been found in `objects`.
    
    :param objects: Dictionary with objects for different eras
    :param era: Name of the era, for which the object is requested
    :param default: Default value to be returned if no matching item is found. Optional.

    :return: Object in `objects` corresponding to `era`.

    :raises KeyError: If keys in `objects` are not strings or tuples of strings, or if the keys are
                      not unique.
    :raises ValueError: If no matching item is found and no default value is specified.
    """

    # Collect all keys and check if they are unique and flatten the objects dictionary
    # Raise an exception if the keys are not a string or a tuple of strings
    # Raise an exception if there are duplicate keys
    keys = []
    _objects = {}
    for key in objects.keys():
        if isinstance(key, str):
            keys.append(key)
            _objects[key] = objects[key]
        elif isinstance(key, tuple) and all(isinstance(k, str) for k in key):
            keys.extend(list(key))
            for k in key:
                _objects[k] = objects[key]
        else:
            raise KeyError(
                f"Invalid key type {type(key)} in 'objects' dictionary; expected str or tuple of "
                "str."
            )
    if len(keys) != len(set(keys)):
        raise KeyError(f"Keys of 'objects' dictionary are not unique: {keys}.")

    # Return the object for the respective era if it exists in the flattened dictionary
    if era in _objects:
        return _objects[era]
    
    # Return the default value if specified
    if default is not None:
        return default

    # If no matching item is found at this point, raise an exception
    raise ValueError(f"No object found for era {era}, and no default value specified.")
