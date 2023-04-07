# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/10_tex.ipynb.

# %% auto 0
__all__ = ['to_formula_maybe', 'join', 'gaussian_pdf', 'q_function_approximation', 'partwise_function', 'from_number',
           'from_matrix', 'dot_product', 'total_probability', 'enumerate_math', 'enumerate_assignments', 'expand']

# %% ../nbs/10_tex.ipynb 5
import functools
from typing import Iterable, Callable, Any

import numpy as np

from .util import render_latex

# %% ../nbs/10_tex.ipynb 8
def to_formula_maybe(
    func: Callable[..., Any] # Function returning a string
) -> str: # $\LaTeX$ formula
    "Decorator for adding the argument `to_formula` to any function"
    
    def wrapper(*args, **kwargs):
        
        if ('to_formula' in kwargs) and (kwargs['to_formula']):
            
            kwargs.pop('to_formula')
            
            return f'${func(*args, **kwargs)}$'
        
        else:
            
            if ('to_formula' in kwargs):
            
                # it must also be popped out
                kwargs.pop('to_formula')
            
            return func(*args, **kwargs)
        
    functools.update_wrapper(wrapper, func)
        
    return wrapper

# %% ../nbs/10_tex.ipynb 26
def join(
    strings_list: list[str], # Strings to be joined
    nexus: str = ' and ', # Text between the second to last and last elements
    to_formula: bool = True # If `True` every string will be enclosed in \$s
) -> str: # $\LaTeX$-compatible text
    "Enumerates the strings in a list, optionally enclosing every element between $s"
    
    if to_formula:
        
        delimiter = '$'
    
    else:
        
        delimiter = ''
    
    return delimiter + \
        f'{delimiter}, {delimiter}'.join(strings_list[:-1]) +\
        f'{delimiter}{nexus}{delimiter}{strings_list[-1]}{delimiter}'

# %% ../nbs/10_tex.ipynb 35
@to_formula_maybe
def gaussian_pdf(
    x: str | None = 'x', # The random variable
    mean: str | None = r'\mu', # The mean of the random variable
    variance: str | None = r'\sigma^2' # The variance of the random variable
) -> str: # $\LaTeX$-compatible text
    "Returns a string representing the probability density function for a Gaussian distribution"

    return r'\frac{1}{\sqrt{2\pi ' + variance + r'}}e^{-\frac{(' + x + '-' + mean + r')^2}{2' + variance + r'}}'

# %% ../nbs/10_tex.ipynb 41
@to_formula_maybe
def q_function_approximation(
    x: str | None = 'x' # The argument of the Q function
) -> str: # $\LaTeX$-compatible text
    "Returns a string representing the Stirling approximation for the Q function"

    return f'Q({x}) \\approx \\frac{{1}}{{2}} e^{{-\\frac{{{x}^2}}{{2}}}}'

# %% ../nbs/10_tex.ipynb 47
@to_formula_maybe
def partwise_function(
    function: str, # The name of the function
    parts: list[tuple[str, str]], # Each element is a tuple yields whose 1st element is the value of the function and whose second is a condition stating where the 1st applies
    add_zero_otherwise: bool | None = True # If `True`, one last part stating "0, otherwise" is added
) -> str: # $\LaTeX$-compatible text
    "Returns a string representing the definition a part-wise mathematical function"
    
    res = f'{function}='
    
    res += '\\begin{cases}\n'
    
    for p in parts:
    
        res += f'{p[0]},& {p[1]} \\\\'
    
    if add_zero_otherwise:
        
        res += r'0,& \text{otherwise}'
    
    res += r'\end{cases}'
    
    return res

# %% ../nbs/10_tex.ipynb 53
@to_formula_maybe
def from_number(
    n: int | float, # The number
    prefix: str | None = '', # A string to be prepended to the number
    precision: int | None = 3, # Number of decimals if `fixed_point_format` is `True`, overall number of figures otherwise (ignored if the number is an integer)
    fixed_point_format: bool | None = False # If `True`, a fixed-point format (`f`) is used regardless of the actual type
) -> str: # $\LaTeX$-compatible text
    "Returns a string for a given number"
    
    format_specifier = f'.{precision}{"f" if fixed_point_format else "g"}'

    return f'{prefix}{n:{format_specifier}}'

