import unittest
from datetime import datetime

from util.utils import extract_datetime_from_filename


class TestExtractDatetime(unittest.TestCase):

    def test_valid_filenames(self):
        test_cases = [
            ("IMG_20170930_193512.jpg", datetime(2017, 9, 30, 19, 35, 12)),
            ("PANO_20180109_194651.jpg", datetime(2018, 1, 9, 19, 46, 51)),
            ("20180412_105603-COLLAGE.jpg", datetime(2018, 4, 12, 10, 56, 3)),
            ("2016-06-17 Invoice Parking Antwerp.jpg", datetime(2016, 6, 17)),
            ("2018_12_23_11_41_50_931.jpg", datetime(2018, 12, 23, 11, 41, 50)),
            ("2018_12_23_11_42_06_933.jpg", datetime(2018, 12, 23, 11, 42, 6)),
            ("WP_20160612_17_08_11_Pro.jpg", datetime(2016, 6, 12, 17, 8, 11)),
            ("041020111108.jpg", datetime(2011, 4, 10, 11, 8)),
            ("070620101530.jpg", datetime(2010, 7, 6, 15, 30)),
            ("20130620_221216.jpg", datetime(2013, 6, 20, 22, 12, 16)),
            ("20230610_151233.jpg", datetime(2023, 6, 10, 15, 12, 33)),
            ("09102023123456.jpg", datetime(2023, 9, 10, 12, 34, 56)),
            ("12102016123456.jpg", datetime(2016, 12, 10, 12, 34, 56)),
            ("IMG_20230610_151233.jpg", datetime(2023, 6, 10, 15, 12, 33)),
        ]

        for filename, expected in test_cases:
            with self.subTest(filename=filename):
                result = extract_datetime_from_filename(filename)
                self.assertEqual(result, expected)

    def test_invalid_filenames(self):
        test_cases = [
            "NoDateHere.jpg",
            "JustSomeText.txt",
            "1234",
            "041020113733.jpg",
            "IMG_99999999_999999.jpg",
            "IMG_20171330_193512.jpg",
            "IMG_20170931_193512.jpg",
        ]

        for filename in test_cases:
            with self.subTest(filename=filename):
                result = extract_datetime_from_filename(filename)
                self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
