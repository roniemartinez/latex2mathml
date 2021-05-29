class NumeratorNotFoundError(Exception):
    pass


class DenominatorNotFoundError(Exception):
    pass


class ExtraLeftOrMissingRightError(Exception):
    pass


class MissingSuperScriptOrSubscriptError(Exception):
    pass


class DoubleSubscriptsError(Exception):
    pass


class DoubleSuperscriptsError(Exception):
    pass


class NoAvailableTokensError(Exception):
    pass
