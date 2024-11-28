# Standard Library
from datetime import datetime as DT
from json import loads
from time import localtime, timezone


class EAS2Text(object):

    def __init__(
        self, sameData: str, timeZone: int = None, mode: str = "NONE"
    ) -> None:
        sameData = (
            sameData.strip()
        )  ## Strip to get rid of leading / trailing newlines and spaces (You're welcome, Don / Kane.)
        stats = loads(self.__data__)
        self.FIPS = []
        self.FIPSText = []
        self.strFIPS = ""
        self.EASData = sameData

        ## CHECKING FOR VALID SAME
        if sameData == "":
            raise MissingSAME()
        elif sameData.startswith("NNNN"):
            self.EASText = "End Of Message"
            return
        elif not sameData.startswith("ZCZC"):
            raise InvalidSAME(sameData, message='"ZCZC" Start string missing')
        else:
            eas = "".join(
                sameData.replace("ZCZC-", "").replace("+", "-")
            ).split("-")
            eas.remove("")

            for i in eas[2:-3]:
                try:
                    assert len(i) == 6
                    assert self.__isInt__(i) == True
                    ## FIPS CODE
                    if i not in self.FIPS:
                        self.FIPS.append(str(i))
                except AssertionError:
                    raise InvalidSAME("Invalid codes in FIPS data")

            for i in sorted(self.FIPS):
                try:
                    subdiv = stats["SUBDIV"][i[0]]
                    same = stats["SAME"][i[1:]]
                    self.FIPSText.append(
                        f"{subdiv + ' ' if subdiv != '' else ''}{same}"
                    )
                except KeyError:
                    self.FIPSText.append(f"FIPS Code {i}")
                except Exception as E:
                    raise InvalidSAME(
                        self.FIPS, message=f"Error in FIPS Code ({str(E)})"
                    )
            if len(self.FIPSText) > 1:
                FIPSText = self.FIPSText
                FIPSText[-1] = f"and {FIPSText[-1]}"
            self.strFIPS = "; ".join(self.FIPSText).strip() + ";"

            ## TIME CODE
            try:
                self.purge = [eas[-3][:2], eas[-3][2:]]
            except IndexError:
                raise InvalidSAME(self.purge, message="Purge Time not HHMM.")
            self.timeStamp = eas[-2]
            utc = DT.utcnow()
            if timeZone == None:
                dtOffset = utc.timestamp() - DT.now().timestamp()
            else:
                dtOffset = -timeZone * 3600

            try:
                alertStartEpoch = (
                    DT.strptime(self.timeStamp, "%j%H%M")
                    .replace(year=utc.year)
                    .timestamp()
                )
            except ValueError:
                raise InvalidSAME(
                    self.timeStamp, message="Timestamp not JJJHHMM."
                )
            alertEndOffset = (int(self.purge[0]) * 3600) + (
                int(self.purge[1]) * 60
            )
            alertEndEpoch = alertStartEpoch + alertEndOffset

            try:
                self.startTime = DT.fromtimestamp(alertStartEpoch - dtOffset)
                self.endTime = DT.fromtimestamp(alertEndEpoch - dtOffset)
                if self.startTime.day == self.endTime.day:
                    self.startTimeText = self.startTime.strftime("%I:%M %p")
                    self.endTimeText = self.endTime.strftime("%I:%M %p")
                elif self.startTime.year == self.endTime.year:
                    self.startTimeText = self.startTime.strftime(
                        "%I:%M %p %B %d"
                    )
                    self.endTimeText = self.endTime.strftime("%I:%M %p %B %d")
                else:
                    self.startTimeText = self.startTime.strftime(
                        "%I:%M %p %B %d, %Y"
                    )
                    self.endTimeText = self.endTime.strftime(
                        "%I:%M %p %B %d, %Y"
                    )
            except Exception as E:
                raise InvalidSAME(
                    self.timeStamp,
                    message=f"Error in Time Conversion ({str(E)})",
                )

            ## ORG / EVENT CODE
            try:
                self.org = str(eas[0])
                self.evnt = str(eas[1])
                try:
                    assert len(eas[0]) == 3
                except AssertionError:
                    raise InvalidSAME("Originator is an invalid length")
                try:
                    assert len(eas[1]) == 3
                except AssertionError:
                    raise InvalidSAME("Event Code is an invalid length")
                try:
                    self.orgText = stats["ORGS"][self.org]
                except:
                    self.orgText = (
                        f"An Unknown Originator ({self.org}) has issued "
                    )
                try:
                    self.evntText = stats["EVENTS"][self.evnt]
                except:
                    self.evntText = f"an Unknown Event ({self.evnt})"
            except Exception as E:
                raise InvalidSAME(
                    [self.org, self.evnt],
                    message=f"Error in ORG / EVNT Decoding ({str(E)})",
                )

            ## CALLSIGN CODE"
            self.callsign = eas[-1].strip()

            ## FINAL TEXT
            if mode == "TFT":
                self.strFIPS = (
                    self.strFIPS[:-1]
                    .replace(",", "")
                    .replace(";", ",")
                    .replace("FIPS Code", "AREA")
                )
                self.startTimeText = self.startTime.strftime(
                    "%I:%M %p ON %b %d, %Y"
                )
                self.endTimeText = (
                    self.endTime.strftime("%I:%M %p")
                    if self.startTime.day == self.endTime.day
                    else self.endTime.strftime("%I:%M %p ON %b %d, %Y")
                )
                if self.org == "EAS" or self.evnt in ["NPT", "EAN"]:
                    self.EASText = f"{self.evntText} has been issued for the following counties/areas: {self.strFIPS} at {self.startTimeText} effective until {self.endTimeText}. message from {self.callsign}.".upper()
                else:
                    self.EASText = f"{self.orgText} has issued {self.evntText} for the following counties/areas: {self.strFIPS} at {self.startTimeText} effective until {self.endTimeText}. message from {self.callsign}.".upper()

            elif mode.startswith("SAGE"):
                if self.org == "CIV":
                    self.orgText = "The Civil Authorities"
                self.strFIPS = self.strFIPS[:-1].replace(";", ",")
                self.startTimeText = self.startTime.strftime(
                    "%I:%M %p"
                ).lower()
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
                    self.strFIPS[:-1]
                    .replace(",", "")
                    .replace("; ", " - ")
                    .replace("and ", "")
                    if "000000" not in self.FIPS
                    else "The United States"
                )
                if self.strFIPS == "The United States":
                    bigFips = "for"
                else:
                    bigFips = "for the following counties:"
                self.startTimeText = ""
                self.endTimeText = self.endTime.strftime(
                    "%m/%d/%y %H:%M:00 "
                ) + self.getTZ(dtOffset)
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
                self.strFIPS = (
                    self.strFIPS[:-1].replace(",", "").replace(";", ",")
                )
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
                self.startTimeText = self.startTime.strftime(
                    "%I:%M %p ON %b %d, %Y"
                ).upper()
                self.endTimeText = self.endTime.strftime(
                    "%I:%M %p %b %d, %Y"
                ).upper()
                self.EASText = f"{self.orgText} HAS ISSUED {self.evntText} FOR THE FOLLOWING COUNTIES/AREAS: {self.strFIPS} AT {self.startTimeText} EFFECTIVE UNTIL {self.endTimeText}. MESSAGE FROM {self.callsign.upper()}."

            else:
                self.EASText = f"{self.orgText} has issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText}. Message from {self.callsign}."

    @classmethod
    def __isInt__(cls, number):
        try:
            int(number)
        except ValueError:
            return False
        else:
            return True

    @classmethod
    def getTZ(cls, tzOffset):
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
