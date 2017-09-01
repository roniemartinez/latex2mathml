#!/usr/bin/env python
import unittest
from latex2mathml import tokenizer

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2016-2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Development"


class TokenizerTest(unittest.TestCase):

    def test_alphabets(self):
        alphabets = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.assertListEqual(list(alphabets), list(tokenizer.tokenize(alphabets)))

    def test_numbers(self):
        numbers = '1234567890'
        self.assertListEqual([numbers], list(tokenizer.tokenize(numbers)))

    def test_numbers_with_decimals(self):
        decimal = '12.56'
        self.assertListEqual([decimal], list(tokenizer.tokenize(decimal)))

    def test_numbers_and_alphabets(self):
        string = '5x'
        self.assertListEqual(list(string), list(tokenizer.tokenize(string)))

    def test_decimals_and_alphabets(self):
        string = '5.8x'
        self.assertListEqual(['5.8', 'x'], list(tokenizer.tokenize(string)))

    def test_string_with_spaces(self):
        string = '3 x'
        self.assertListEqual(['3', 'x'], list(tokenizer.tokenize(string)))

    def test_operators(self):
        string = '+-*/=()[]_^{}'
        self.assertListEqual(list(string), list(tokenizer.tokenize(string)))

    def test_numbers_alphabets_and_operators(self):
        string = '3 + 5x - 5y = 7'
        self.assertListEqual(['3', '+', '5', 'x', '-', '5', 'y', '=', '7'], list(
            tokenizer.tokenize(string)))

    def test_symbols(self):
        string = r'\alpha\beta'
        self.assertListEqual([r'\alpha', r'\beta'], list(tokenizer.tokenize(string)))

    def test_symbols_appended_number(self):
        string = r'\frac2x'
        self.assertListEqual([r'\frac', '2', 'x'], list(tokenizer.tokenize(string)))

    def test_matrix(self):
        self.assertListEqual([r'\matrix', '{', 'a', '&', 'b', r'\\', 'c', '&', 'd', '}'],
                             list(tokenizer.tokenize(r'\begin{matrix}a & b \\ c & d \end{matrix}')))

    def test_matrix_with_alignment(self):
        self.assertListEqual([r'\matrix*', 'r', '{', 'a', '&', 'b', r'\\', 'c', '&', 'd', '}'],
                             list(tokenizer.tokenize(r'\begin{matrix*}[r]a & b \\ c & d \end{matrix*}')))

    def test_matrix_with_negative_sign(self):
        self.assertListEqual([r'\matrix', '{', '-', 'a', '&', 'b', r'\\', 'c', '&', 'd', '}'],
                             list(tokenizer.tokenize(r'\begin{matrix}-a & b \\ c & d \end{matrix}')))

    def test_simple_array(self):
        self.assertListEqual([r'\array', 'cc', '{', '1', '&', '2', r'\\', '3', '&', '4', '}'],
                             list(tokenizer.tokenize(r'\begin{array}{cc} 1 & 2 \\ 3 & 4 \end{array}''')))

if __name__ == '__main__':
    unittest.main(verbosity=2)
