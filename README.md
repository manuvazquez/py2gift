# py2gift
> Write Moodle quizzes from a Jupyter notebook.


`py2gift` is a library meant to write [question banks](https://docs.moodle.org/38/en/Question_bank) in [GIFT](https://docs.moodle.org/38/en/GIFT_format) format ([Moodle](https://moodle.org/)) from within a [Jupyter](https://jupyter.org/) notebook. The advantages are:

* you can use all your Python skills to *compute* whatever is required for the statement, solution and feedback of a question
* it makes easy to write different (random) versions of the same question
* questions can be previewed (pictures, $\LaTeX$...) in the notebook
* no need to install anything!! You can (though don't have to) click this mybinder link and start writing your questions right now from the browser.

This library relies [gift-wrapper](https://github.com/manuvazquez/gift-wrapper) and it has been created using [nbdev](https://github.com/fastai/nbdev). The latter fact means you can explore the *actual* source code through jupyter notebooks and see all the pieces in action.

# How to use it

Writing a question involves specifying the statement, the solution and, *optionally*, the feedback, each one on a different notebook *cell*. In every case *variables*, specified with the prefix `!` can be included, and those are meant to be *filled in* from within a Python class. This comes very handy when you want to create different versions of a single question in which some input data (maybe in the form of a picture) changes from question to question. Then, you can instruct `py2gift` to call your run your python code a number of times, each one giving rise to a different version of the same question.

Underneath, images are handled by *gift-wrapper*, and hence *paths* (e.g., `images/scheme.svg`) to either `.tex` (that can be compiled with *pdflatex*) or `.svg` files can be included in the statement, solution or feedback to a question. Moreover, they can be included through one of the variables (prefix `!`), and hence random (but nonetheless meaningful) pictures are a possibility.

Notice that the difference between two instances of the same question can be minor or significant. Ultimately, it depends on how sophisticated your Python code is (if the latter can solve the question/problem in a very general form, and you are also able to present it in the `statement`, then it is fine).

Beside the above mentioned *core* functionality, `py2gift` provides some extra functions to ease the process of writing questions (modules `tex`, `util`, `time`, `hash`). However, a thorough description of the functionality would be very dry and you are probably better off by taking a look at the *sample* notebook, [sample_1](sample_1.ipynb).
