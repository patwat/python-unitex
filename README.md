# Unitex binding for python

This package provides access to the Unitex C++ Library.

## Main features

* Unitex as a library
* Linguistic resources persistence
* File virtualization

## Installation

The library has been tested on MacOSX (with `python` from the [MacPorts](https://www.macports.org/) projet) and Linux for the versions 2 and 3 of Python. The installation requires the Python header files and the [Unitex](http://igm.univ-mlv.fr/~unitex/index.php?page=3&html=download.html) source distribution. If you plan to use the configuration system, you will also need the `yaml` python module.

Once you have filled the requirements and downloaded the package, you just have to run (as root):

```
UNITEX_INC=/path/to/unitex/Src/C++ python setup.py install
```

## Getting started

**NOTE: The texts must be encoded in UTF-8. There's no support so far for UTF-16-(LE|BE).**

There is three ways to use the Unitex Python library:

1. The `_unitex` C++ extension.
2. The Unitex basic commands and features.
3. The `Processor` high-level class.

The following sections gives some sample codes to illustrate each of them.

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

This part of the binding is just an abstraction layer in front of the the C++ API. It provides some kind of logging and a bunch of checking (mostly arguments). There's also the possibility to store the different resources and (tools) options in a [configuration file](https://github.com/patwat/python-unitex/blob/master/config/unitex.yaml) which offers more flexibility. 

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

This class hides most of the Unitex (pre-)processing procedures in order to facilitate his usage.

```python
from unitex.resources import load_persistent_fst2, free_persistent_fst2
from unitex.processor import UnitexProcessor

grammar = load_persistent_fst2("grammar.fst2")

processor = UnitexProcessor("unitex.yaml")
processor.open("corpus.txt", mode="srtlf", tagged=False)

kwargs = {}
kwarg["xml"] = True

processor.tag(grammar, "corpus.tag", **kwargs)

processor.close(clean=True, free=True)

free_persistent_fst2(grammar)
```

## Useful links

* The **Unitex/GramLab** corpus processor: [homepage](http://www-igm.univ-mlv.fr/~unitex/) and [documentation](http://igm.univ-mlv.fr/~unitex/UnitexManual3.1.pdf)

* The **Unitex C++/Java library**: [documentation](http://unitex-library-fr.readthedocs.org/)


