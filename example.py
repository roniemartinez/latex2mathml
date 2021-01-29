from latex2mathml.converter import convert


def convert_to_mathml(latex_input):
    mathml_output = convert(latex_input)
    print(mathml_output)


if __name__ == "__main__":
    convert_to_mathml(r"x = {-b \pm \sqrt{b^2-4ac} \over 2a}")
