# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['main', 'init_parameters_from_settings', 'build', 'build_question', 'generator_to_markdown', 'latex_to_markdown']

# %% ../nbs/00_core.ipynb 5
import sys
import argparse
import pathlib
import importlib.util
import string
import collections
from types import ModuleType

import numpy as np
import yaml

import py2gift.util
import py2gift.question
import py2gift.input_file

import gift_wrapper.core
import gift_wrapper.question

# some classes in `gift_wrapper.question` are "patched" when this module is imported
import py2gift.markdown

# %% ../nbs/00_core.ipynb 8
def main():
    "Parses command-line arguments to be passed to `build`"
    
    parser = argparse.ArgumentParser(description='Python to GIFT converter')

    parser.add_argument(
        'input_file', type=argparse.FileType('r'), default='global_settings.yaml', help='settings file', nargs='?')

    parser.add_argument('-c', '--code_directory', default='.', help='directory with the required source code')

    parser.add_argument(
        '-m', '--main_module', default='questions.py', help='file with the questions generators')

    parser.add_argument(
        '-l', '--local', default=False, action='store_true', help="don't try to copy the images to the server")

    command_line_arguments = parser.parse_args()
    
    code_directory = pathlib.Path(command_line_arguments.code_directory)
    main_module = pathlib.Path(command_line_arguments.main_module)

    sys.path.insert(0, code_directory.absolute().as_posix())
    spec = importlib.util.spec_from_file_location(main_module.stem, (code_directory / main_module).absolute())
    questions_generators = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(questions_generators)
    
    build(command_line_arguments.input_file.name, command_line_arguments.local, questions_generators)

# %% ../nbs/00_core.ipynb 11
def init_parameters_from_settings(
    cls_settings: dict # Settings for the class, which should include `statement`, `feedback` and, optionally, `time`
) -> dict: # *Exact* parameters that must be passed when instantiating the class.
    "Returns a dictionary with the initialization parameters for a question"

    init_parameters = {
        'statement': py2gift.question.TemplatedLatexText(cls_settings['statement']),
        'feedback': py2gift.question.TemplatedLatexText(cls_settings['feedback'])
    }
    
    if 'time' in cls_settings:
        
        init_parameters['time'] = cls_settings['time']

    init_parameters.update(cls_settings.get('init parameters', {}))
    
    return init_parameters

# %% ../nbs/00_core.ipynb 25
def build(
    settings: str | dict, # Settings for all the questions (generators)
    local_run: bool, # If `True`, pictures will not be copied to a remote host
    questions_module: ModuleType, # A module or structure to hold the classes referenced in the settings
    parameters_file: str | dict = 'parameters.yaml', # Parameters to be passed to "gift-wrapper"
    no_checks: bool = False, # If `True` LaTeX formulas are not be checked
    embed_images: bool = False # If `True`, images will be embedded in the questions (rather than linked)
) -> None:
    "Generates a GIFT file"
    
    # if settings is the name of a file...
    if type(settings) == str:

        with open(settings) as f:

            settings = yaml.load(f, Loader=yaml.FullLoader)
    
    else:
        
        assert type(settings) == dict

    output_file = settings['output file']

    category_questions = collections.defaultdict(list)

    for cat in settings['categories']:

        questions = []

        for c in cat['classes']:

            this_class_questions = []
            
            # either `parameters` or `number of instances` is present, but not both
            assert ('parameters' in c) ^ ('number of instances' in c), (
                'either "parameters" or "number of instances" must be specified')
            
            question_generator = getattr(questions_module, c['name'])(**init_parameters_from_settings(c))
            
            if 'parameters' in c:

                for p in c['parameters']:

                    this_class_questions.append(question_generator(**p))
            
            else:
                
                for _ in range(c['number of instances']):
                    
                    this_class_questions.append(question_generator())

            questions.extend(py2gift.util.add_name(this_class_questions, base_name=c['question base name']))
        
        category_questions[cat['name'] if type(cat['name']) != list else tuple(cat['name'])].extend(questions)

    # --------

    py2gift.util.write_multiple_categories(
        category_questions, settings['pictures base directory'], output_file=output_file)
    
    gift_wrapper.core.wrap(
        parameters_file, output_file, local_run=local_run, no_checks=no_checks, embed_images=embed_images)

# %% ../nbs/00_core.ipynb 47
def build_question(
    question_generator: py2gift.question.QuestionGenerator, # The question generator that will generate the appropirate settings
    category_name: str, # The name of category the class belongs to
    settings: dict, # User settings
    n_question: int = 0 # The number of instances to be returned
) -> dict: # Settings that allow building the question using "gift-wrapper"
    'Returns the settings for building a question using "gift-wrapper"'
    
    class_name = question_generator.__name__
    
    class_settings = py2gift.input_file.extract_class_settings(category_name, class_name, settings)
    
    # an instance
    question_generator = question_generator(**init_parameters_from_settings(class_settings))

    assert ('parameters' in class_settings) ^ ('number of instances' in class_settings), (
        'either "parameters" or "number of instances" must be specified')

    if 'parameters' in class_settings:
        # notice that `parameters` yields a list
        return question_generator(**class_settings['parameters'][n_question])
    else:
        return question_generator()

# %% ../nbs/00_core.ipynb 60
def generator_to_markdown(
    settings: str | pathlib.Path | dict, # Settings
    category: str, # Category of the question
    cls: py2gift.question # Class implementing the generator
) -> str: # Markdown text
    "Returns markdown text from a generator"
    
    # if settings is the name of a file...
    if type(settings) == str:
        
        settings = py2gift.util.yaml_to_dict(settings)
    
    else:
        
        assert type(settings) == dict

    question_settings = build_question(cls, category, settings)

    return py2gift.markdown.settings_to_markdown(question_settings)

# %% ../nbs/00_core.ipynb 64
def latex_to_markdown(
    input_file: str | pathlib.Path, # TeX file
    delete_input_file_afterwards: bool = False # If `True` the TeX file is deleted after conversion to svg
) -> str: # Markdown text
    "Returns markdown text that shows the result of compiling a TeX file"
    
    output_file = gift_wrapper.image.pdf_to_svg(gift_wrapper.image.tex_to_pdf(input_file))
    
    suffixes = ['.aux', '.log', '.pdf']
    
    if delete_input_file_afterwards:
        
        suffixes.append('.tex')
    
    for suffix in suffixes:
        
        file_to_delete = output_file.with_suffix(suffix)
        
        if file_to_delete.exists():
        
            file_to_delete.unlink()
    
    return r'![](' + output_file.as_posix() + ')'
