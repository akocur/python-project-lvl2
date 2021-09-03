### Hexlet tests and linter status:
[![Actions Status](https://github.com/akocur/python-project-lvl2/workflows/hexlet-check/badge.svg)](https://github.com/akocur/python-project-lvl2/actions) [![Linter](https://github.com/akocur/python-project-lvl2/actions/workflows/linter.yml/badge.svg?branch=main)](https://github.com/akocur/python-project-lvl2/actions/workflows/linter.yml)
### CODE CLIMATE:
[![Maintainability](https://api.codeclimate.com/v1/badges/f18410dbffcbbdb6159d/maintainability)](https://codeclimate.com/github/akocur/python-project-lvl2/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/f18410dbffcbbdb6159d/test_coverage)](https://codeclimate.com/github/akocur/python-project-lvl2/test_coverage)

###Gendiff is a CLI utility for finding differences between configuration files. 
###Suppported formats: YAML, JSON
## Usage

### As external library

```python
from gendiff import generate_diff

diff = generate_diff(file_path1, file_path2)
```

### As CLI tool

```
> gendiff --help
usage: gendiff [-h] [-f FORMAT] first_file second_file

Compares two configuration files and shows a difference.

positional arguments:
  first_file
  second_file

optional arguments:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        output format (default: "stylish"). Available: ['stylish', 'plain',
                        'json']

```
## Installation

```bash
python3 -m pip install --user git+https://github.com/akocur/python-project-lvl2.git
```
## Uninstallation

```bash
python3 -m pip uninstall hexlet-code
```

## Demo:
### Compare plain files:
[![asciicast](https://asciinema.org/a/gy6Ec9Z5Ct3YxyaZL8tnA28dT.svg)](https://asciinema.org/a/gy6Ec9Z5Ct3YxyaZL8tnA28dT)
### Compare complex files:
[![asciicast](https://asciinema.org/a/BVV3LufPZR3nSCftS2zY3GCbG.svg)](https://asciinema.org/a/BVV3LufPZR3nSCftS2zY3GCbG)
