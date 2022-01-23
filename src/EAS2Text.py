import json
import datetime
from datetime import datetime as DT
import time



class Utilities:

    def __init__(self) -> None:
        with open('EASData.json', 'r') as f:
	        _stats = json.load(f)

    @classmethod
    def _isInt(cls, number):
        try:
            int(number)
        except ValueError:
            return False
        else:
            return True

    @classmethod
    def toText(cls, eas):
        FIPS = []
        _strFIPS = ''
        if eas.startswith('NNNN'):
            return "End Of Message"
        _eas = ''.join(eas.split('ZCZC')[1].replace('+', '-')).split('-')
        for _i in _eas:
            if _i.strip(" ") == "":
                _eas.remove(_i)
            if len(_i) == 6 and cls._isInt(_i) and _i not in FIPS:
                FIPS.append(str(_i))
        for _i in FIPS:
            try:
                if _i == FIPS[-1] and len(FIPS) > 1:
                    _strFIPS += f"and {_stats['SUBDIV'][i[0]]+_stats['SAME'][_i[1:]]}; "
                else:
                    _strFIPS += f"{_stats['SUBDIV'][_i[0]]+_stats['SAME'][_i[1:]]}; "
            except:
                if _i == FIPS[-1] and len(FIPS) > 1:
                    _strFIPS += f"and FIPS Code {_stats['SUBDIV'][_i[0]]+_i}; "
                else:
                    _strFIPS += f"FIPS Code {_stats['SUBDIV'][_i[0]]+_i}; "
        purge = [(_eas[-3][_i:_i+2]) for _i in range(0, len(_eas[-3]), 2)]
        timeStamp = _eas[-2]
        _dtOffset = time.mktime(DT.utcnow().timetuple())-time.mktime(DT.now().timetuple())
        _x = DT.strptime(timeStamp, '%j%H%M')
        _test = time.mktime(DT(DT.utcnow().year, _x.month, _x.day, _x.hour, _x.minute).timetuple())+_dtOffset
        _test2 = time.localtime(_test)
        if _test2.tm_hour >= 12:
            _validhour2 = _test2.tm_hour-12
            _ampm = ' PM'
        else:
            _validhour2 = _test2.tm_hour
            _ampm = ' AM'
        _validminute = _test2.tm_min
        if _validhour2 == 0:
            _validhour2 = 12
        BEGINNING = f"{str(_validhour2)}:{str(_validminute).rjust(2,'0')}{_ampm} {datetime.date(1900, _test2.tm_mon, 1).strftime('%B')} {str(_test2.tm_mday)}, {_test2.tm_year}"
        endtime = (int(purge[1])*60)+((int(purge[0])*60)*60)
        test2 = time.localtime(test+endtime)
        if test2.tm_hour >= 12:
            validhour2 = test2.tm_hour-12
            if validhour2 == 0:
                validhour2 = 12
            ampm = ' PM'
            validminute = test2.tm_min
        else:
            validhour2 = test2.tm_hour
            if validhour2 == 0:
                validhour2 = 12
            ampm = ' AM'
            validminute = test2.tm_min
        ENDING = f"{str(validhour2)}:{str(validminute).rjust(2,'0')}{ampm} {datetime.date(1900, test2.tm_mon, 1).strftime('%B')} {str(test2.tm_mday)}, {test2.tm_year}"
        try:
            org = stats["ORGS"][eas[0]]
        except:
            org = "An Unknown Originator ("+str(eas[0])+") has issued "
        try:
            evn = stats["EVENTS"][eas[1]]
        except:
            evn = "an Unknown Event ("+str(eas[1])+")"

        eas[0]
        eas[1]
        org
        evn
        FIPS
        strFIPS
        Purge
        timeStamp
        BEGINNING
        ENDING


        return f"{org}{evn} for {strFIPS}beginning at {BEGINNING} and ending at {ENDING}. Message from {eas[-1].strip()}."