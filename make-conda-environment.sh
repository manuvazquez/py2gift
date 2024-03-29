#!/bin/bash

MANAGER="mamba"

COLOR="\033[40m\033[32m"
UNCOLOR="\033[0m"

GIFTWRAPPER_PATH=$HOME/gift-wrapper
THIS_LIBRARY_LOCAL_PATH=$HOME/py2gift

NAME=py2gift

# only required if "anaconda" is not in the path
source $HOME/$MY_CONDA_INSTALLATION/etc/profile.d/conda.sh

$MANAGER create --yes -n $NAME jupyterlab ipywidgets numpy pandas ruamel.yaml tqdm pyyaml paramiko colorama twine nbdev">2.3" -c defaults -c conda-forge -c fastai

echo -e new environment is \"$COLOR$NAME$UNCOLOR\"

conda activate $NAME

# so that git is aware of nbdev/notebooks (only required once, when creating the repository, not through re-installs of conda)
nbdev_install_hooks

# "gift-wrapper" and other personal libraries are installed "live"...
pip install -e "$GIFTWRAPPER_PATH"

# ...and so is *this* library
pip install -e "$THIS_LIBRARY_LOCAL_PATH"

# # the environment is exported into a yaml file
# conda env export --no-builds --from-history -f environment.yml
