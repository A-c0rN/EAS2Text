# Standard Library
import re
from datetime import datetime as DT
from datetime import timezone
from time import localtime
from typing import Any, Iterable, Literal

# Third-Party
from errors import *

# First-Party
import db


class DBAccess(object):
    def __init__(self) -> None:
        self._language: str = "EN"
        self._country: str = "US"
        self._samelist: dict = db.SAME_US_FIPS

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, language: str) -> None:
        if language not in db.LANGUAGES:
            raise InvalidParameterError(
                error=language, message=f"Language needs to be in list {db.LANGUAGES}"
            )
        else:
            self._language = language

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, country: str) -> None:
        if country not in db.COUNTRIES:
            raise InvalidParameterError(
                error=country, message=f"Country needs to be in list {db.COUNTRIES}"
            )
        else:
            self._country = country
            if country == "CA":
                self._samelist = db.SAME_CA_FIPS
            elif country == "US":
                self._samelist = db.SAME_US_FIPS

    def get_locs_from_fips(self, fips_codes: Iterable[str]) -> dict[str, dict]:
        # Define some pre-processing values:
        # seen_fips used for keeping track of duplicates
        # process_fips used for tracking regional and area mappings
        # locs used for returned storage area
        seen_fips = []
        process_fips = {}
        locs = {
            "country": {"name": "", "abbrev": ""},
            "regions": {},
        }

        locs["country"]["name"] = self._samelist["name"]
        locs["country"]["abbrev"] = self._samelist["abbrev"]

        # Process input into valid fips codes
        for fips_code in fips_codes:
            # Skip if already processed
            if fips_code in seen_fips:
                continue
            else:
                seen_fips.append(fips_code)
                try:
                    # Make sure the code is numeric
                    assert fips_code.isnumeric()
                    # Make sure the code is 5 or 6 chars long
                    assert len(fips_code) >= 5 and len(fips_code) <= 6
                    # Zfill to make sure in range
                    _valid_fips = fips_code.zfill(6)
                    # Get Sub, Reg, Code from SAME FIPS
                    _subdiv = _valid_fips[0]
                    _region = _valid_fips[1:3]
                    _area = _valid_fips[3:6]
                    # Check if region already defined, if not define it.
                    if _region in process_fips.keys():
                        process_fips[_region] += [{"sub": _subdiv, "area": _area}]
                    else:
                        process_fips[_region] = [{"sub": _subdiv, "area": _area}]
                except AssertionError:
                    raise InvalidSAMEError(fips_code, "Invalid SAME FIPS code.")

        # Process fips codes
        for _region in process_fips.keys():
            # Process region data:
            try:
                # Define Region format
                reg = {"abbrev": "", "locs": []}
                # Check if region is valid in our FIPS list
                if _region in list(self._samelist.keys()):
                    reg_name = self._samelist[_region]["name"]
                    reg["abbrev"] = self._samelist[_region]["abbrev"]
                # Create an unknown loc if not defined
                else:
                    reg_name = f"Unknown"
                    reg["abbrev"] = ""

                # Check if region is defined in our final output, if not define it.
                if reg_name not in locs["regions"].keys():
                    locs["regions"][reg_name] = reg
            except Exception as E:
                raise InvalidSAMEError(_region, f"Error ({E}) on processing region.")

            # Process area codes:
            # All Loc codes (000) get special processing based off of subdivision.
            # Otherwise use "<subdiv> <area>"
            try:
                for codes in process_fips[_region]:
                    subcode = codes["sub"]
                    subdiv = db.SAME_SUBDIVISIONS[subcode][self._language]
                    code = codes["area"]
                    if code != "000":
                        if "Unknown" not in reg_name:
                            if code in self._samelist[_region]["codes"].keys():
                                area = self._samelist[_region]["codes"][code]
                            else:
                                area = f"FIPS {subcode}{_region}{code}"
                        else:
                            area = f"FIPS {subcode}{_region}{code}"
                        locs["regions"][reg_name]["locs"] += [f"{subdiv}{area}".strip()]
                    else:
                        alltext = self._samelist["all_text"][self.language]
                        locs["regions"][reg_name]["locs"] += [
                            f"{alltext}{subdiv}{reg_name}".strip()
                        ]
            except Exception as E:
                raise InvalidSAMEError(_region, f"Error ({E}) on processing area code.")
        return locs

    def get_event(self, event_code: str) -> dict[str, str]:
        try:
            # Make sure the event is alphanumeric
            assert event_code.isalnum()
            # Make sure the event is 3 chars long
            assert len(event_code) == 3
            # Check if the event is valid
            if event_code in db.SAME_EVENTS.keys():
                code = db.SAME_EVENTS[event_code]
                name = code["name"][self._language]
                article = code["article"][self._language]
                severity = code["severity"]
            # check if valid unknown event
            elif f"**{event_code[2]}" in db.SAME_EVENTS["Unknown"].keys():
                code = db.SAME_EVENTS["Unknown"][f"**{event_code[2]}"]
                name = f"{code["name"][self._language]} ({event_code})".strip()
                article = code["article"][self._language]
                severity = code["severity"]
            # return unknown event if invalid
            else:
                code = db.SAME_EVENTS["Unknown"]["*"]
                name = f"{code["name"][self._language]} ({event_code})".strip()
                article = code["article"][self._language]
                severity = code["severity"]
            return {
                "name": name,
                "article": article,
                "severity": severity,
            }
        except AssertionError:
            raise InvalidSAMEError(event_code, "Invalid SAME event code.")

    def get_originator(self, originator_code: str) -> dict[str, str]:
        try:
            # Make sure the originator is alphanumeric
            assert originator_code.isalnum()
            # Make sure the originator is 3 chars long
            assert len(originator_code) == 3
            # Check if the originator is valid
            if originator_code in db.SAME_ORIGINATORS.keys():
                code = db.SAME_ORIGINATORS[originator_code]
                try:
                    name = code["name"][self._language][self._country]
                    article = code["article"][self._language][self._country]
                    verb = code["verb"][self._language]
                except KeyError:
                    name = code["name"][self._language]["US"]
                    article = code["article"][self._language]["US"]
                    verb = code["verb"][self._language]
            else:
                code = db.SAME_ORIGINATORS["*"]
                name = f"{code["name"][self._language]} ({originator_code})"
                article = code["article"][self._language]
                verb = code["verb"][self._language]
            return {"name": name, "article": article, "verb": verb}
        except AssertionError:
            raise InvalidSAMEError(originator_code, "Invalid SAME originator code.")


