![EAS2Text](https://github.com/A-c0rN/EASGen/blob/main/doc/img/EASGen.png)

![PyPI](https://img.shields.io/pypi/v/EASGen?label=Version&style=flat-square) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/A-c0rN/EASGen/CodeQL?style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dm/EASGen?style=flat-square) ![GitHub language count](https://img.shields.io/github/languages/count/A-c0rN/EASGen?style=flat-square) ![GitHub](https://img.shields.io/github/license/A-c0rN/EASGen?style=flat-square)

An Extensive EAS Header to Text Translation Python Library

## Features
> - [x] EAS to Text Translation
> - [x] EAS EOM detection
> - [x] Handles Unknown Callsigns, Originators, and FIPS codes
> - [x] Fast as all hell, as per usual :3

## Installation
This package should be installable through Pip.

On a Debian Based Linux OS:
```
sudo apt update
sudo apt install python3 python3-pip
pip3 install EAS2Text
```


On Windows:

[Install Python](https://www.python.org/downloads/)

In CMD:
```
python -m pip install EAS2Text
```

## Usage
This package should take a raw ZCZC string, and then return the full text, and/or individual options:
```python
from EAS2Text.EAS2Text import EAS2Text

header = "ZCZC-WXR-RWT-048031-048209-048491-048453-048021-048053-048287-048491-048055+0015-0211700-KALT/ERN-" ## EAS Header to decode
EASConverted = EAS2Text.toText(header=header)
print(EASConverted)
```
should output:
```
The National Weather Service has issued a Required Weekly Test for Blanco, TX; Hays, TX; Williamson, TX; Travis, TX; Bastrop, TX; Burnet, TX; Lee, TX; and Caldwell, TX; beginning at 11:00 PM January 21, 2022 and ending at 11:15 PM January 21, 2022. Message from KALT/ERN.
```