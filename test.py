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


if __name__ == "__main__":
    unittest.main()
