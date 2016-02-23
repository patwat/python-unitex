# Unitex binding for Python

This package provides access to the Unitex C++ Library.

## Main features

* Unitex as a library
* Linguistic resources persistence
* File virtualization

## Installation

The library has been tested on MacOSX (with Python from the [MacPorts](https://www.macports.org/) project) and Linux (Debian stable) for the versions 2.7 and 3.5 of Python. The installation requires the Python header files and the `setuptools` module. If you plan to use the configuration system, you will also need the [`yaml`](http://pyyaml.org/wiki/PyYAML) module.

```bash
# Run as root
# On MacOSX (MacPorts)
# NOTE: the Python header files are installed by default
#       (cf. https://trac.macports.org/wiki/Python)
# For Python 2.7
port install py27-setuptools
port install py27-yaml

# For Python 3.5
port install py35-setuptools
port install py35-yaml

# On Linux (Debian)
# For Python 2.7
apt-get install python-dev
apt-get install python-setuptools
apt-get install python-yaml
```

Once you have filled the requirements and downloaded the [Unitex](http://igm.univ-mlv.fr/~unitex/index.php?page=3&html=download.html) source distribution, run (as root):

```bash
UNITEX_INC=/path/to/unitex/Src/C++ python setup.py install
```

## Getting started

**NOTE: The texts must be encoded in UTF-8. There is so far no support for UTF-16-(LE|BE) or any other encoding.**

There are three ways to use the Unitex Python library:

1. The `_unitex` C++ extension.
2. The Unitex basic commands and features.
3. The `Processor` high-level class.

The following sections give some sample codes for each of these ways.

### The `_unitex` C++ extension.

```python
from _unitex import unitex_load_persistent_alphabet,\
					unitex_free_persistent_alphabet,\
					unitex_tool

alphabet = unitex_load_persistent_alphabet("Alphabet.txt")

command = "UnitexTool Grf2Fst2 --no_loop_check --alphabet=%s grammar.grf -qutf8-no-bom" % alphabet

ret = unitex_tool(command)

unitex_free_persistent_alphabet(alphabet)
```
### The Unitex basic commands and features.

This part of the binding is just an abstraction layer in front of the C++ API. It provides a basic logging system and a number of checks (on arguments). There is also the possibility to store the different resources and (tools) options in a [configuration file](https://github.com/patwat/python-unitex/blob/master/config/unitex.yaml) which offers more flexibility. 

```python
import yaml

from unitex.tools import grf2fst2
from unitex.config import UnitexConfig
from unitex.resources import load_persistent_alphabet, free_persistent_alphabet

grammar = "grammar.grf"

config = None
with open("unitex.yaml", "r") as f:
    config = yaml.load(f)

options = UnitexConfig(config)

alphabet = options["resources"]["alphabet"]
if options["persistence"] is True:
	alphabet = load_persistent_alphabet(alphabet)

kwargs = options["tools"]["grf2fst2"]

ret = grf2fst2(grammar, alphabet, **kwargs)

if options["persistence"] is True:
	free_persistent_alphabet(alphabet)
```

### The `Processor` high-level class.

This class hides most of the Unitex (pre-)processing procedures in order to facilitate its usage.

```python
import os

from unitex.resources import load_persistent_fst2, free_persistent_fst2
from unitex.processor import UnitexProcessor

files = [ ... ]
grammar = load_persistent_fst2("grammar.fst2")

# Persistence is achieved during object initialization
processor = UnitexProcessor("unitex.yaml")

kwargs = {}
kwargs["xml"] = True

for f in files:
    path, _ = os.path.splitext(f)
    output = "%s.xml" % path

    # mode: 's': segment (apply Sentence.fst2)
    #       'r': replace (apply Replace.fst2)
    #       't': tokenize
    #       'l': lexicalize (apply dictionaries)
    processor.open(f, mode="srtl", tagged=False)
    processor.tag(grammar, output, **kwargs)

# 'clean': suppress the files produced by Unitex
# 'free': unload all the persisted resources
processor.close(clean=True, free=True)

free_persistent_fst2(grammar)
```

## Useful links

* The **Unitex/GramLab** corpus processor: [homepage](http://www-igm.univ-mlv.fr/~unitex/) and [documentation](http://igm.univ-mlv.fr/~unitex/UnitexManual3.1.pdf)
* The **Unitex C++/Java library**: [documentation](http://unitex-library-fr.readthedocs.org/)
