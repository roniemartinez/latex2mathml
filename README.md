# latex2mathml

Pure Python library for LaTeX to MathML conversion

<table>
    <tr>
        <td>License</td>
        <td><img src='https://img.shields.io/pypi/l/latex2mathml.svg' alt="License"></td>
        <td>Version</td>
        <td><img src='https://img.shields.io/pypi/v/latex2mathml.svg' alt="Version"></td>
    </tr>
    <tr>
        <td>Travis CI</td>
        <td><img src='https://www.travis-ci.com/roniemartinez/latex2mathml.svg?branch=master' alt="Travis CI"></td>
        <td>Coverage</td>
        <td><img src='https://codecov.io/gh/roniemartinez/latex2mathml/branch/master/graph/badge.svg' alt="CodeCov"></td>
    </tr>
    <tr>
        <td>Supported versions</td>
        <td><img src='https://img.shields.io/pypi/pyversions/latex2mathml.svg' alt="Python Versions"></td>
        <td>Wheel</td>
        <td><img src='https://img.shields.io/pypi/wheel/latex2mathml.svg' alt="Wheel"></td>
    </tr>
    <tr>
        <td>Status</td>
        <td><img src='https://img.shields.io/pypi/status/latex2mathml.svg' alt="Status"></td>
        <td>Downloads</td>
        <td><img src='https://img.shields.io/pypi/dm/latex2mathml.svg' alt="Downloads"></td>
    </tr>
</table>

## Support
If you like `latex2mathml` or if it is useful to you, show your support by buying me a coffee.

<a href="https://www.buymeacoffee.com/roniemartinez" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

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
usage: l2m [-h] [-V] [-b] [-t TEXT | -f FILE]

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
