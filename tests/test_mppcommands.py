import unittest
from mppsolar import mppcommands


class test_mppcommands(unittest.TestCase):
    def testOne(self):
        mp = mpcommands.mppCommands('/dev/ttyUSB0')
        mp.getKnownCommands()
        return True
