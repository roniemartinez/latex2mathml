# Change Log
List of changes to latex2mathml

## [Unreleased]

## [1.0.5] - 2016-01-06
### Fixed
- VERSION file not added to manifest

## [1.0.4] - 2016-01-06
### Added
- additional matrices (pmatrix, bmatrix, bmatrix*, Bmatrix, Bmatrix*, vmatrix, vmatrix*, Vmatrix, Vmatrix*)

### Changed
- changed test asserts in command_test.py and converter_test.py from string format to Element object

### Fixed
- negative sign (-) becomes a separate element inside a matrix environment

## [1.0.3] - 2016-01-04
### Added
- matrix
    - \begin{matrix}..\end{matrix}
    - \matrix{...} -> taken from MathJax

## [1.0.2] - 2016-01-03
### Added
- added support for binomial
- added support for \left and \right commands
- added support for space commands \, \: \; \quad \qquad \<blank>
- added support for overline and underline

### Fixed
- aggregator bug on superscripts and subscipts

## [1.0.1] - 2016-01-02
### Added
- aggregator for grouping latex code with curly braces({})
- simple mathml viewer using flask
- parser for latex (unicode) symbols from http://milde.users.sourceforge.net/LUCR/Math/
- support for subscript and superscript
- support for fractions (\frac only)
- support for radicals

### Changed
- updated Element class, added attributes

## [1.0.0] - 2015-12-31
### Added
- latex string tokenizer
- Element class for xml elements
- simple converter implementation

[Unreleased]: https://github.com/Code-ReaQtor/latex2mathml/compare/v1.0.5...master
[1.0.5]: https://github.com/Code-ReaQtor/latex2mathml/releases/tag/1.0.5
[1.0.4]: https://github.com/Code-ReaQtor/latex2mathml/releases/tag/1.0.4
[1.0.3]: https://github.com/Code-ReaQtor/latex2mathml/releases/tag/1.0.3