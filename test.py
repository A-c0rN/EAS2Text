# Standard Library
import unittest

# First-Party
from EAS2Text import EAS2Text


class TestEAS2Text(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.EASString = "ZCZC-EAS-RWT-055079+0015-0012345-SOFTTEST-"
        cls.EASData = EAS2Text(cls.EASString)

    def testRawOrg(self):
        self.assertIsNotNone(self.EASData.org, "Raw Originator Code Missing!")
        self.assertIsInstance(
            self.EASData.org, str, "Raw Originator Code Not String!"
        )
        self.assertEqual(
            self.EASData.org, "EAS", "Raw Originator Code Incorrect!"
        )

    def testRawEvnt(self):
        self.assertIsNotNone(self.EASData.evnt, "Raw Event Code Missing!")
        self.assertIsInstance(
            self.EASData.evnt, str, "Raw Event Code Not String!"
        )
        self.assertEqual(self.EASData.evnt, "RWT", "Raw Event Code Incorrect!")

    def testRawFips(self):
        self.assertIsNotNone(self.EASData.FIPS, "Raw FIPS Code(s) Missing!")
        self.assertIsInstance(
            self.EASData.FIPS, list, "Raw FIPS Code(s) Not List!"
        )
        self.assertEqual(
            self.EASData.FIPS, ["055079"], "Raw FIPS Code(s) Incorrect!"
        )

    def testRawPurge(self):
        self.assertIsNotNone(self.EASData.purge, "Raw Purge Time Missing!")
        self.assertIsInstance(
            self.EASData.purge, list, "Raw Purge Time Not List!"
        )
        self.assertEqual(
            self.EASData.purge, ["00", "15"], "Raw Purge Time Incorrect!"
        )

    def testRawTimeStamp(self):
        self.assertIsNotNone(self.EASData.timeStamp, "Raw Time Stamp Missing!")
        self.assertIsInstance(
            self.EASData.timeStamp, str, "Raw Time Stamp Not String!"
        )
        self.assertEqual(
            self.EASData.timeStamp, "0012345", "Raw Time Stamp Incorrect!"
        )

    def testRawCallsign(self):
        self.assertIsNotNone(self.EASData.callsign, "Callsign Missing!")
        self.assertIsInstance(
            self.EASData.callsign, str, "Callsign Not String!"
        )
        self.assertEqual(
            self.EASData.callsign, "SOFTTEST", "Callsign Incorrect!"
        )


def main():
    SAME_Events = {
        "**A": {
            "name": "Unknown Watch",
            "article": "An",
            "severity": "Watch",
        },
        "**E": {
            "name": "Unknown Emergency",
            "article": "An",
            "severity": "Emergency",
        },
        "**S": {
            "name": "Unknown Statement",
            "article": "An",
            "severity": "Statement",
        },
        "**T": {
            "name": "Unknown Test",
            "article": "An",
            "severity": "Statement",
        },
        "**W": {
            "name": "Unknown Warning",
            "article": "An",
            "severity": "Warning",
        },
        "ADR": {
            "name": "Administrative Message",
            "article": "An",
            "severity": "Statement",
        },
        "AVA": {
            "name": "Avalanche Watch",
            "article": "An",
            "severity": "Watch",
        },
        "AVW": {
            "name": "Avalanche Warning",
            "article": "An",
            "severity": "Warning",
        },
        "BHW": {
            "name": "Biological Hazard Warning",
            "article": "A",
            "severity": "Warning",
        },
        "BLU": {
            "name": "Blue Alert",
            "article": "A",
            "severity": "Warning",
        },
        "BWW": {
            "name": "Boil Water Warning",
            "article": "A",
            "severity": "Warning",
        },
        "BZW": {
            "name": "Blizzard Warning",
            "article": "A",
            "severity": "Warning",
        },
        "CAE": {
            "name": "Child Abduction Emergency",
            "article": "A",
            "severity": "Emergency",
        },
        "CDW": {
            "name": "Civil Danger Warning",
            "article": "A",
            "severity": "Warning",
        },
        "CEM": {
            "name": "Civil Emergency Message",
            "article": "A",
            "severity": "Warning",
        },
        "CFA": {
            "name": "Coastal Flood Watch",
            "article": "A",
            "severity": "Watch",
        },
        "CFW": {
            "name": "Coastal Flood Warning",
            "article": "A",
            "severity": "Warning",
        },
        "CHW": {
            "name": "Chemical Hazard Warning",
            "article": "A",
            "severity": "Warning",
        },
        "CWW": {
            "name": "Contaminated Water Warning",
            "article": "A",
            "severity": "Warning",
        },
        "DBA": {
            "name": "Dam Watch",
            "article": "A",
            "severity": "Watch",
        },
        "DBW": {
            "name": "Dam Break Warning",
            "article": "A",
            "severity": "Warning",
        },
        "DEW": {
            "name": "Contagious Disease Warning",
            "article": "A",
            "severity": "Warning",
        },
        "DMO": {
            "name": "Practice/Demo Warning",
            "article": "A",
            "severity": "Statement",
        },
        "DSW": {
            "name": "Dust Storm Warning",
            "article": "A",
            "severity": "Warning",
        },
        "EAN": {
            "name": "National Emergency Message",
            "article": "A",
            "severity": "Emergency",
        },
        "EAT": {
            "name": "Emergency Action Termination",
            "article": "An",
            "severity": "Statement",
        },
        "EQW": {
            "name": "Earthquake Warning",
            "article": "A",
            "severity": "Warning",
        },
        "EVA": {
            "name": "Evacuation Watch",
            "article": "An",
            "severity": "Watch",
        },
        "EVI": {
            "name": "Immediate Evacuation",
            "article": "An",
            "severity": "Warning",
        },
        "EWW": {
            "name": "Extreme Wind Warning",
            "article": "An",
            "severity": "Warning",
        },
        "FCW": {
            "name": "Food Contamination Warning",
            "article": "A",
            "severity": "Warning",
        },
        "FFA": {
            "name": "Flash Flood Watch",
            "article": "A",
            "severity": "Watch",
        },
        "FFS": {
            "name": "Flash Flood Statement",
            "article": "A",
            "severity": "Statement",
        },
        "FFW": {
            "name": "Flash Flood Warning",
            "article": "A",
            "severity": "Warning",
        },
        "FLA": {"name": "Flood Watch", "article": "A", "severity": "Watch"},
        "FLS": {
            "name": "Flood Statement",
            "article": "A",
            "severity": "Statement",
        },
        "FLW": {
            "name": "Flood Warning",
            "article": "A",
            "severity": "Warning",
        },
        "FRW": {
            "name": "Fire Warning",
            "article": "A",
            "severity": "Warning",
        },
        "FSW": {
            "name": "Flash Freeze Warning",
            "article": "A",
            "severity": "Warning",
        },
        "FZW": {
            "name": "Freeze Warning",
            "article": "A",
            "severity": "Warning",
        },
        "HLS": {
            "name": "Hurricane Statement",
            "article": "A",
            "severity": "Statement",
        },
        "HMW": {
            "name": "Hazardous Materials Warning",
            "article": "A",
            "severity": "Warning",
        },
        "HUA": {
            "name": "Hurricane Watch",
            "article": "A",
            "severity": "Watch",
        },
        "HUW": {
            "name": "Hurricane Warning",
            "article": "A",
            "severity": "Warning",
        },
        "HWA": {
            "name": "High Wind Watch",
            "article": "A",
            "severity": "Watch",
        },
        "HWW": {
            "name": "High Wind Warning",
            "article": "A",
            "severity": "Warning",
        },
        "IBW": {
            "name": "Iceberg Warning",
            "article": "An",
            "severity": "Warning",
        },
        "IFW": {
            "name": "Industrial Fire Warning",
            "article": "An",
            "severity": "Warning",
        },
        "LAE": {
            "name": "Local Area Emergency",
            "article": "A",
            "severity": "Emergency",
        },
        "LEW": {
            "name": "Law Enforcement Warning",
            "article": "A",
            "severity": "Warning",
        },
        "LSW": {
            "name": "Land Slide Warning",
            "article": "A",
            "severity": "Warning",
        },
        "NAT": {
            "name": "National Audible Test",
            "article": "A",
            "severity": "Statement",
        },
        "NIC": {
            "name": "National Information Center",
            "article": "A",
            "severity": "Statement",
        },
        "NMN": {
            "name": "Network Message Notification",
            "article": "A",
            "severity": "Statement",
        },
        "NPT": {
            "name": "Nationwide Test of the Emergency Alert System",
            "article": "A",
            "severity": "Statement",
        },
        "NST": {
            "name": "National Silent Test",
            "article": "A",
            "severity": "Statement",
        },
        "NUW": {
            "name": "Nuclear Plant Warning",
            "article": "A",
            "severity": "Warning",
        },
        "POS": {
            "name": "Power Outage Statement",
            "article": "A",
            "severity": "Statement",
        },
        "RHW": {
            "name": "Radiological Hazard Warning",
            "article": "A",
            "severity": "Warning",
        },
        "RMT": {
            "name": "Required Monthly Test",
            "article": "A",
            "severity": "Statement",
        },
        "RWT": {
            "name": "Required Weekly Test",
            "article": "A",
            "severity": "Statement",
        },
        "SCS": {
            "name": "School Closing Statement",
            "article": "A",
            "severity": "Statement",
        },
        "SMW": {
            "name": "Special Marine Warning",
            "article": "A",
            "severity": "Warning",
        },
        "SPS": {
            "name": "Special Weather Statement",
            "article": "A",
            "severity": "Statement",
        },
        "SPW": {
            "name": "Shelter In Place Warning",
            "article": "A",
            "severity": "Warning",
        },
        "SQW": {
            "name": "Snow Squall Warning",
            "article": "A",
            "severity": "Warning",
        },
        "SSA": {
            "name": "Storm Surge Watch",
            "article": "A",
            "severity": "Watch",
        },
        "SSW": {
            "name": "Storm Surge Warning",
            "article": "A",
            "severity": "Warning",
        },
        "SVA": {
            "name": "Severe Thunderstorm Watch",
            "article": "A",
            "severity": "Watch",
        },
        "SVR": {
            "name": "Severe Thunderstorm Warning",
            "article": "A",
            "severity": "Warning",
        },
        "SVS": {
            "name": "Severe Weather Statement",
            "article": "A",
            "severity": "Statement",
        },
        "TOA": {
            "name": "Tornado Watch",
            "article": "A",
            "severity": "Watch",
        },
        "TOE": {
            "name": "911 Telephone Outage Emergency",
            "article": "A",
            "severity": "Emergency",
        },
        "TOR": {
            "name": "Tornado Warning",
            "article": "A",
            "severity": "Warning",
        },
        "TRA": {
            "name": "Tropical Storm Watch",
            "article": "A",
            "severity": "Watch",
        },
        "TRW": {
            "name": "Tropical Storm Warning",
            "article": "A",
            "severity": "Warning",
        },
        "TSA": {
            "name": "Tsunami Watch",
            "article": "A",
            "severity": "Watch",
        },
        "TSW": {
            "name": "Tsunami Warning",
            "article": "A",
            "severity": "Warning",
        },
        "TXB": {
            "name": "Transmitter Backup On",
            "article": "A",
            "severity": "Statement",
        },
        "TXF": {
            "name": "Transmitter Carrier Off",
            "article": "A",
            "severity": "Statement",
        },
        "TXO": {
            "name": "Transmitter Carrier On",
            "article": "A",
            "severity": "Statement",
        },
        "TXP": {
            "name": "Transmitter Primary On",
            "article": "A",
            "severity": "Statement",
        },
        "VOA": {
            "name": "Volcano Watch",
            "article": "A",
            "severity": "Watch",
        },
        "VOW": {
            "name": "Volcano Warning",
            "article": "A",
            "severity": "Warning",
        },
        "WFA": {
            "name": "Wild Fire Watch",
            "article": "A",
            "severity": "Watch",
        },
        "WFW": {
            "name": "Wild Fire Warning",
            "article": "A",
            "severity": "Warning",
        },
        "WSA": {
            "name": "Winter Storm Watch",
            "article": "A",
            "severity": "Watch",
        },
        "WSW": {
            "name": "Winter Storm Warning",
            "article": "A",
            "severity": "Warning",
        },
    }
    translator = Translator()
    print("{")
    for name in SAME_Events.keys():
        print(f'  "{name}": ', end="")
        print("{")
        print(
            f'    "name": "{translator.translate(SAME_Events[name]["name"], dest="es").text}",'
        )
        print(f'    "severity": "{SAME_Events[name]["severity"]}"')
        print("  },")
    print("}")


if __name__ == "__main__":
    # unittest.main()
    # Third-Party
    from googletrans import Translator

    main()
