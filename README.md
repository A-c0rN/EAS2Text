![EAS2Text](https://github.com/A-c0rN/EAS2Text/blob/master/doc/img/EAS2Text.png)

![PyPI](https://img.shields.io/pypi/v/EAS2Text?label=Version&style=flat-square) ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/A-c0rN/EAS2Text/main.yml?style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dm/EAS2Text?style=flat-square) ![GitHub language count](https://img.shields.io/github/languages/count/A-c0rN/EAS2Text?style=flat-square) ![GitHub](https://img.shields.io/github/license/A-c0rN/EAS2Text?style=flat-square)

An Extensive EAS Header to Text Translation Python Library

## Features
> - [x] EAS to Text Translation
> - [x] EAS EOM detection
> - [x] Handles Unknown Callsigns, Originators, and FIPS codes
> - [x] Additional raw outputs and individual item outputs
> - [x] EAS Data Validation
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
from EAS2Text import EAS2Text

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
from EAS2Text import EAS2Text

oof = EAS2Text("ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-WACN    -")

## RAW Data output
print(f"RAW Data: {oof.EASData}") ## Input Data
print(f"RAW ORG: {oof.org}") ## Raw Originator Code: ZCZC-{ORG}-EVN-PSSCCC-PSSCCC+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW EVNT: {oof.evnt}") ## Raw Event Code: ZCZC-ORG-{EVN}-PSSCCC-PSSCCC+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW FIPS: {oof.FIPS}")  ## Raw FIPS Code(s) in a list: ZCZC-ORG-EVN-{PSSCCC-PSSCCC}+TTTT-JJJHHMM-CCCCCCCC-
print(f"Purge Time: {oof.purge}") ## Purge Time in a list format of HH, MM: ZCZC-ORG-EVN-PSSCCC-PSSCCC+{TTTT}-JJJHHMM-CCCCCCCC-
print(f"RAW TIMESTAMP: {oof.timeStamp}") ## RAW Timestamp: ZCZC-ORG-EVN-PSSCCC-PSSCCC+TTTT-{JJJHHMM}-CCCCCCCC-

## Semi-RAW Data
print(f"Start Time: {oof.startTime}") ## A Datetime.Datetime object of the Start Time (Local Timezone)
print(f"End Time: {oof.endTime}") ## A Datetime.Datetime object of the End Time (Local Timezone)

## Parsed Data Output
print(f"TEXT ORG: {oof.orgText}") ## A Human-Readable Version of ORG
print(f"TEXT EVNT: {oof.evntText}") ## A Human Readable Version of EVN
print(f"TEXT FIPS: {oof.FIPSText}") ## A List of All FIPS County Names (Returns "FIPS Code PSSCCC" if no available county)
print(f"TEXT Start Time: {oof.startTimeText}") ##A Start-Time Tag in the format of "HH:MM AM/PM MONTH_NAME DD, YYYY"
print(f"TEXT End Time: {oof.endTimeText}") ##A End-Time Tag in the format of "HH:MM AM/PM MONTH_NAME DD, YYYY"
print(f"{oof.EASText}") ## The full EAS Output data
```
should output:
```
RAW Data: ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-WACN    -
RAW ORG: WXR
RAW EVNT: SPS
RAW FIPS: ['024043', '024021', '024013', '024005', '024001', '024025', '051840', '051069', '054027', '054065', '054003', '054037', '054057']
Purge Time: ['06', '00']
RAW TIMESTAMP: 0231829
Start Time: 2022-01-23 13:29:00.000178
End Time: 2022-01-23 19:29:00.000178
TEXT ORG: The National Weather Service
TEXT EVNT: a Special Weather Statement
TEXT FIPS: ['Washington, MD', 'Frederick, MD', 'Carroll, MD', 'Baltimore county, MD', 'Allegany, MD', 'Harford, MD', 'Winchester city, VA', 'Frederick, VA', 'Hampshire, WV', 'Morgan, WV', 'Berkeley, WV', 'Jefferson, WV', 'Mineral, WV']
TEXT Start Time: 01:29 PM
TEXT End Time: 07:29 PM
The National Weather Service has issued a Special Weather Statement for Washington, MD; Frederick, MD; Carroll, MD; Baltimore county, MD; Allegany, MD; Harford, MD; Winchester city, VA; Frederick, VA; Hampshire, WV; Morgan, WV; Berkeley, WV; Jefferson, WV; and Mineral, WV; beginning at 01:29 PM and ending at 07:29 PM. Message from WACN.
```

## NEW FEATURE: Encoder Emulation!
EAS2Text is the first Header to Text adapter that can "Emulate ENDECs"

Currently Supported:
 - DASDEC
 - BURK
 - SAGE EAS
 - SAGE DIGITAL
 - TRILITHIC
 - TFT

Not Supported:
 - EAS-1
 - HollyAnne Units

To use an emulation system:
```python
from EAS2Text import EAS2Text

oof = EAS2Text(sameData = "ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-WACN    -", mode="SAGE EAS") ## Emulates a SAGE EAS ENDEC

print(f"{oof.EASText}") ## The full EAS Output data, 1822 style
```

## NEW FEATURE: Timezone Specification!
You can now specify a timezone offset to use! 
Note: This *CAN* and *WILL* break if you use obscure timezones. Keep it to Mainland U.S. for best reliability.

To use an specific timezone:
```python
from EAS2Text import EAS2Text

oof = EAS2Text(sameData = "ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-WACN    -", timeZone=-6) ## Uses a UTC-6 Offset

print(f"{oof.EASText}") ## The full EAS Output data, with a UTC-6 Offset.
```
