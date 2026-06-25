from wb_contracts.errors import ProblemCode, WbError


def test_problem_shape():
    err = WbError("bad input", ProblemCode.VALIDATION_FAILED)
    assert err.to_problem() == {"type": "validation_failed", "title": "bad input"}


def test_default_code():
    assert WbError("x").code is ProblemCode.VALIDATION_FAILED
