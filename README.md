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
    <tr>
        <td>All Contributors</td>
        <td><a href="#contributors-"><img src='https://img.shields.io/badge/all_contributors-1-orange.svg?style=for-the-badge' alt="All Contributors"></a></td>
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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://ron.sh"><img src="https://avatars.githubusercontent.com/u/2573537?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ronie Martinez</b></sub></a><br /><a href="#maintenance-roniemartinez" title="Maintenance">🚧</a> <a href="https://github.com/roniemartinez/latex2mathml/commits?author=roniemartinez" title="Code">💻</a> <a href="#infra-roniemartinez" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="https://anwen.cc/"><img src="https://avatars.githubusercontent.com/u/1472850?v=4?s=100" width="100px;" alt=""/><br /><sub><b>askender</b></sub></a><br /><a href="https://github.com/roniemartinez/latex2mathml/commits?author=askender" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/ghost"><img src="https://avatars.githubusercontent.com/u/10137?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Deleted user</b></sub></a><br /><a href="https://github.com/roniemartinez/latex2mathml/issues?q=author%3Aghost" title="Bug reports">🐛</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
