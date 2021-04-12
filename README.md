# py2gift
> Write GIFT (Moodle-compatible quizzes) files using Python.


`py2gift` is a library meant to write [question banks](https://docs.moodle.org/38/en/Question_bank) in [GIFT](https://docs.moodle.org/38/en/GIFT_format) format ([Moodle](https://moodle.org/)) *programmatically* in Python. Ultimately, questions can be written (though this is not a requirement) from a [Jupyter](https://jupyter.org/) notebook. The advantages are:

* you can use all your Python skills to *compute* whatever is required for the statement, solution and feedback of a question
* it makes easy to write different (random) versions of the same question
* questions can be previewed (pictures, $\LaTeX$...) in the notebook
* no need to install anything: you can click this mybinder badge, 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/manuvazquez/py2gift/master?filepath=examples)
, open any of the provided examples, and start writing your questions right now from the browser (the file generated at the end of the notebook, accesible through a link, can be imported in *Moodle*).

This library relies on [gift-wrapper](https://github.com/manuvazquez/gift-wrapper) and it has been created using [nbdev](https://github.com/fastai/nbdev). The latter fact means you can [explore the *actual* source code](https://manuvazquez.github.io/py2gift/) through jupyter notebooks and see the inner workings of each individual piece.

## Setup

Since the library is in [PyPI](https://pypi.org/project/py2gift/)

```
pip install py2gift
```

should do.

### Manual

If you'd rather clone this repository, the command below should install all the required packages 

```
pip install pandas numpy matplotlib ruamel.yaml gift-wrapper
```

## How to use it

Writing a question involves specifying the statement and, *optionally*, the feedback in different notebook cells. In any case, *variables*, specified with the prefix `!`, can be included, and those are meant to be *filled in* from within a Python class. This comes very handy when you want to create different versions of a single question in which some input data (maybe in the form of a picture) *randomly* changes from question to question. Then, you can instruct `py2gift` to call your Python code a number of times, each one giving rise to a different version of the same question (as long as some *variable* is set at random, e.g., by exploiting the functionality in `np.random`). The solution, whose format depends on the question type, must also be set from within the code.

Underneath, images are handled by *gift-wrapper*, and hence *paths* (e.g., `images/scheme.svg`) to either `.tex` (that can be compiled with *pdflatex*) or `.svg` files can be included in the statement, solution or feedback of a question. Moreover, they can be included through one of the variables (prefix `!`), and hence random (but nonetheless meaningful) pictures are a possibility.

Notice that the difference between two instances of the same question can be minor or significant. Ultimately, it depends on how sophisticated your Python code is (if the latter can solve the question/problem in a very general form, and you are also able to present it in the `statement`, then it is fine).

Besides the above mentioned *core* functionality, `py2gift` provides some extra functions to ease the process of writing questions (modules `tex`, `util`, `time`, `hash`). However, a thorough description of the functionality would be very dry and you are probably better off by taking a look at one of the *sample* notebooks ([minimal](examples/minimal.ipynb) or [example_1](examples/example_1.ipynb)). Also, you can take a look at the [documentation](https://manuvazquez.github.io/py2gift/).
