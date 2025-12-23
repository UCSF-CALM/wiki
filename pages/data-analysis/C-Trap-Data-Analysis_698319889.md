---
layout: default
title: C-Trap Data Analysis
author: Stuurman, Nico
date: Mar 05, 2025
---

2.  [CALM Microscopy Wiki
    Home](CALM-Microscopy-Wiki-Home_512554980.html)

\

# Installation instructions 

## Install Lakeview 

- download [Lakeview
  installer](https://lumicks.com/lakeview-data-analysis/#get-lakeview){.external-link
  rel="nofollow"}
- Run the installer
- Enter license only when needed (ask CALM if you think you need a
  license)\
   

## Install Python packages 

###  [Install uv (Python package manager)](https://docs.astral.sh/uv/getting-started/installation/){.external-link rel="nofollow"}

How to do this depends on your Operating System. 

On Windows:

- open powershell (under the current user) and run:

- powershell -ExecutionPolicy ByPass -c {$env:UV_INSTALL_DIR = "C:\Custom\Path";irm https://astral.sh/uv/install.ps1 | iex}

On Mac OS:

In a terminal execute:

    curl -LsSf https://astral.sh/uv/install.sh | sh

###  Create a virtual environment for pylake (needed only the first time)

- Open a terminal (on Windows, I use [git
  bash](https://git-scm.com/downloads/win){.external-link
  rel="nofollow"})
- In a directory of your choice (I like the directory \"Projects\", to
  create this directory type \`mkdir Projects\`, then \`cd Projects\`)
  run

<!-- -->

    uv venv pylake

###  Activate the virtual environment (needed each session)

- cd to the directory with the venv (\`cd Projects\` if you followed the
  instructions above) and enter:

<!-- -->

    source pylake/Scripts/activate

###  Install the needed packaged (needed only first time):

    uv pip install lumicks.pylake
    uv pip install jupyter

\

It may be needed to install jupyter extensions:

\

    jupyter labextension install jupyter-matplotlib

\

### Launch Jupyter by typing (needed each session)

    jupyter notebook

### Startup during daily use. Open a terminal, type:

\

    cd Projects
    source pylake/Scripts/activate
    jupyter notebook

\

### Example notebook code (follow the [ tutorial](https://lumicks-pylake.readthedocs.io/en/stable/tutorial/file.html)):

**Jupyter notebook**

``` {.syntaxhighlighter-pre syntaxhighlighter-params="brush: py; gutter: false; first-line: 1"}
import numpy as np
import matplotlib.pyplot as plt
import lumicks.pylake as lk
filenames = lk.download_from_doi("10.5281/zenodo.7729525", "test_data")
file = lk.File("test_data/kymo.h5")

plt.figure()
file.force1x.plot()
plt.savefig("force1x.png")
plt.show()

d_data = file["Distance"]["Distance 1"]
hf_downsampled, d_cropped = file["Force HF"]["Force 1x"].downsampled_like(d_data)

plt.figure()
d_cropped.plot()
hf_downsampled.plot()
plt.show()
```

###   Script sharing website  [http://harbor.lumicks.com/](https://github.com/lumicks/harbor){.external-link rel="nofollow"}