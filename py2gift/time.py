# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/50_time.ipynb.

# %% auto 0
__all__ = ['TimeKeeper']

# %% ../nbs/50_time.ipynb 2
import json
from typing import Union

import pandas as pd

# %% ../nbs/50_time.ipynb 5
class TimeKeeper:
    
    def __init__(self) -> None:
        
        self.df = pd.DataFrame(columns=['time'])
        self.df.index.name = 'category'
        
        
        # for making sure calls to `record` and `record_question` are not mixed
        self.record_type = None
    
    def process_category_name(self, category_name: Union[str, list]) -> str:
        
        # if the category is a string (rather than a list)...
        if type(category_name)==str:
            
            # ...an attempt...
            try:
            
                # ...to interpret it is made
                category_name = json.loads(category_name)
                
                # if it is still a string...
                if type(category_name)==str:
                    
                    # ...that's it
                    return category_name
                
                # if it's not a string, then it is assumed it is a list
            
            except json.JSONDecodeError:
                
                return category_name
        
        return category_name[-1].split('/')[-1]
    
    def record(self, minutes: int, category_name: Union[str, list]) -> None:
        
        if self.record_type is None:
            
            self.record_type = 'category'
        
        else:
            
            assert self.record_type == 'category', 'you cannot mix questions and categories'
        
        self.df.loc[self.process_category_name(category_name)] = minutes
        
    def record_question(self, minutes: int, question_name: str) -> None:
        
        if self.record_type is None:
            
            self.record_type = 'question'
        
        else:
            
            assert self.record_type == 'question', 'you cannot mix questions and categories'
        
        self.df.loc[question_name] = minutes
    
    def __str__(self) -> str:
        
        return f'Accumulated time: {self.df["time"].sum()} minutes'
    
    def plot(self):
        
        ax = self.df.plot.pie(y='time')
        ax.legend().remove()
        ax.set_ylabel(None)
        
        return ax
