# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/60_notebook.ipynb.

# %% auto 0
__all__ = ['ClassesContainer', 'MyMagics']

# %% ../nbs/60_notebook.ipynb 2
import argparse
import json

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic, line_cell_magic

import py2gift.input_file

# %% ../nbs/60_notebook.ipynb 5
class ClassesContainer:
    
    def add(cls, class_to_add):
        
        setattr(cls, class_to_add.__name__, class_to_add)

# %% ../nbs/60_notebook.ipynb 12
# The class MUST call this class decorator at creation time
@magics_class
class MyMagics(Magics):
    
    statement_key = 'statement'
    feedback_key = 'feedback'
    
    def __init__(self, shell=None,  **kwargs):
        
        super().__init__(shell=shell, **kwargs)
        
        
        self.location_parser = argparse.ArgumentParser(description='Specification')
        self.location_parser.add_argument('settings', help='Settings object')
        self.location_parser.add_argument('-c', '--cls', default=None, help='class')
        
        # the name of a category can contain spaces; notice that this will yield a *list* rather than a string
        self.location_parser.add_argument('-C', '--category', default=None, nargs='+', help='category')
    
    def process(self, line: str, cell: str, key: str):
        
        line_arguments = self.location_parser.parse_args(line.split())
        
#         print(f'line_arguments.category={line_arguments.category}')
        
        if line_arguments.category:
            
            category = json.loads(' '.join(line_arguments.category))
        
        else:
            
            category = None
        
        settings = self.shell.user_ns[line_arguments.settings]
        
        if category is None:
            
            category = settings.store['categories'][-1]['name']
            
        
        cls = line_arguments.cls
        
        if cls is None:
            
            cls = settings.locate(category_name=category)['classes'][-1]['name']
        

#         print(f'category={category}, class={cls}')
        
        settings.locate(category_name=category, class_name=cls)[key] = cell

    @cell_magic
    def statement(self, line, cell):

        self.process(line, cell, self.statement_key)
        
        return f'statement recorded'
    
    @cell_magic
    def feedback(self, line, cell):
        
        self.process(line, cell, self.feedback_key)
        
        return f'feedback recorded'

# %% ../nbs/60_notebook.ipynb 31
get_ipython().register_magics(MyMagics)
