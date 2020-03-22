#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2018-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"


class EmptyGroupError(Exception):
    pass


class NumeratorNotFoundError(Exception):
    pass


class DenominatorNotFoundError(Exception):
    pass


class ExtraLeftOrMissingRight(Exception):
    pass


class MissingSuperScriptOrSubscript(Exception):
    pass
