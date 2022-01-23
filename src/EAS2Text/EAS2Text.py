import json
import datetime
from datetime import datetime as DT
import time

class EAS2Text(object):

    def __init__(self, RawEASData:str) -> None:
        with open('EASData.json', 'r') as f:
            stats = json.load(f)
        self.FIPS = []
        self.FIPSText = []
        strFIPS = ''
        self.EASData = RawEASData
        if RawEASData.startswith('NNNN'):
            return "End Of Message"
        eas = ''.join(RawEASData.split('ZCZC')[1].replace('+', '-')).split('-')
        for i in eas:
            if i.strip(" ") == "":
                eas.remove(i)
            if len(i) == 6 and self.__isInt__(i) and i not in self.FIPS:
                self.FIPS.append(str(i))
        for i in self.FIPS:
            try:
                if i == self.FIPS[-1] and len(self.FIPS) > 1:
                    strFIPS += f"and {stats['SUBDIV'][i[0]]}{stats['SAME'][i[1:]]}; "
                    self.FIPSText.append(f"{stats['SUBDIV'][i[0]]} {stats['SAME'][i[1:]]}")
                else:
                    strFIPS += f"{stats['SUBDIV'][i[0]]} {stats['SAME'][i[1:]]}; "
                    self.FIPSText.append(f"{stats['SUBDIV'][i[0]]} {stats['SAME'][i[1:]]}")
            except:
                if i == self.FIPS[-1] and len(self.FIPS) > 1:
                    strFIPS += f"and FIPS Code {i}; "
                    self.FIPSText.append(f"FIPS Code {i}")
                else:
                    strFIPS += f"FIPS Code {i}; "
                    self.FIPSText.append(f"FIPS Code {i}")
        self.purge = [(eas[-3][i:i+2]) for i in range(0, len(eas[-3]), 2)]
        self.timeStamp = eas[-2]
        dtOffset = time.mktime(DT.utcnow().timetuple())-time.mktime(DT.now().timetuple())
        alertStartTime = DT.strptime(self.timeStamp, '%j%H%M')
        alertStartEpoch = time.mktime(DT(DT.utcnow().year, alertStartTime.month, alertStartTime.day, alertStartTime.hour, alertStartTime.minute).timetuple())+dtOffset
        alertEndEpochOffset = (int(self.purge[1])*60)+((int(self.purge[0])*60)*60)
        alertLocalTime = time.localtime(alertStartEpoch)
        if alertLocalTime.tm_hour >= 12:
            validhour2 = alertLocalTime.tm_hour-12
            ampm = ' PM'
        else:
            validhour2 = alertLocalTime.tm_hour
            ampm = ' AM'
        validminute = alertLocalTime.tm_min
        if validhour2 == 0:
            validhour2 = 12
        self.startTimeText = f"{str(validhour2)}:{str(validminute).rjust(2,'0')}{ampm} {datetime.date(1900, alertLocalTime.tm_mon, 1).strftime('%B')} {str(alertLocalTime.tm_mday)}, {alertLocalTime.tm_year}"
        alertLocalTime = time.localtime(alertStartEpoch+alertEndEpochOffset)
        if alertLocalTime.tm_hour >= 12:
            validhour2 = alertLocalTime.tm_hour-12
            if validhour2 == 0:
                validhour2 = 12
            ampm = ' PM'
            validminute = alertLocalTime.tm_min
        else:
            validhour2 = alertLocalTime.tm_hour
            if validhour2 == 0:
                validhour2 = 12
            ampm = ' AM'
            validminute = alertLocalTime.tm_min
        self.endTimeText = f"{str(validhour2)}:{str(validminute).rjust(2,'0')}{ampm} {datetime.date(1900, alertLocalTime.tm_mon, 1).strftime('%B')} {str(alertLocalTime.tm_mday)}, {alertLocalTime.tm_year}"
        self.org = str(eas[0])
        self.evnt = str(eas[1])
        try:
            self.orgText = stats["ORGS"][self.org]
        except:
            self.orgText = "An Unknown Originator ("+self.org+") has issued "
        try:
            self.evntText = stats["EVENTS"][self.evnt]
        except:
            self.evntText = "an Unknown Event ("+self.evnt+")"

        self.callsign = eas[-1].strip()

        self.EASText =  f"{self.orgText} has issued {self.evntText} for {strFIPS}beginning at {self.startTimeText} and ending at {self.endTimeText}. Message from {self.callsign}."

    @classmethod
    def __isInt__(cls, number):
        try:
            int(number)
        except ValueError:
            return False
        else:
            return True

