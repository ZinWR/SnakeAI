# Environment Installation
```
# Basic Envinronemt 

## Anaconda (Conda) install
conda config --add channels conda-forge
conda config --set channel_priority strict

## Set up pyenv
brew install pyenv
pyenv install 3.7.12
pyenv global 3.7.12

# Initial Set up - Pygame & Pytorch
conda create -n pygame_env python=3.8
conda activate pygame_env
pip install pygame
pip install torch torch vision
```