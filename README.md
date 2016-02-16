# Unitex binding for python

This package provides access to the Unitex C++ Library.

## Features

* Unitex as a library
* Persistence
* Virtualization

## Installation

The library has been tested on MacOSX (with `python` from the [MacPorts](https://www.macports.org/) projet) and Linux for the versions 2 and 3 of Python. The installation requires the Python header files and the [Unitex](http://igm.univ-mlv.fr/~unitex/index.php?page=3&html=download.html) source distribution.

Once you have filled the requirements and downloaded the package, you just have to run (as root):

```
UNITEX_INC=/path/to/unitex/Src/C++ python setup.py install
```

## Getting started

There is three ways to use the Unitex Python library:

1. The `_unitex` C++ extension.
2. The Unitex basic commands and features.
3. The `Processor` high-level class.

The following sections gives some sample codes to illustrate each of them.

### The `_unitex` C++ extension.
### The Unitex basic commands and features.
### The `Processor` high-level class.

## Useful links

* The **Unitex/GramLab** corpus processor: [homepage](http://www-igm.univ-mlv.fr/~unitex/) and [documentation](http://igm.univ-mlv.fr/~unitex/UnitexManual3.1.pdf)



