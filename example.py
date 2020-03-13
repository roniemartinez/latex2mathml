#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2018-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
from latex2mathml.converter import convert


def convert_to_mathml(latex_input):
    mathml_output = convert(latex_input)
    print(mathml_output)


if __name__ == "__main__":
    convert_to_mathml(r"x = {-b \pm \sqrt{b^2-4ac} \over 2a}")
