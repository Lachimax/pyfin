import os
from typing import Union

import astropy.io.misc.yaml as yaml


def read_yaml(file: str) -> dict:
    """Reads a YAML file from disk, returning as a dict.

    Args:
        file (str): path to load YAML file from.

    Returns:
        dict: the YAML contents, represented asa dictionary.
    """
    if os.path.isfile(file):
        with open(file) as f:
            p = yaml.load(f)
    else:
        p = None
    return p

def write_yaml(file: str, dictionary: dict):
    """Writes a dictionary to disk in YAML format.

    Args:
        file (str): Path to write YAML file to.
        dictionary (dict): Dictionary to write.
    """
    with open(file, 'w') as f:
        yaml.dump(dictionary, f)
        