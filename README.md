<table>
    <tr>
        <td>License</td>
        <td><img src='https://img.shields.io/pypi/l/latex2mathml.svg?style=for-the-badge' alt="License"></td>
        <td>Version</td>
        <td><img src='https://img.shields.io/pypi/v/latex2mathml.svg?logo=pypi&style=for-the-badge' alt="Version"></td>
    </tr>
    <tr>
        <td>Github Actions</td>
        <td><img src='https://img.shields.io/github/workflow/status/roniemartinez/latex2mathml/Python?label=actions&logo=github%20actions&style=for-the-badge' alt="Github Actions"></td>
        <td>Coverage</td>
        <td><img src='https://img.shields.io/codecov/c/github/roniemartinez/latex2mathml/branch?label=codecov&logo=codecov&style=for-the-badge' alt="CodeCov"></td>
    </tr>
    <tr>
        <td>Supported versions</td>
        <td><img src='https://img.shields.io/pypi/pyversions/latex2mathml.svg?logo=python&style=for-the-badge' alt="Python Versions"></td>
        <td>Wheel</td>
        <td><img src='https://img.shields.io/pypi/wheel/latex2mathml.svg?style=for-the-badge' alt="Wheel"></td>
    </tr>
    <tr>
        <td>Status</td>
        <td><img src='https://img.shields.io/pypi/status/latex2mathml.svg?style=for-the-badge' alt="Status"></td>
        <td>Downloads</td>
        <td><img src='https://img.shields.io/pypi/dm/latex2mathml.svg?style=for-the-badge' alt="Downloads"></td>
    </tr>
</table>

# latex2mathml

Pure Python library for LaTeX to MathML conversion

## Installation

```bash
pip install latex2mathml
```

## Usage

### Python

```python
import latex2mathml.converter

latex_input = "<your_latex_string>"
mathml_output = latex2mathml.converter.convert(latex_input)
```

### Command-line

```shell
% latex2mathml -h
usage: latex2mathml [-h] [-V] [-b] [-t TEXT | -f FILE]

Pure Python library for LaTeX to MathML conversion

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Show version
  -b, --block           Display block

required arguments:
  -t TEXT, --text TEXT  Text
  -f FILE, --file FILE  File
```

## References
### LaTeX

- https://en.wikibooks.org/wiki/LaTeX/Mathematics
- http://artofproblemsolving.com/wiki/index.php?title=Main_Page
- http://milde.users.sourceforge.net/LUCR/Math/
- https://math-linux.com/latex-26/faq/latex-faq/article/latex-derivatives-limits-sums-products-and-integrals
- https://www.tutorialspoint.com/tex_commands
- https://www.giss.nasa.gov/tools/latex/ltx-86.html
- https://ftp.gwdg.de/pub/ctan/info/l2tabu/english/l2tabuen.pdf

### MathML

- http://www.xmlmind.com/tutorials/MathML/


## Author

- [Ronie Martinez](mailto:ronmarti18@gmail.com)
