# Unitex binding for python

This package provides access to the Unitex C++ Library.

## Main features

* Unitex as a library
* Linguistic resources persistence
* File virtualization

## Installation

The library has been tested on MacOSX (with `python` from the [MacPorts](https://www.macports.org/) projet) and Linux for the versions 2 and 3 of Python. The installation requires the Python header files and the [Unitex](http://igm.univ-mlv.fr/~unitex/index.php?page=3&html=download.html) source distribution. If you plan to use the Processor high-level class, you will also need the `yaml` python module.

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
from _unitex import *

alphabet = unitex_load_persistent_alphabet("Alphabet.txt")

command = "UnitexTool Grf2Fst2 --no_loop_check --alphabet=%s grammar.grf -qutf8-no-bom" % alphabet

ret = unitex_tool(command)
```
### The Unitex basic commands and features.

The main difference with the `_unitex` extension is the argument checking.

```python
from unitex.tools import *
from unitex.resources import *

grammar = "grammar.grf"
alphabet = load_persistent_alphabet("Alphabet.txt")

kwargs = {}
kwargs["loop_check"] = False
kwargs["char_by_char"] = False
kwargs["pkgdir"] = None
kwargs["no_empty_graph_warning"] = False
kwargs["tfst_check"] = False
kwargs["silent_grf_name"] = False
kwargs["named_repositories"] = None
kwargs["debug"] = False
kwargs["check_variables"] = False

ret = grf2fst2(grammar, alphabet, **kwargs)
```

### The `Processor` high-level class.

**TODO**

## Useful links

* The **Unitex/GramLab** corpus processor: [homepage](http://www-igm.univ-mlv.fr/~unitex/) and [documentation](http://igm.univ-mlv.fr/~unitex/UnitexManual3.1.pdf)

* The **Unitex C++/Java library**: [documentation](http://unitex-library-fr.readthedocs.org/)


