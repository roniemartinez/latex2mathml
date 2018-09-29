#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2018, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
# __status__ = "Production"
from latex2mathml.converter import convert

if __name__ == '__main__':
    latex_input = r"F_{x} = m \cdot a"
    mathml_output = convert(latex_input)
    print(mathml_output)
