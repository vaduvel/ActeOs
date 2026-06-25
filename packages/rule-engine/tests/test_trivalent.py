from wb_rule_engine.trivalent import Tri, from_bool, tri_all, tri_any, tri_not


def test_from_bool():
    assert from_bool(True) is Tri.TRUE
    assert from_bool(False) is Tri.FALSE


def test_not():
    assert tri_not(Tri.TRUE) is Tri.FALSE
    assert tri_not(Tri.FALSE) is Tri.TRUE
    assert tri_not(Tri.UNKNOWN) is Tri.UNKNOWN


def test_all():
    assert tri_all([Tri.TRUE, Tri.TRUE]) is Tri.TRUE
    assert tri_all([Tri.TRUE, Tri.FALSE]) is Tri.FALSE
    assert tri_all([Tri.TRUE, Tri.UNKNOWN]) is Tri.UNKNOWN
    # one FALSE dominates even with UNKNOWN present
    assert tri_all([Tri.UNKNOWN, Tri.FALSE]) is Tri.FALSE
    assert tri_all([]) is Tri.TRUE


def test_any():
    assert tri_any([Tri.FALSE, Tri.FALSE]) is Tri.FALSE
    assert tri_any([Tri.FALSE, Tri.TRUE]) is Tri.TRUE
    assert tri_any([Tri.FALSE, Tri.UNKNOWN]) is Tri.UNKNOWN
    # one TRUE dominates even with UNKNOWN present
    assert tri_any([Tri.UNKNOWN, Tri.TRUE]) is Tri.TRUE
    assert tri_any([]) is Tri.FALSE
