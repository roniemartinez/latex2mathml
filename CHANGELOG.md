#  List of changes to latex2mathml

## Unreleased

## 2.8.0 - 2019-11-23
### Added
- OSX tests
- pycodestyle linter

### Changed
- Move package metadata to setup.cfg

### Fixed
- Group items in array rows correctly (#55)

### Removed
- Drop Python 2 support

## 2.7.1 - 2019-08-23
- Add xmlns in <math> (#56)

## 2.7.0 - 2019-06-05
### Added
- Support Math alphabets (#51)

### Fixed
- Correctly show \bar (#52)

## 2.6.7 - 2019-04-03
### Removed
- Drop Python 3.4 support

### Changed
- Update CI to use pipenv

## 2.6.6 - 2019-03-23
### Fixed
- Incorrect conversion when parentheses next to exponent (#44)
- Escaping of "<", ">" kept in XML (#46)

## 2.6.5 - 2019-03-23
### Fixed
- Escaping of "<", ">" kept in XML (#46)

## 2.6.4 - 2019-02-10
### Fixed
- IndexError on r'\sqrt { ( - 25 ) ^ { 2 } } = \pm 25' (#42)

## 2.6.3 - 2019-01-13
### Changed
- Update copyright

## 2.6.2 - 2018-10-17
### Added
- More shields (#37)

## 2.6.1 - 2018-10-13
### Added
- Support universal wheel (#35)

## 2.6.0 - 2018-10-13
### Fixed
- Drop TexSoup (#33)

### Changed
- Support Python 2.7

## 2.5.2 - 2018-10-10
### Added
- Deploy to PyPI from Travis CI (#25)

## 2.5.1 - 2018-10-10
### Changed
- Show README badges in table

## 2.5.0 - 2018-10-09
### Added
- AppVeyor Integration (#26)
- Implement Caching in Travis-CI and AppVeyor (#28)

## 2.4.0 - 2018-10-07
### Added
- Codecov Integration (#22)

## 2.3.0 - 2018-10-07
### Added
- Travis CI Integration (#18)

## 2.2.0 - 2018-10-04
### Changed
- Use TexSoup parser

### Removed
- Drop Python 2.7.x support

## 2.1.1.2 - 2018-10-02
### Fixed
- README not rendering rendering in PyPI (#11)

## 2.1.0 - 2018-09-29
### Added
- Support \over (#8)

## 2.0.3 - 2018-09-29
### Fixed
- Unescape texts (#5)

## 2.0.2 - 2017-09-02
### Fixed
- latex2mathml folder not included in package.

## 2.0.1 - 2017-09-02
### Changed
- LaTeX inputs and MathML outputs are shown in table in README.
- unimathsymbols.txt will be read once.
- Element class remove in exchange of xml.etree.xElementTree.

### Added
- File headers are included to source.

## 1.1.1 - 2016-07-21
### Fixed
- Python 3 compatibility (importing, xrange, iterator.next)

## 1.0.10 - 2016-02-14
### Added
- Support for arrays including arrays with vertical bars and horizontal lines (borders not supported)

## 1.0.9 - 2016-01-16
### Removed
- Flask viewer

### Changed
- Updated README.md

## 1.0.8 - 2016-01-10
### Added
- Viewer - Support for other browsers using CSS Fallback for MathML (https://github.com/fred-wang/mathml.css)
- Conversion of latex commands within matrix environments

### Fixed
- Incorrect aggregation of latex commands within matrix environment
- Removed newline and whitespaces when prettyprinting elements with text but without children

## 1.0.7 - 2016-01-09
### Added
- Pretty feature for Element class

### Changed
- Refactored codes
- Updated README file

## 1.0.6 - 2016-01-08
### Added
- Simple viewer using bootstrap and openshift

## 1.0.5 - 2016-01-06
### Fixed
- VERSION file not added to MANIFEST

## 1.0.4 - 2016-01-06
### Added
- additional matrices (pmatrix, bmatrix, bmatrix*, Bmatrix, Bmatrix*, vmatrix, vmatrix*, Vmatrix, Vmatrix*)

### Changed
- changed test asserts in command_test.py and converter_test.py from string format to Element object

### Fixed
- negative sign (-) becomes a separate element inside a matrix environment

## 1.0.3 - 2016-01-04
### Added
- matrix
    - \begin{matrix}..\end{matrix}
    - \matrix{...} -> taken from MathJax

## 1.0.2 - 2016-01-03
### Added
- added support for binomial
- added support for \left and \right commands
- added support for space commands \, \: \; \quad \qquad \<blank>
- added support for overline and underline

### Fixed
- aggregator bug on superscripts and subscipts

## 1.0.1 - 2016-01-02
### Added
- aggregator for grouping latex code with curly braces({})
- simple mathml viewer using flask
- parser for latex (unicode) symbols from http://milde.users.sourceforge.net/LUCR/Math/
- support for subscript and superscript
- support for fractions (\frac only)
- support for radicals

### Changed
- updated Element class, added attributes

## 1.0.0 - 2015-12-31
### Added
- latex string tokenizer
- Element class for xml elements
- simple converter implementation
