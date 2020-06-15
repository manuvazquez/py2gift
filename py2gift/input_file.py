# AUTOGENERATED! DO NOT EDIT! File to edit: 40_input_file.ipynb (unless otherwise specified).

__all__ = ['extract_class_settings', 'Settings', 'initialize', 'set_class_preamble', 'set_class_closing', 'set_class',
           'write_header', 'write_class_preamble', 'write_class_closing', 'function_to_make_hierarchical_category_name']

# Cell

import sys
import pathlib
import pprint
import inspect
from typing import Union, Optional, Callable, List

import py2gift.util

import yaml

# Cell

def extract_class_settings(category_name: Union[str, list], class_name: str, settings: dict):

    category_found = False

    for cat in settings['categories']:

        if cat['name'] == category_name:

            category_found = True

            for cls in cat['classes']:

                if cls['name'] == class_name:

                    return cls

    else:

        if category_found:

            print(f'cannot find the requested class, {class_name}')
            sys.exit(1)

        else:

            print(f'cannot find the requested category, {category_name}')
            sys.exit(1)

# Cell

class Settings:

    def __init__(self, output_file: str = 'quiz.yaml', pictures_directory: str = 'quiz/pics', test_mode: bool = False) -> None:

        self.test_mode = test_mode

        self.store = {}

        self.store['output file'] = output_file
        self.store['pictures base directory'] = pictures_directory
        self.store['categories'] = None

        self._classes = set()

    def to_dict(self) -> dict:

        return self.store

    def __repr__(self) -> str:

        return pprint.pformat(self.store)

    @property
    def fake_module(self) -> 'ClassesContainer':

        # [0] is the caller of the method (`stack`)
        caller_globals = inspect.stack()[1].frame.f_globals

        class ClassesContainer:

            pass

        class_container = ClassesContainer()

        for c in self._classes:

#             assert c in globals(), f'class "{c}" was not defined'
            assert c in caller_globals, f'class "{c}" was not defined'

#             setattr(class_container, c, globals()[c])
            setattr(class_container, c, caller_globals[c])

        return class_container


    def add_category(self, category_name: str, base_category: Optional[str] = None) -> Union[str, List[str]]:
        """
        Adds a category if it doesn't exist.

        Parameters
        ----------
        category_name: str
            The name of the category to be added.
        base_category: str, optional
            Parent of the category

        Returns
        -------
        out: str or list of str
            The category *actually* added.

        """

        assert type(category_name) == str

        if self.test_mode:

            category_name = 'test'

        else:

            if base_category:

                category_name = [base_category, f'{base_category}/{category_name}']


        if self.store['categories'] is None:

            self.store['categories'] = []

        # only if the category doesn't exist...
        if self.locate(category_name=category_name) is None:

            # ...is it added
            self.store['categories'].append({'name': category_name, 'classes': None})

        return category_name

    def locate(self, category_name: Union[str, list], class_name: Optional[str] = None) -> dict:
        """
        Returns the requested category or class (inside a category) or `None` if it can't be found.

        Parameters
        ----------
        category_name: str
            The name of the category.
        class_name: str, optional
            The name of the class.

        Returns
        -------
        out: dict
            The dictionary for the category or class.

        """

        for cat in self.store['categories']:

            if cat['name'] == category_name:

                # if no particular class was requested...
                if class_name is None:

                    return cat

                # if a particular class was requested...
                else:

                    # the found category is saved for use below
                    category_settings = cat

                    # this is the only way out of the loop without return
                    break

        else:

            return None


        # at this point the category has been found and `class_name` is not `Ǹone`

        # if the category doesn't have any class...
        if category_settings['classes'] is None:

            return None

        for cls in category_settings['classes']:

            if cls['name'] == class_name:

                return cls

        else:

            return None

    def add_or_update_class(
        self, category_name: Union[str, list], class_name: str, question_base_name: str,
        init_parameters: Optional[dict] = None, parameters: Optional[List[dict]] = None,
        n_instances: Optional[int] = None, time: Optional[int]=None) -> None:

        d = {'name': class_name, 'question base name': question_base_name}

        if init_parameters:

            d['init parameters'] = init_parameters

        assert (parameters is not None) ^ (n_instances is not None)

        if parameters:

            d['parameters'] = parameters

        else:

            d['number of instances'] = n_instances

        if time:

            d['time'] = time

        class_settings = self.locate(category_name, class_name)

        if class_settings is None:

            category_settings = self.locate(category_name)

            assert category_settings is not None, f'category "{category_name}" not found'

            if category_settings['classes'] is None:

                category_settings['classes'] = []

            category_settings['classes'].append(d)

        else:

            class_settings.update(d)

        self._classes.add(class_name)

# Cell

def initialize(output_file: str, pictures_directory: str, ) -> dict:

    settings = {}

    settings['output file'] = output_file
    settings['pictures base directory'] = pictures_directory
    settings['categories'] = None

    return settings

# Cell

def set_class_preamble(settings: dict, category_name: str, base_category: Optional[str] = None, test_mode: bool = False) -> Union[str, list]:

    if test_mode:

        category_name = 'test'

    else:

        if base_category:

            category_name = [base_category, f'{base_category}/{category_name}']


    if settings['categories'] is None:

        settings['categories'] = []

    settings['categories'].append({'name': category_name, 'classes': None})

    return category_name

# Cell

def set_class_closing(settings: dict, n_instances: int, time: Optional[int] = None) -> None:

    if settings['categories'][-1]['classes'] is None:

        settings['categories'][-1]['classes'] = [{}]

    settings['categories'][-1]['classes'][-1]['number of instances'] = n_instances
    settings['categories'][-1]['classes'][-1]['time'] = time

# Cell

def set_class(
    settings: dict, class_name: str, question_base_name: str, init_parameters: Optional[dict] = None,
    parameters: Optional[List[dict]] = None, n_instances: Optional[int] = None, time: Optional[int]=None) -> None:

    assert (parameters is not None) ^ (n_instances is not None)

    d = {'name': class_name, 'question base name': question_base_name}

    if init_parameters:

        d['init parameters'] = init_parameters

    if parameters:

        d['parameters'] = parameters

    else:

        d['number of instances'] = n_instances

    if time:

        d['time'] = time

    settings['categories'][-1]['classes'] = [d]

# Cell

def write_header(file: Union[str, pathlib.Path], output_file: str, pictures_directory: str, ) -> None:

    settings = initialize(output_file, pictures_directory)

    py2gift.util.dict_to_yaml(settings, file)

# Cell

def write_class_preamble(file: Union[str, pathlib.Path], category_name: str, base_category: Optional[str] = None, test_mode: bool = False) -> Union[str, list]:


    settings = py2gift.util.yaml_to_dict(file)
    category_name = set_class_preamble(settings, category_name, base_category, test_mode)
    py2gift.util.dict_to_yaml(settings, file)

    return category_name

# Cell

def write_class_closing(file: Union[str, pathlib.Path], n_instances: int, time: Optional[int] = None) -> None:

    settings = py2gift.util.yaml_to_dict(file)
    category_name = set_class_closing(settings, n_instances, time)
    py2gift.util.dict_to_yaml(settings, file)

# Cell

def function_to_make_hierarchical_category_name(base_category: str) -> Callable[[str], list]:

    def make_subcategory(category: str) -> list:

        return [base_category, f'{base_category}/{category}']

    return make_subcategory