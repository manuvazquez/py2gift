# AUTOGENERATED! DO NOT EDIT! File to edit: 03_question.ipynb (unless otherwise specified).

__all__ = ['TemplatedLatexText', 'QuestionGenerator', 'NumericalQuestionGenerator', 'MultipleChoiceQuestionGenerator',
           'MultipleChoiceTheoreticalQuestionGenerator']

# Cell

import abc
import string
import re
import pathlib
from typing import List, Union, Optional, Tuple

import numpy as np

# to avoid tqdm's experimental warning
import warnings
warnings.filterwarnings("ignore", message='Using `tqdm.autonotebook.tqdm` in notebook mode')

import py2gift.tex
import py2gift.util

# Cell
class TemplatedLatexText:

    wildcard_symbol = '!'

    type_to_processing_function = {
        type('string'): lambda x: x,
        type(pathlib.Path('foo')): lambda x: str(x),
        type(np.array([1,2])): py2gift.tex.from_matrix,
        type([1,2]): py2gift.tex.from_matrix,
        type(3): py2gift.tex.from_number,
        type(4.2): py2gift.tex.from_number,
        type(np.array([2, 3], dtype=int)[0]): py2gift.tex.from_number,
        type(np.array([2.0, 3.0], dtype=float)[0]): py2gift.tex.from_number
    }

    def __init__(self, raw_text: str) -> None:

        self.template = string.Template(self.pre_process(raw_text))

        try:

            # this is fine if there are no "placeholder"s that need to be substituted
            self._final = self.template.substitute()

        # if there are "placeholders" that need to be taken care of...
        except:

            self._final = None

    def pre_process(self, text: str) -> str:

        return text.replace('$', '$$').replace(self.wildcard_symbol, '$')

    def fill(self, **kwargs) -> None:

        processed_args = dict()

        for k,v in kwargs.items():

            # the type of the passed value
            t = type(v)

            assert t in self.type_to_processing_function, (
                f'the type of {k} ({t}) cannot be handled (turned into a string)')

            processed_args[k] = self.type_to_processing_function[t](v)


#         self._final = self.template.substitute(**kwargs)
        self._final = self.template.substitute(**processed_args)

    @property
    def final(self) -> str:

        assert self._final is not None, f'text has unfilled slots'

        return self._final

    def __repr__(self) -> str:

        if self._final:

            return self._final

        else:

            return f'un-filled template:\n{self.template.template}'

    @property
    def is_full(self) -> bool:

        return self._final is not None

# Cell

class QuestionGenerator(metaclass=abc.ABCMeta):

    def __init__(
        self, statement: TemplatedLatexText, feedback: TemplatedLatexText,
        time: Optional[int] = None, prng: np.random.RandomState = np.random.RandomState(42)) -> None:

        self.statement = statement
        self.feedback = feedback
        self.time = time
        self.prng = prng

    @property
    @abc.abstractmethod
    def class_name(self) -> str:

        pass

    # this is the method to be defined by the user
    @abc.abstractmethod
    def setup(self, **kwargs):

        pass

    def partially_assemble_question(self, statement: str, feedback: str) -> dict:

        question = dict()

        question['class'] = self.class_name
        question['statement'] = statement
        question['feedback'] = feedback

        if self.time:

            question['time'] = str(self.time)

        return question

    def __call__(self, **kwargs):

        # arguments are passed directly to `setup`
        self.setup(**kwargs)

        assert self.statement.is_full
        assert self.feedback.is_full

# Cell

class NumericalQuestionGenerator(QuestionGenerator):

    def __init__(
        self, statement: TemplatedLatexText, feedback: TemplatedLatexText,
        time: Optional[int] = None, prng: np.random.RandomState = np.random.RandomState(42)) -> None:

        super().__init__(statement, feedback, time, prng)

        self.solution = None
        self.error = None

    @property
    def class_name(self) -> str:

        return 'Numerical'

    def assemble_question(
        self, statement: str, feedback: str, solution: float, error: Optional[float] = None) -> dict:

        question = self.partially_assemble_question(statement, feedback)

        # some yaml "writers" (e.g., ruamel.yaml) don't play well with numpy floats
        if type(solution) == np.float64:

            solution = solution.item()

        question['solution'] = dict()
        question['solution']['value'] = solution

        if error is None:

            # 10% margin
            error = solution * 0.1

        question['solution']['error'] = error

        return question

    def __call__(self, **kwargs):

        super().__call__(**kwargs)

        assert self.solution is not None, 'solution was not defined, please try setting `self.solution` to a number'
        assert self.error is not None, (
            'error (tolerance) was not defined, please try setting `self.error` to a number')

        return self.assemble_question(
            statement=self.statement.final, feedback=self.feedback.final, solution=self.solution, error=self.error)

# Cell

class MultipleChoiceQuestionGenerator(QuestionGenerator):

    def __init__(
        self, statement: TemplatedLatexText, feedback: TemplatedLatexText,
        time: Optional[int] = None, prng: np.random.RandomState = np.random.RandomState(42)) -> None:

        super().__init__(statement, feedback, time, prng)

        self.right_answer = None
        self.wrong_answers = None

    @property
    def class_name(self) -> str:

        return 'MultipleChoice'

    def assemble_question(
            self, statement: str, feedback: str, perfect_answer: str,
            wrong_answers: Union[List[str], List[Tuple[str, float]]]) -> dict:

        question = self.partially_assemble_question(statement, feedback)

        question['answers'] = dict()

        if self.right_answer:

            question['answers']['perfect'] = perfect_answer

        question['answers']['wrong'] = wrong_answers

        return question

    def __call__(self, **kwargs):

        super().__call__(**kwargs)

        if self.right_answer:

            assert isinstance(self.right_answer, str), f'right answer "{self.right_answer}" is not a string'

        assert self.wrong_answers is not None, (
            'wrong answers were not given, please try setting `self.wrong_answers` to a list of strings')

        # in order to check that every wrong answer is different
        wrong_answers_texts = []

        for e in self.wrong_answers:

            assert isinstance(e, str) or isinstance(e, list), (
                f'"{e}" is not a string or list encompassing a string and a number')

            if isinstance(e, list):

                wrong_answers_texts.append(e[0])

                assert isinstance(e[0], str)
                assert isinstance(e[1], int) or isinstance(e[1], float)

            else:

                wrong_answers_texts.append(e)

        # all the answers are different
        assert np.unique(wrong_answers_texts).size == np.array(wrong_answers_texts).size, (
            f'all the wrong answers are not different: {wrong_answers_texts}')


        return self.assemble_question(
            statement=self.statement.final, feedback=self.feedback.final, perfect_answer=self.right_answer,
            wrong_answers=self.wrong_answers)

# Cell

class MultipleChoiceTheoreticalQuestionGenerator(MultipleChoiceQuestionGenerator):

    def setup(self, right_answer: str, wrong_answers: List[str]):

        self.statement = self.unprocessed_statement.safe_substitute()
        self.feedback = self.unprocessed_feedback.safe_substitute()

        self.right_answer = right_answer
        self.wrong_answers = wrong_answers