class EASAlert(object):

    def __init__(self):
        ## All returnable values
        self.originatorCode = ""
        self.originatorText = ""

        self.eventCode = ""
        self.eventText = ""
        self.eventSeverity = ""

        self.fipsCode = ()
        self.fipsText = ""

        self.durationCode = ""
        self.durationOffset = 0

        self.timestampCode = ""
        self.timeStartEpoch = 0
        self.timeEndEpoch = 0
        self.timeStartText = ""
        self.timeEndText = ""

        self.callsign = ""

        self.text = ""


class EAS2Text(object):

    def __init__(
        self, language: str = "EN", country: str = "US", timeZone: int = None, mode: str = "NONE"
    ) -> None:

        self.DB = DBAccess()
        self.DB.language = language
        self.DB.country = country
        self.timeZone: int = timeZone
        self.textMode: str = mode

    def process_originator(self, originator):
        if not originator:
            raise InvalidParameterError("Originator is Missing")
        print("ORG")
        try:
            assert len(originator) == 3
        except AssertionError:
            raise InvalidSAMEError(f"Originator {originator} is an invalid length")
        originatorData = self.DB.get_originator(originator)
        return originatorData

    def process_event(self, event):
        if not event:
            raise InvalidParameterError("Event is Missing")
        print("EVNT")
        try:
            assert len(event) == 3
        except AssertionError:
            raise InvalidSAMEError(f"Event {event} is an invalid length")
        eventData = self.DB.get_event(event)
        return eventData

    def process_fips(self, fips: str):
        if not fips:
            raise InvalidParameterError("FIPS Codes are Missing")
        print("FIPS")
        tempFips = []
        for i in fips.split("-"):
            try:
                assert len(i) == 6
                assert i.isnumeric()
            except AssertionError:
                raise InvalidSAMEError(f"Invalid codes in FIPS data {fips}")
            if i not in tempFips:
                tempFips.append(i)
        fipsCode = tuple(tempFips)
        fipsData = self.DB.get_locs_from_fips(fipsCode)
        tempstr = []
        for region in fipsData["regions"]:
            name = region
            abbrev = fipsData["regions"][region]["abbrev"]
            locations = fipsData["regions"][region]["locs"]
            for location in locations:
                if not location.startswith("All of") or location.startswith("Todo"):
                    tempstr.append(f"{location}, {abbrev}")
                else:
                    tempstr.append(location)
        tempstr[-1] = f"and {tempstr[-1]};"
        fipsText = "; ".join(tempstr).strip()
        return (fipsCode, fipsData, fipsText)

    def process_duration(self, duration: str):
        if not duration:
            raise InvalidParameterError("Duration Code is Missing")
        print("DUR")
        try:
            assert duration.isnumeric()
            assert len(duration) == 4
        except AssertionError:
            raise InvalidSAMEError(f"Duration code {duration} is not in range HHMM")
        hour = int(duration[:2]) * 3600
        minute = int(duration[2:]) * 60
        durationOfs = hour + minute
        return durationOfs

    def process_timestamp(self, timestamp: str, durationOfs: int = 0):
        if not timestamp:
            raise InvalidParameterError("Timestamp is Missing")
        if not durationOfs:
            raise InvalidParameterError("Duration Epoch is Missing")
        print("STAMP")
        try:
            assert timestamp.isnumeric()
            assert len(timestamp) == 7
        except AssertionError:
            raise InvalidSAMEError(f"Timestamp {timestamp} is not in range JJJHHMM")
        utc = DT.now(timezone.utc)
        if self.timeZone == None:
            dtOffset = utc.timestamp() - DT.now().timestamp()
        else:
            dtOffset = -self.timeZone * 3600

        alertStartEpoch = DT.strptime(timestamp, "%j%H%M").replace(year=utc.year).timestamp()
        alertEndEpoch = alertStartEpoch + durationOfs
        timeStartEpoch = alertStartEpoch
        timeEndEpoch = alertEndEpoch

        try:
            timeStart = DT.fromtimestamp(alertStartEpoch - dtOffset)
            timeEnd = DT.fromtimestamp(alertEndEpoch - dtOffset)
        except Exception as E:
            raise InvalidSAMEError(
                timestamp,
                message=f"Error in Time Conversion ({str(E)})",
            )
        return (timeStartEpoch, timeEndEpoch, timeStart, timeEnd)

    def process_callsign(self, callsign: str):
        if not callsign:
            raise InvalidParameterError("Callsign is Missing")
        print("CALL")
        try:
            assert len(callsign) == 8
            for char in callsign:
                assert char in self.validCall
        except AssertionError:
            raise InvalidSAMEError(f"Invalid Callsign: {callsign}")
        return callsign

    def generate_alert_text(self, sameData: str):
        ## Clean up SAME data:
        sameData = sameData.strip()
        ## Checking for valid SAME codes:
        if not sameData:
            raise MissingSAMEError()
        self.sameData = sameData

        reg = r"^.*?(NNNN|ZCZC)(?:-([A-Za-z0-9]{3})-([A-Za-z0-9]{3})-((?:-?[0-9]{6})+)\+([0-9]{4})-([0-9]{7})-(.{8})-)?.*?$"
        prog = re.compile(reg, re.MULTILINE)
        groups = prog.match(self.sameData).groups()
        if groups[0] == ("NNNN"):
            self.EASText = "End Of Message"
            return "End Of Message"
        elif groups[0] != ("ZCZC"):
            raise InvalidSAMEError(f'"ZCZC" Start string missing in data {sameData}')
        else:
            eas = groups[1:]

            alertObj = EASAlert()

            orgCode = eas[0]
            orgData = self.process_originator(orgCode)
            alertObj.originatorCode = orgCode
            alertObj.originatorText = orgData["name"]

            evntCode = eas[1]
            evntData = self.process_event(event=evntCode)
            alertObj.eventCode = evntCode
            alertObj.eventText = evntData["name"]
            alertObj.eventSeverity = evntData["severity"]

            fipsCode, fipsData, fipsText = self.process_fips(eas[2])
            alertObj.fipsCode = fipsCode
            alertObj.fipsText = fipsText

            durCode = eas[3]
            durOffset = self.process_duration(durCode)
            alertObj.durationCode = durCode
            alertObj.durationOffset = durOffset

            tStampCode = eas[4]
            sEpoch, eEpoch, timeStart, timeEnd = self.process_timestamp(tStampCode, durOffset)
            alertObj.timestampCode = tStampCode
            alertObj.timeStartEpoch = sEpoch
            alertObj.timeEndEpoch = eEpoch

            call = self.process_callsign(eas[5])
            alertObj.callsign = call

            # ## FINAL TEXT
            if self.textMode == "TFT":
                timeStartText = timeStart.strftime("%I:%M %p ON %b %d, %Y")
                timeEndText = (
                    timeEnd.strftime("%I:%M %p")
                    if timeStart.day == timeEnd.day
                    else timeEnd.strftime("%I:%M %p ON %b %d, %Y")
                )
                fipsText = (
                    fipsText[:-1].replace(",", "").replace(";", ",").replace("FIPS", "AREA")
                )
                if orgCode == "EAS" or evntCode in ["NPT", "EAN"]:
                    self.EASText = f"{self.evntText} has been issued for the following counties/areas: {self.strFIPS} at {self.startTimeText} effective until {self.endTimeText}. message from {self.callsign}.".upper()
                else:
                    self.EASText = f"{self.orgText} has issued {self.evntText} for the following counties/areas: {self.strFIPS} at {self.startTimeText} effective until {self.endTimeText}. message from {self.callsign}.".upper()

            elif mode.startswith("SAGE"):
                if self.org == "CIV":
                    self.orgText = "The Civil Authorities"
                self.strFIPS = self.strFIPS[:-1].replace(";", ",")
                self.startTimeText = self.startTime.strftime("%I:%M %p").lower()
                self.endTimeText = self.endTime.strftime("%I:%M %p").lower()
                if self.startTime.day != self.endTime.day:
                    self.startTimeText += self.startTime.strftime(" %a %b %d")
                    self.endTimeText += self.endTime.strftime(" %a %b %d")
                if mode.endswith("DIGITAL"):
                    self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText} ({self.callsign})"
                else:
                    if self.org == "EAS":
                        self.orgText = "A Broadcast station or cable system"
                    self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText} ({self.callsign})"

            elif mode in ["TRILITHIC", "VIAVI", "EASY"]:
                self.strFIPS = (
                    self.strFIPS[:-1].replace(",", "").replace("; ", " - ").replace("and ", "")
                    if "000000" not in self.FIPS
                    else "The United States"
                )
                if self.strFIPS == "The United States":
                    bigFips = "for"
                else:
                    bigFips = "for the following counties:"
                self.startTimeText = ""
                self.endTimeText = self.endTime.strftime("%m/%d/%y %H:%M:00 ") + self.getTZ(
                    dtOffset
                )
                if self.org == "CIV":
                    self.orgText = "Civil Authorities"
                self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} {bigFips} {self.strFIPS}. Effective Until {self.endTimeText}. ({self.callsign})"

            elif mode in ["BURK"]:
                if self.org == "EAS":
                    self.orgText = "A Broadcast station or cable system"
                elif self.org == "CIV":
                    self.orgText = "Civil Authorities"
                elif self.org == "WXR":
                    self.orgText = "National Weather Service"
                self.strFIPS = self.strFIPS[:-1].replace(",", "").replace(";", ",")
                self.startTimeText = (
                    self.startTime.strftime("%B %d, %Y").upper()
                    + " at "
                    + self.startTime.strftime("%I:%M %p")
                )
                self.endTimeText = self.endTime.strftime("%I:%M %p, %B %d, %Y")
                self.evntText = " ".join(self.evntText.split(" ")[1:]).upper()
                self.EASText = f"{self.orgText} has issued {self.evntText} for the following counties/areas: {self.strFIPS} on {self.startTimeText} effective until {self.endTimeText}."

            elif mode in ["DAS", "DASDEC", "MONROE"]:
                self.orgText = self.orgText.upper()
                self.evntText = self.evntText.upper()
                self.startTimeText = self.startTime.strftime("%I:%M %p ON %b %d, %Y").upper()
                self.endTimeText = self.endTime.strftime("%I:%M %p %b %d, %Y").upper()
                self.EASText = f"{self.orgText} HAS ISSUED {self.evntText} FOR THE FOLLOWING COUNTIES/AREAS: {self.strFIPS} AT {self.startTimeText} EFFECTIVE UNTIL {self.endTimeText}. MESSAGE FROM {self.callsign.upper()}."

            else:
                if timeStart.day == timeEnd.day:
                    timeStartText = timeStart.strftime("%I:%M %p")
                    timeEndText = timeEnd.strftime("%I:%M %p")
                elif timeStart.year == timeEnd.year:
                    timeStartText = timeStart.strftime("%I:%M %p %B %d")
                    timeEndText = timeEnd.strftime("%I:%M %p %B %d")
                else:
                    timeStartText = timeStart.strftime("%I:%M %p %B %d, %Y")
                    timeEndText = timeEnd.strftime("%I:%M %p %B %d, %Y")
                self.EASText = f"{self.orgText} has issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText}. Message from {self.callsign}."

    @classmethod
    def get_tz(cls, tzOffset):
        tzone = int(tzOffset / 3600.0)
        locTime = localtime().tm_isdst
        TMZ = "UTC"
        if tzone == 3 and locTime > 0:
            TMZ = "ADT"
        elif tzone == 4:
            TMZ = "AST"
            if locTime > 0:
                TMZ = "EDT"
        elif tzone == 5:
            TMZ = "EST"
            if locTime > 0:
                TMZ = "CDT"
        elif tzone == 6:
            TMZ = "CST"
            if locTime > 0:
                TMZ = "MDT"
        elif tzone == 7:
            TMZ = "MST"
            if locTime > 0:
                TMZ = "PDT"
        elif tzone == 8:
            TMZ = "PST"
        return TMZ


if __name__ == "__main__":
    test = EAS2Text()
    test.process_same(
        "ZCZC-WXR-RWT-020103-020209-020091-020121-029047-029165-029095-029037+0030-3650000-KEAX/NWS-"
    )
