Melody squares
=============

Data and code for the project _Melody squares_, visualizing which melodic motifs can be found in a collection of melodies.

------

<img src="figures/figure-melody-square/figure-melody-square.jpg?raw=true" width="800" 
    title="Melody squares highlight which melodic motifs are common and which are rare in a corpus of melodies.">




**Abstract.** Melody squares visualize the melodic movements in melodies. It breaks down a melody into overlapping motifs of three notes which form two pitch intervals, and plots the first interval horizontally and the second vertically. A melody square, differently put, shows the frequency of pitch interval bigrams. This way of representing melodic motifs immediately highlights differences between corpora, but also suggests some interesting generalizations.


-----


Repository structure
--------------------

To do


Setup
-----

You can find the Python version used in `.python-version` and all dependencies are listed in `requirements.txt`. If you use pyenv and venv to manage python versions and virtual environments, do the following:

```bash
# Install the right python version
pyenv install | cat .python-version

# Create a virtual environment
python -m venv env

# Activate the environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```