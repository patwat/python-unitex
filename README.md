# Python bindings for Unitex/GramLab

This package provides access to the Unitex C++ Library.

## Main features

* Unitex as a library
* Persistence of linguistic resources
* File virtualization

## Installation

The library has been tested on MacOSX (with Python from the [MacPorts](https://www.macports.org/) project) and Linux ([Debian](https://www.debian.org/)) for versions 2.7 and 3.5 of Python. The installation requires the Python header files and the `setuptools` module. If you plan to use the configuration system, you will also need the `yaml` module.

```bash
# Run as root
# On MacOSX (MacPorts)
# NOTE: the Python header files are installed by default
#       (cf. https://trac.macports.org/wiki/Python)
# Python 2.7
port install py27-setuptools
port install py27-yaml

# Python 3.5
port install py35-setuptools
port install py35-yaml

# On Linux (distributions based on Debian)
# Python 2.7
apt-get install python-dev
apt-get install python-setuptools
apt-get install python-yaml
```

Once you have met these requirements and downloaded the [Unitex](http://igm.univ-mlv.fr/~unitex/index.php?page=3&html=download.html) source distribution, run (as root):

```bash
UNITEX_INC=/path/to/unitex/Src/C++ python setup.py install
```

## Installation testing

If you want to test your installation, open a terminal, move in the `tests` directory and run (as user):

```bash
pat@lucy /home/dev/projects/python-unitex/tests [2]$ python 01_test_tools.py
............
----------------------------------------------------------------------
Ran 12 tests in 0.023s

OK
```

```bash
pat@lucy /home/dev/projects/python-unitex/tests [3]$ python 02_test_resources.py
......
----------------------------------------------------------------------
Ran 6 tests in 0.003s

OK
```

```bash
pat@lucy /home/dev/projects/python-unitex/tests [4]$ python 03_test_io.py
....................
----------------------------------------------------------------------
Ran 20 tests in 0.004s

OK
```

```bash
pat@lucy /home/dev/projects/python-unitex/tests [5]$ python 04_test_processor.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.045s

OK
```

## Getting started

**NOTE: The texts must be encoded in UTF-8. There is so far no support for UTF-16-(LE|BE) or any other encoding.**

There are three ways to use the bindings (from low to high-level):

1. The `_unitex` C++ extension.
2. The Unitex basic commands and features.
3. The high-level `Processor` class.

The following sections give some sample code for each of these methods.

### The `_unitex` C++ extension

This works like the JNI interface which is part of the Unitex distribution and provides conversion of arguments (into C++ types) and returned values (into Python objects).

```python
from _unitex import unitex_load_persistent_alphabet,\
					unitex_free_persistent_alphabet,\
					unitex_tool

alphabet = unitex_load_persistent_alphabet("/path/to/Alphabet.txt")
grammar = "/path/to/grammar.grf"

command = "UnitexTool Grf2Fst2 --no_loop_check --alphabet=%s %s -qutf8-no-bom" % (alphabet, grammar)

ret = unitex_tool(command)

unitex_free_persistent_alphabet(alphabet)
```
### The Unitex basic commands and features

This part of the bindings is just an abstraction layer in front of the C++ extension. It provides a basic logging system and a number of checks (on arguments). There is also the possibility of storing the different resources and (tools) options in a [configuration file](https://github.com/patwat/python-unitex/blob/master/config/unitex-template.yaml) which offers more flexibility. 

```python
import yaml

from unitex.tools import grf2fst2
from unitex.config import UnitexConfig
from unitex.resources import load_persistent_alphabet, free_persistent_alphabet

grammar = "/path/to/grammar.grf"

config = None
with open("/path/to/unitex.yaml", "r") as f:
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

### The high-level `Processor` class

This class hides most of the Unitex (pre-)processing procedures in order to facilitate its usage.

```python
import os

from unitex.resources import load_persistent_fst2, free_persistent_fst2
from unitex.processor import UnitexProcessor

files = [ ... ]
grammar = load_persistent_fst2("/path/to/grammar.fst2")

# Persistence is achieved during object initialization
processor = UnitexProcessor("/path/to/unitex.yaml")

kwargs = {}
kwargs["xml"] = False

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

In the [`examples`](https://github.com/patwat/python-unitex/blob/master/examples/) directory, you will find two scripts you can use to achieve two simple tasks.

1. `build-config-file.py`: this script builds, for a given language, a default YAML configuration file adapted to your local Unitex installation. This configuration file allows you to define the different parameters required by Unitex and by the bindings.
2. `do-concord.py`: this script can be used to perform a real Unitex process: the extraction of concordances from a corpus on the basis of a grammar. It also illustrates in a more detailed way of using the package for other tasks.

To visualize the different options and arguments of these scripts, just run (as user) each script with the `--help` option as shown below:

```bash
pat@lucy /home/dev/projects/python-unitex/examples [1]$ python build-config-file.py --help
Build Config File -- build the (default) config file for a given language

  $ build-config-file [OPTIONS] <Unitex YAML config template>

Options:
  [ -h, --help      = this help message                                      ]
    -o, --output    = the resulting config filename
    -l, --language  = the language name
    -d, --directory = the original resources directory for the language
                      (i.e. the language directory from Unitex distribution)

Example:
  $ build-config-file -l fr -d /path/to/French -o unitex-fr.yaml unitex.yaml
```

```bash
pat@lucy /home/dev/projects/python-unitex/examples [2]$ python do-concord.py --help
Do Concord -- A simple script to illustrate the Unitex Python bindings

  $ do-concord [OPTIONS] <file1(, file2, ...)>

Options:
  [ -h, --help    = this help message       ]
    -c, --config  = the Unitex config file
    -g, --grammar = the fst2 grammar to use

Example:
  $ do-concord -c unitex-fr.yaml *.txt
```

## Useful links

* The **Unitex/GramLab** corpus processor: [homepage](http://www-igm.univ-mlv.fr/~unitex/) and [documentation](http://igm.univ-mlv.fr/~unitex/UnitexManual3.1.pdf)
* The **Unitex C++/Java library**: [documentation](http://unitex-library-fr.readthedocs.org/)
