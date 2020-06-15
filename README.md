# py2gift
> Write <a href='https://jupyter.org/'>Moodle](https://moodle.org/) quizzes from a [Jupyter</a> notebook.


`py2gift` is a library meant to write [question banks](https://docs.moodle.org/38/en/Question_bank) in [GIFT](https://docs.moodle.org/38/en/GIFT_format) format from within a Jupyter notebook. The advantages are:

* you can use all your Python skills to *compute* whatever is required for the statement, solution and feedback of a question
* it makes easy to write different (random) versions of the same question
* questions can be previewed (pictures, $\LaTeX$...) in the notebook
* no need to install anything!! You can (though don't have to) click this mybinder link and start writing your questions right now from the browser.

This library is meant as a *companion* for [gift-wrapper](https://github.com/manuvazquez/gift-wrapper). The latter is meant to
> Build GIFT (Moodle compatible) files easily

but still you need to write the questions *by hand*. This library encompasses some utilities to ease the process. The ultimate goal is to write the exams in [jupyter](https://jupyter.org/) notebooks.
It has been created using [nbdev](https://github.com/fastai/nbdev).

# Give it a try

## Install

`pip install py2gift`

## How to use

Fill me in please! Don't forget code examples:

```python
1+1
```

The images are underneath handled by *gift-wrapper*, and hence either `.tex` (that can be compiled with *pdflatex*) or `.svg` files are fine.

The difference between two instances of the same question can be minor or significant. Ultimately, it depends on how sophisticated your Python code is (if the latter can solve the question/problem in a very general form, and you are also able to present it in the `statement`, you are good to go).
