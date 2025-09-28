import os
import string
import random as r
from typing import Union

import astropy.units as u

import astropy.io.misc.yaml as yaml

def generate_id(length: int = 10):
    """Generate a random string to act as a unique ID. Does not check for uniqueness; this should be implemented in the class using this function.

    Args:
        length (int): Length of ID

    Returns:
        str: Generated ID
    """

    letters = string.ascii_lowercase
    numbers = string.digits
    return ''.join(r.choice(letters + numbers) for i in range(length))

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
        
def relevant_timescale(time: u.Quantity):

    if not time.unit.is_equivalent(u.second):
        raise ValueError(f"{time} is not a time.")

    microseconds = time.to(u.us)
    if microseconds < 1000 * u.us:
        return microseconds
    milliseconds = time.to(u.ms)
    if milliseconds < 1000 * u.ms:
        return milliseconds
    seconds = time.to(u.second)
    if seconds < 60 * u.second:
        return seconds
    minutes = time.to(u.minute)
    if minutes < 60 * u.minute:
        return minutes
    hours = time.to(u.hour)
    if hours < 24 * u.hour:
        return hours
    days = time.to(u.day)
    if days < 7 * u.day:
        return days
    weeks = time.to(u.week)
    if weeks < 52.2 * u.week:
        return weeks
    years = time.to(u.year)
    return years
