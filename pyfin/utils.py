import os
import random as r
import string
from typing import Union, List

import astropy.units as u
from astropy.time import Time
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
    params = {}
    # Placeholder for now
    for key, value in dictionary.items():
        # if value can be written to yaml:
        params[key] = value
    with open(file, 'w') as f:
        yaml.dump(params, f)
    

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

def option(
        options: list,
        default: str = None,
        allow_text_entry: bool = True
):
    for i, opt in enumerate(options):
        print(i, opt)

    selection = None
    picked = None

    while selection is None or picked is None:
        selection = input()
        if selection == "" and default is not None:
            selection = default
        if selection.isnumeric():
            selection = int(selection)
        # The user may type their option instead of making a numeric selection.
        elif allow_text_entry and selection in options:
            picked = selection
            selection = options.index(picked)
            return selection, picked
        else:
            if allow_text_entry:
                print("Invalid response. Please enter an integer, or type a valid option.")
            else:
                print("Invalid response. Please enter an integer.")
            continue
        try:
            picked = options[selection]
        except IndexError:
            print(f"Response is not in provided options. Please select an integer from 0 to {len(options) - 1}")
    print(f"You have selected {selection}: {picked}")
    return selection, picked


def enter_time(message: str):
    date = None
    while date is None:
        date = input(message + "\n")
        print()
        try:
            date = Time(date)
        except ValueError:
            print("Date format not recognised. Try again:")
    return date


def select_option(
        message: str,
        options: Union[List[str], dict],
        default: Union[str, int] = None,
        sort: bool = False,
        include_exit: bool = True,
        allow_text_entry: bool = True
) -> tuple:
    """
    Options can be a list of strings, or a dict in which the keys are the options to be printed and the values are the
    represented options. The returned object is a tuple, with the first entry being the number given by the user and
    the second entry being the corresponding option. If a dict is passed to options, the second tuple entry will be the
    dict value.
    :param message: Message to display before options.
    :param options: Options to display.

    :param default: Option to return if no user input is given.
    :param sort: Sort options?
    :return: Tuple containing (user input, selection)
    """
    if type(default) is str:
        default = options.index(default)
    if default is not None:
        message += f" [default: {default} {options[default]}]"
    print()
    print(message)

    dictionary = False
    if type(options) is dict:
        dictionary = True
        options_list = []
        for opt in options:
            options_list.append(opt)
        if sort:
            options_list.sort()
    else:
        options_list = options

    if sort:
        options_list.sort()
    if include_exit:
        options_list.append("Exit")

    selection, picked = option(options=options_list, default=default, allow_text_entry=allow_text_entry)
    if include_exit and picked == "Exit":
        exit()
    if dictionary:
        return selection, options[picked]
    else:
        return selection, picked


def select_yn(message: str, default: Union[str, bool] = None):
    message += " (y/n) "
    positive = ['y', 'yes', '1', 'true', 't']
    negative = ['n', 'no', '0', 'false', 'f']
    if default in positive or default is True:
        positive.append("")
        message += f"[default: y]"
    elif default in negative or default is False:
        negative.append("")
        message += f"[default: n]"
    elif default is not None:
        print("Warning: default not recognised. No default value will be used.")
    print(message)
    inp = None
    while inp is None:
        inp = input().lower()
        if inp not in positive and inp not in negative:
            print("Input not recognised. Try again:")
    if inp in positive:
        print("You have selected 'yes'.")
        return True
    else:
        print("You have selected 'no'.")
        return False


def select_yn_exit(message: str):
    options = ["No", "Yes"]
    opt, _ = select_option(message=message, options=options, include_exit=True)
    if opt == 0:
        return False
    if opt == 1:
        return True


def user_input(message: str, input_type: type = str, default=None):
    inp = None
    if default is not None:
        if type(default) is not input_type:
            try:
                default = input_type(default)

            except ValueError:
                print(f"Default ({default}) could not be cast to {input_type}. Proceeding without default value.")

        message += f" [default: {default}]"

    print(message)
    while type(inp) is not input_type:
        inp = input()
        if inp == "" or inp is None:
            inp = default
        if type(inp) is not input_type:
            try:
                inp = input_type(inp)
            except ValueError:
                print(f"Could not cast {inp} to {input_type}. Try again:")
    print(f"You have entered {inp}.")
    return inp
