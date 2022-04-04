![EAS2Text](https://github.com/A-c0rN/EAS2Text/blob/master/doc/img/EAS2Text.png)

![PyPI](https://img.shields.io/pypi/v/EAS2Text?label=Version&style=flat-square) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/A-c0rN/EAS2Text/CodeQL?style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dm/EAS2Text?style=flat-square) ![GitHub language count](https://img.shields.io/github/languages/count/A-c0rN/EAS2Text?style=flat-square) ![GitHub](https://img.shields.io/github/license/A-c0rN/EAS2Text?style=flat-square)

An Extensive EAS Header to Text Translation Python Library

## Features
> - [x] EAS to Text Translation
> - [x] EAS EOM detection
> - [x] Handles Unknown Callsigns, Originators, and FIPS codes
> - [x] Additional raw outputs and individual item outputs
> - [x] Fast as all hell, as per usual :3
> - [x] Both US and Canada integration

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

data = EAS2Text("ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-WACN    -")
print(f"{data.EASText}")
```
should output:
```
The National Weather Service has issued a Special Weather Statement for  Washington, MD;  Frederick, MD;  Carroll, MD;  Baltimore, MD;  Allegany, MD;  Harford, MD;  Winchester, VA;  Frederick, VA;  Hampshire, WV;  Morgan, WV;  Berkeley, WV;  Jefferson, WV; and  Mineral, WV; beginning at 12:29 AM January 24, 2022 and ending at 6:29 AM January 24, 2022. Message from WACN.
```

## Advanced Useage:
Using the Generator, you can get additional output of info from an alert:
```python
from EAS2Text.EAS2Text import EAS2Text

oof = EAS2Text("ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-WACN    -")

## RAW Data output
print(f"RAW Data: {oof.EASData}") ## Input Data
print(f"RAW ORG: {oof.org}") ## Raw Originator Code: ZCZC-{ORG}-EVN-PSSCCC-PSSCCC+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW EVNT: {oof.evnt}") ## Raw Event Code: ZCZC-ORG-{EVN}-PSSCCC-PSSCCC+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW FIPS: {oof.FIPS}")  ## Raw FIPS Code(s) in a list: ZCZC-ORG-EVN-{PSSCCC-PSSCCC}+TTTT-JJJHHMM-CCCCCCCC-
print(f"Purge Time: {oof.purge}") ## Purge Time in a list format of HH, MM: ZCZC-ORG-EVN-PSSCCC-PSSCCC+{TTTT}-JJJHHMM-CCCCCCCC-
print(f"RAW TIMESTAMP: {oof.timeStamp}") ## RAW Timestamp: ZCZC-ORG-EVN-PSSCCC-PSSCCC+TTTT-{JJJHHMM}-CCCCCCCC-

## Parsed Data Output
print(f"TEXT ORG: {oof.orgText}") ## A Human-Readable Version of ORG
print(f"TEXT EVNT: {oof.evntText}") ## A Human Readable Version of EVN
print(f"TEXT FIPS: {oof.FIPSText}") ## A List of All FIPS County Names (Returns "FIPS Code PSSCCC" if no available county)
print(f"TEXT Start Time: {oof.startTimeText}") A Start-Time Tag in the format of "HH:MM AM/PM MONTH_NAME DD, YYYY"
print(f"TEXT End Time: {oof.endTimeText}")
print(f"{oof.EASText}")
```
should output:
```
RAW Data: ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-WACN    -
RAW ORG: WXR
RAW EVNT: SPS
RAW FIPS: ['024043', '024021', '024013', '024005', '024001', '024025', '051840', '051069', '054027', '054065', '054003', '054037', '054057']
Purge Time: ['06', '00']
RAW TIMESTAMP: 0231829
TEXT ORG: The National Weather Service
TEXT EVNT: a Special Weather Statement
TEXT FIPS: [' Washington, MD', ' Frederick, MD', ' Carroll, MD', ' Baltimore, MD', ' Allegany, MD', ' Harford, MD', ' Winchester, VA', ' Frederick, VA', ' Hampshire, WV', ' Morgan, WV', ' Berkeley, WV', ' Jefferson, WV', ' Mineral, WV']
TEXT Start Time: 12:29 AM January 24, 2022
TEXT End Time: 6:29 AM January 24, 2022
The National Weather Service has issued a Special Weather Statement for  Washington, MD;  Frederick, MD;  Carroll, MD;  Baltimore, MD;  Allegany, MD;  Harford, MD;  Winchester, VA;  Frederick, VA;  Hampshire, WV;  Morgan, WV;  Berkeley, WV;  Jefferson, WV; and  Mineral, WV; beginning at 12:29 AM January 24, 2022 and ending at 6:29 AM January 24, 2022. Message from WACN.
```