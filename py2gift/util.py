# AUTOGENERATED! DO NOT EDIT! File to edit: 02_util.ipynb (unless otherwise specified).

__all__ = ['render_latex', 'AccessorEndowedClass', 'int_to_roman', 'dict_to_yaml', 'yaml_to_dict',
           'write_multiple_categories', 'supplement_file_name', 'add_name',
           'wrong_numerical_solutions_from_correct_one']

# Cell

import pathlib
import re
import sys
from typing import List, Dict, Union, Optional

import numpy as np
import IPython.display
import ruamel.yaml
import yaml
import pandas as pd
from pandas.core.accessor import _register_accessor as register_accessor

import gift_wrapper.core
import gift_wrapper.question
import gift_wrapper.image

# Cell

def render_latex(text: str) -> str:

    return IPython.display.Markdown(re.sub(r'\$([^\$]*)\$', '$' + '\\\Large ' + r'\1' + '$', text))

# Cell
class AccessorEndowedClass:

    _accessors = set()

# Cell

# taken from https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-1.php
def int_to_roman(num: int) -> str:
    """
    Returns an integer number in roman format.
    """

    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

assert int_to_roman(12) == 'XII'
assert int_to_roman(9) == 'IX'

# Cell

def dict_to_yaml(d: dict, output_file: Union[str, pathlib.Path]) -> None:

    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=2)

    with open(output_file, 'w') as f:

        yaml.dump(d, f)

# Cell

def yaml_to_dict(file: Union[str, pathlib.Path]) -> dict:

    with open(file) as f:

        d = yaml.load(f, Loader=yaml.FullLoader)

    return d

# Cell

def write_multiple_categories(
        category_questions: Dict[str, List[dict]], pictures_base_directory: str, output_file: str = 'out.yaml') -> None:
    """
    Writes a file suitable as input to `gift-wrapper`.

    Parameters
    ----------
    category_questions : dict
        Every key is the name of a category, and every value is a list of questions
        (every question is itself a dictionary).
    pictures_base_directory : str
        The "pictures base directory" parameter that must be passed to `gift-wrapper`
    output_file : str
        Output file

    """

    file = dict()
    file['pictures base directory'] = pictures_base_directory
    file['categories'] = []

    for category_name, questions in category_questions.items():

        file['categories'].append({'name': category_name, 'questions': questions})

    dict_to_yaml(file, output_file)

# Cell

def supplement_file_name(file: Union[str, pathlib.Path], sup: str) -> pathlib.Path:
    """
    Adds a string between the file name in a path and the suffix.

    Parameters
    ----------
    file : str
        File name
    sup : str
        String to be added

    Returns
    -------
    out: pathlib.Path
        "Supplemented" file

    """

    file = pathlib.Path(file)

    # the `suffix` is incorporated into the file name
    return file.with_name(file.stem + f'_{sup}' + file.suffix)

assert supplement_file_name('/a/b/quixote.tex', 'foo') == pathlib.Path('/a/b/quixote_foo.tex')

# Cell

def add_name(questions: List[dict], base_name: str) -> List[dict]:
    """
    Adds a name to every question based on a pattern.

    Parameters
    ----------
    questions : list
        List of questions; every question is a dictionary.
    question_base_name : str
        All the questions will be given this name and a different (Roman) number.

    Returns
    -------
    out: list
        List with the same questions after adding the corresponding name to each one.

    """

    res = []

    for i_q, q in enumerate(questions):

        res.append({**q, 'name': f'{base_name} {int_to_roman(i_q + 1)}'})

    return res

assert add_name([{'k1': 'aa', 'k2': 1}, {'k3': 'pi', 'foo': 'variance'}], 'Viterbi') == [
    {'k1': 'aa', 'k2': 1, 'name': 'Viterbi I'}, {'k3': 'pi', 'foo': 'variance', 'name': 'Viterbi II'}]

# Cell

def wrong_numerical_solutions_from_correct_one(
    solution: float, n: int, min_sep: float, max_sep: float, lower_bound: float = -np.inf,
    upper_bound: float = np.inf, precision: int = 4, to_str: bool = True, fixed_point_format: bool = False,
    bin_width: Optional[float] = None, unique: bool = False, prng: np.random.RandomState = np.random.RandomState(42)
) -> Union[List[float], List[str]]:
    """
    Generates random numerical wrong answers given the correct one.


    Parameters
    ----------
    solution: float
        The actual solution.
    n: int
        The number of wrong solutions.
    min_sep: float
        Minimum separation.
    max_sep: float
        Maximum separation.
    lower_bound: float, optional
        A lower bound on the returned numbers.
    upper_bound: float, optional
        A upper bound on the returned numbers.
    precision: int, optional
        The number of decimal places.
    to_str: bool, optional
        If True, every element in the result will be converted to a string.
    fixed_point_format: bool
        Only meaningful when to_str is True. In such case, if True a fixed-point format (f) is used
        regardless of the actual type.
    bin_width: float, optional
        The granularity on the answers: every one will be a multiple of this parameter.
    unique: bool, optional
        If True, all the answers will be different.
    prng: RandomState, optional
        A pseudo-random numbers generator.

    Returns
    -------
    out: list of float, or list of str
        The random wrong solutions.

    """

    max_iterations = 1_000

    # in the current implementation all the answers are generated by pivoting around the solution; in order to prevent the correct solution being approximately in the middle, more wrong answers than requested are generated and, in the end, the requested number is randomly picked
    n_generated = n + 2

    assert (solution - min_sep > lower_bound) or (solution + min_sep < upper_bound)

    if bin_width:

        assert bin_width < (max_sep - min_sep)

    res = []

    # this acts as "pivot" to get to new values around
    current = solution

    for i in range(max_iterations):

        if bin_width:

            candidates = np.arange(min_sep, max_sep, bin_width)
            steps = prng.choice(candidates, size=2).round(precision)

        else:

            # one number to be added to the `current` solution and one to be subracted
            steps = prng.uniform(min_sep, max_sep, size=2)

        next_values = [v.round(precision)
                       for v in [current + steps[0], current - steps[1]] if lower_bound < v < upper_bound]
        if unique:

            next_values = [e for e in next_values if e not in set(res)]

        res.extend(next_values)

        # TODO: `current` *should* be modified so that the results are less centered around the correct solution (it reveals information!!) but with the current implementation it's hard to do while honoring the minimum and maximum separations
#         # this sort of adds entropy
#         current = np.median(res + [solution])

        if len(res) >= n:

            break

    else:

        raise Exception(f"Parameters are too much constraining, can't find the solution after {max_iterations}")

    if to_str:

        format_specifier = f'.{precision}{"f" if fixed_point_format else "g"}'

#         res = [str(e) for e in res]
        res = [f'{e:{format_specifier}}' for e in res]

#     return res[:n]
    return prng.choice(res, n, replace=False).tolist()