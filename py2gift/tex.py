# AUTOGENERATED! DO NOT EDIT! File to edit: 01_tex.ipynb (unless otherwise specified).

__all__ = ['mathfy_and_join', 'gaussian_pdf', 'q_function_approximation', 'mutual_information', 'from_number',
           'from_matrix', 'dot_product', 'total_probability', 'enumerate_math', 'enumerate_assignments', 'expand']

# Cell

from typing import Union, Iterable, List, Optional

import numpy as np

from .util import to_formula_maybe

# Cell

def mathfy_and_join(strings_list: List[str], nexus: str = 'and'):

    return '$' + '$, $'.join(strings_list[:-1]) + f'$ {nexus} ${strings_list[-1]}$'

# Cell

@to_formula_maybe
def gaussian_pdf(x: str = 'x', mean: str = r'\mu', variance: str = r'\sigma^2') -> str:
    """
        Returns a string representing the probability density function for a Gaussian distribution.
    """

    return r'\frac{1}{\sqrt{2\pi ' + variance + r'}}e^{-\frac{(' + x + '-' + mean + r')^2}{2' + variance + r'}}'

# Cell

@to_formula_maybe
def q_function_approximation(x: str = 'x') -> str:
    """
    Returns a string representing the Stirling approximation.
    """

    return f'Q({x}) \\approx \\frac{{1}}{{2}} e^{{-\\frac{{{x}^2}}{{2}}}}'

# Cell

@to_formula_maybe
def mutual_information(X: str = 'X', Y: str = 'Y') -> str:

    return f'I({X},{Y}) = H({Y}) - H({Y}|{X})'

# Cell

@to_formula_maybe
def from_number(n: Union[int, float], prefix: str = '', precision: int = 3) -> str:
    """
    Returns a string for a given number.
    """

    if (type(n) == float) or (type(n) == np.float64):

        format_specifier = f'.{precision}f'

        return f'{prefix}{n:{format_specifier}}'

    else:

        return f'{n}'

# Cell

@to_formula_maybe
def from_matrix(m: Union[list, np.ndarray], float_point_precision: int = 3) -> str:
    """
    Returns a string for a given array or matrix.
    """

    format_from_number = lambda x: f'.{float_point_precision}f' if (type(x) == np.float64) or (type(x) == float) else f'd'

    if isinstance(m[0], (list, np.ndarray)):

        return r'\begin{bmatrix}' + r' \\ '.join(
            [(r' & '.join([f'{e:{format_from_number(m[0][0])}}' for e in row])) for row in m]) + r'\end{bmatrix}'

    else:

        return r'\begin{bmatrix}' + r' & '.join([f'{e:{format_from_number(m[0])}}' for e in m]) + r'\end{bmatrix}'

# Cell

@to_formula_maybe
def dot_product(lhs_template: str, lhs: list, rhs_template: str, rhs: list, nexus: str = 'and', product_operator = '',precision: int = 3, start_at_zero: bool = False) -> str:

    return '+'.join([lhs_template.format(l) + product_operator + rhs_template.format(r) for l,r in zip(lhs, rhs)])

# Cell

@to_formula_maybe
def total_probability(fixed_symbol: str, varying_symbol_template: str, n: int, start_at_zero: bool = False) -> str:

    start = int(not start_at_zero)

    return '+'.join([f'p({fixed_symbol},{varying_symbol_template.format(i)})' for i in range(start, start+n)])

# Cell

def enumerate_math(
    numbers_list: List[float], assigned_to: Optional[str] = None, nexus: str = 'and', precision: int = 3) -> str:
    """
    Returns a string for a enumeration of formulas.
    """

    format_specifier = f'.{precision}f'

    strings_list = [f'{e:{format_specifier}}' for e in numbers_list]

    if assigned_to:

        strings_list = [assigned_to.format(i_s+1) + ' = ' + s for i_s, s in enumerate(strings_list)]

    return mathfy_and_join(strings_list, nexus=nexus)

# Cell

def enumerate_assignments(
    lhs_template: str, rhs_template: str, rhs: List[float], nexus: str = 'and', precision: int = 3, start_at_zero: bool = False) -> str:
    """
    Returns a string for a enumeration of formulas.
    """

#     format_specifier = f'.{precision}f'
#     breakpoint()

    return mathfy_and_join([f'{lhs_template} = {rhs_template}'.format(i+int(not start_at_zero), r) for i, r in enumerate(rhs)])

# Cell

def expand(template: str, n: int, to_math: bool = False, nexus: str = 'and') -> str:
    """
    Expand a symbol according to a pattern.

    >>> util.expand('s_{}', 3, True)
    '$s_1$, $s_2$ and $s_3$'

    Parameters
    ----------
    template : str
        String with a *single* replacement field ({})
    n : int
        Requested number of terms
    to_math : bool
        If `True`, every output term is enclosed between $'s
    nexus : str
        String joining the second to last and last terms.

    Returns
    -------

    """

    res = [template.format(i) for i in range(1, 1 + n)]

    if to_math:

        res = [f'${e}$' for e in res]

    return ', '.join(res[:-1]) + f' {nexus} {res[-1]}'

assert expand('s_{}', 3, True) == '$s_1$, $s_2$ and $s_3$'