#!/bin/bash

COLOR="\033[40m\033[32m"
UNCOLOR="\033[0m"

NAME=py2gift

# only required if "anaconda" is not in the path
source $HOME/anaconda3/etc/profile.d/conda.sh

conda create --yes -n $NAME python=3 jupyterlab=2 numpy pandas ruamel.yaml tqdm pyyaml paramiko colorama -c defaults -c conda-forge

echo -e new environment is \"$COLOR$NAME$UNCOLOR\"

conda activate $NAME

# just for testing purposes
conda install sympy

# pip install gift-wrapper nbdev
pip install nbdev

# ipython widgets (tqdm progress bar in a notebook)
conda install ipywidgets
jupyter labextension install @jupyter-widgets/jupyterlab-manager

# a Table of Contents extension for JupyterLab
jupyter labextension install @jupyterlab/toc

# the environment is exported into a yaml file
conda env export --no-builds --from-history -f environment.yml