# %% ../nbs/10_tex.ipynb 68
@to_formula_maybe
def from_matrix(
    m: list | np.ndarray, # Matrix or vector
    float_point_precision: int = 3 # Number of decimals (ignored if the number is an integer)
) -> str: # $\LaTeX$-compatible text
    "Returns a string for a given array or matrix"
    
    format_from_number = lambda x: f'.{float_point_precision}g' if (type(x) == np.float64) or (type(x) == float) else f'd'

    if isinstance(m[0], (list, np.ndarray)):

        return r'\begin{bmatrix}' + r' \\ '.join(
            [(r' & '.join([f'{e:{format_from_number(m[0][0])}}' for e in row])) for row in m]) + r'\end{bmatrix}'

    else:
        
        return r'\begin{bmatrix}' + r' & '.join([f'{e:{format_from_number(m[0])}}' for e in m]) + r'\end{bmatrix}'

# %% ../nbs/10_tex.ipynb 81
@to_formula_maybe
def dot_product(
    lhs_template: str, # Left-hand side template; it should include a replacement field ({}) that will be replaced by one of the elements in `lhs`
    lhs: list, # Left-hand side elements
    rhs_template: str, #  Right-hand side template; it should include a replacement field ({}) that will be replaced by one of the elements in `rhs`
    rhs: list, # Right-hand side elements
    product_operator: str | None = '', # Symbol to be used as product operator
    addition_operator: str | None = '+' # Symbol to be used as addition operator
) -> str: # $\LaTeX$-compatible text
    "Returns a string for the dot product of two vectors, regardless of whether they are symbols or numbers"

    
    return addition_operator.join([lhs_template.format(l) + product_operator + rhs_template.format(r) for l,r in zip(lhs, rhs)])

# %% ../nbs/10_tex.ipynb 85
@to_formula_maybe
def total_probability(
    fixed_symbol: str, # The symbol that stays the same in the summation
    varying_symbol_template: str, # A template for the varying symbol that includes a replacement field (`{}`) for the index
    n: int, # The number of values for the varying symbol
    start_at: int = 1 # The index at which `varying_symbol_template`starts
) -> str: # $\LaTeX$-compatible text
    "Returns a string for law of total probability"
    
    return '+'.join([f'p({fixed_symbol},{varying_symbol_template.format(i)})' for i in range(start_at, start_at+n)])

# %% ../nbs/10_tex.ipynb 90
def enumerate_math(
    numbers_list: list[float], # The elements to be enumerated
    assigned_to: str | None = None, # Some text with a replacement field (this means that any { or } must be escaped by doubling it)
    nexus: str | None = ' and ', # The text joining the second to last and last elements
    precision: int | None = 3, # The number of decimal places
    start_at: int | None = 1 # The index of the first element that enters the enumeration
) -> str: # $\LaTeX$-compatible text
    "Builds a $\TeX$ string from a list of numbers in which each one is printed after (optionally) being assigned to an indexed variable that follows a given pattern"

    format_specifier = f'.{precision}g'

    strings_list = [f'{e:{format_specifier}}' for e in numbers_list]

    if assigned_to:

        strings_list = [assigned_to.format(i_s) + ' = ' + s for i_s, s in enumerate(strings_list, start_at)]
    
    return join(strings_list, nexus=nexus)

# %% ../nbs/10_tex.ipynb 98
def enumerate_assignments(
    lhs_template: str, # Text with a replacement field that will be replaced by an index
    rhs_template: str, # Text with a replacement field that will be replaced by one of the corresponding elements in rhs
    rhs: list[float], # Elements to be enumerated
    nexus: str = ' and ', # The text joining the second to last and last elements
    precision: int = 3, # The number of decimal places
    start_at: int = 1 # The index of the first element that enters the enumeration
) -> str: # $\LaTeX$-compatible text
    "Constructs a enumeration of assignments from left-hand-side and right-hand-side templates and right-hand-side values. It's similar to `enumerate_math` when the argument `assigned_to` is passed to the latter, but more general since the right-hand expression is also obtained from a template"
    
    return join([f'{lhs_template} = {rhs_template}'.format(i, r) for i, r in enumerate(rhs, start_at)], nexus=nexus)

# %% ../nbs/10_tex.ipynb 103
def expand(
    template: str, # String with a *single* replacement field ({})
    n: int, # Requested number of terms
    to_math: bool = False, # If `True`, every output term is enclosed between \$'s
    nexus: str = ' and ', # String joining the second to last and last terms
    start_at: int = 1 # The number at which indexes start
) -> str: # $\LaTeX$-compatible text
    "Expand a symbol according to a pattern"
    
    return join([template.format(i) for i in range(start_at, start_at + n)], nexus=nexus, to_formula=to_math)

assert expand('s_{}', 3, True) == '$s_1$, $s_2$ and $s_3$'
