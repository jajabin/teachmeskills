import unittest
import server


class SayByeTest(unittest.TestCase):

    def test_good_night(self):
        for i in range(0, 6):
            self.assertEqual("Goodnight!", server.say_bye(i))

        self.assertEqual("Goodnight!", server.say_bye(23))

    def test_good_morning(self):
        for i in range(6, 12):
            self.assertEqual("Good Morning!", server.say_bye(i))

    def test_good_day(self):
        for i in range(12, 18):
            self.assertEqual("Have a nice day!", server.say_bye(i))

    def test_good_evening(self):
        for i in range(18, 23):
            self.assertEqual("Good Evening!", server.say_bye(i))

    def test_invalid_value(self):
        self.assertEqual("Invalid value.", server.say_bye(24))
        self.assertEqual("Invalid value.", server.say_bye(-1))
        self.assertEqual("Invalid value.", server.say_bye(100))