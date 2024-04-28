import unittest

from scouterx.common.util.strmatch import StrMatch


class TestStrMatch(unittest.TestCase):

    def test_str_match_cases(self):
        any_asta = StrMatch("*")
        start_asta = StrMatch("*HelloWorld")
        end_asta = StrMatch("HelloWorld*")
        mid_asta = StrMatch("Hello*World")
        start_mid_asta = StrMatch("*Hello*World")
        mid_end_asta = StrMatch("Hello*World*")
        start_end_asta = StrMatch("*HelloWorld*")
        complex_asta = StrMatch("*Hello*World*")
        no_asta = StrMatch("HelloWorld")

        test_cases = [
            ("Xxx", [True, False, False, False, False, False, False, False, False]),
            ("HelloWorld", [True] * 9),
            ("HelloWorldxxx", [True, False, True, False, False, True, True, True, False]),
            ("XxxHelloWorld", [True, True, False, False, True, False, True, True, False]),
            ("XxxHelloWorldXxx", [True, False, False, False, False, False, True, True, False]),
            ("HelloXxxWorldxxx", [True, False, False, False, False, True, False, True, False]),
            ("xxxHelloXxxWorldxxx", [True, False, False, False, False, False, False, True, False]),
            ("xxxHelloXxxWorld", [True, False, False, False, True, False, False, True, False])
        ]

        for test_input, expected in test_cases:
            results = [
                any_asta.include(test_input),
                start_asta.include(test_input),
                end_asta.include(test_input),
                mid_asta.include(test_input),
                start_mid_asta.include(test_input),
                mid_end_asta.include(test_input),
                start_end_asta.include(test_input),
                complex_asta.include(test_input),
                no_asta.include(test_input)
            ]
            self.assertEqual(results, expected)


if __name__ == '__main__':
    unittest.main()
