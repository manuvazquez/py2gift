# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['main', 'init_parameters_from_settings', 'build_question', 'build']

# Cell

import sys
import argparse
import pathlib
import subprocess
import importlib.util
import string
import collections
from types import ModuleType

import yaml
from py2gift import util
from py2gift import question

# Cell

def main():

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

# Cell

def init_parameters_from_settings(settings: dict) -> dict:

    init_parameters = {
        'unprocessed_statement': string.Template(settings['statement']),
        'unprocessed_feedback': string.Template(settings['feedback'])
    }

    init_parameters.update(settings.get('init parameters', {}))

    return init_parameters

# Cell

def build_question(question_generator: question.QuestionGenerator, category_name: str, settings: dict) -> dict:

    class_name = question_generator.__name__

    class_settings = util.extract_class_settings(category_name, class_name, settings)

    # an instance
    question_generator = question_generator(**init_parameters_from_settings(class_settings))

    assert ('parameters' in class_settings) ^ ('number of instances' in class_settings), 'either "parameters" or "number of instances" must be specified'

    if 'parameters' in class_settings:
        return question_generator(**class_settings['parameters'])
    else:
        return question_generator()

# Cell

def build(input_file: str, local_run: bool, questions_module: ModuleType):

    with open(input_file) as f:

        settings = yaml.load(f, Loader=yaml.FullLoader)

    output_file = settings['output file']
    executable = pathlib.Path(settings['path to gift-wrapper']).expanduser()

    category_questions = collections.defaultdict(list)

    for cat in settings['categories']:

        questions = []

        for c in cat['classes']:

            this_class_questions = []

            assert ('parameters' in c) ^ ('number of instances' in c), 'either "parameters" or "number of instances" must be specified'

            question_generator = getattr(questions_module, c['name'])(**init_parameters_from_settings(c))

            if 'parameters' in c:

                for p in c['parameters']:

                    this_class_questions.append(question_generator(**p))

            else:

                for _ in range(c['number of instances']):

                    this_class_questions.append(question_generator())

            questions.extend(util.add_name(this_class_questions, base_name=c['question base name']))

        category_questions[cat['name']].extend(questions)

    # --------

    util.write_multiple_categories(category_questions, settings['pictures base directory'], output_file=output_file)

    command = [executable.as_posix()]

    # if "local" running was requested...
    if local_run:

        command.append('-l')

    command.extend(['-i', output_file])

    run_summary = subprocess.run(command, capture_output=True)

    assert run_summary.returncode == 0, f'"gift-wrapper" finished abruptly ({run_summary.stderr})'