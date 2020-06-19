import unittest
import server
from datetime import datetime


class GetYearTest(unittest.TestCase):

    def test_valid_ages(self):
        ages_for_2020 = (
            (0, '2020'),
            (1, '2019'),
            (20, '2000'),
            (100, '1920'),
        )

        for age, expected_year in ages_for_2020:
            qs = {"age": [age]}
            self.assertEqual(expected_year, server.get_year(qs))

    def test_invalid_ages(self):
        qs = {}
        self.assertEqual("Unknown", server.get_year(qs))

        qs = {"age": [-7]}
        self.assertEqual("Unknown", server.get_year(qs))