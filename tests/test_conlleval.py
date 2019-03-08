import os
import json
import glob
from collections import abc

import conlleval

EPS = 1e-4


def compare(d1, d2, eps=1e-7):
    """
    Compares two data (recursively) and throws an error if a difference
    is detected.

    Argument:
        d1, d2 (Mapping or Sequence-like objects): objects to compare
        eps (float): the difference threshold for comparing two floats
    """
    t1, t2 = type(d1), type(d2)
    assert t1 == t2, f"the two items have different types: '{d1}', '{d2}'"

    if t1 == float:
        assert abs(d1 - d2) < eps, \
            f"the two floats are different: {d1} != {d2}"
    elif t1 in {int, str}:
        assert d1 == d2, \
            f"the two values are different: {d1} != {d2}"
    elif issubclass(t1, abc.Sequence):
        d1, d2 = list(d1), list(d2)
        assert len(d1) == len(d2), \
            f"the two sequences have different sizes: {len(d1)} != {len(d2)}"
        for x1, x2 in zip(d1, d2):
            compare(x1, x2, eps=eps)
    elif issubclass(t1, abc.Mapping):
        d1k, d2k = set(d1.keys()), set(d2.keys())
        assert d1k == d2k, \
            f"the two mappings have different key sets: {d1k} != {d2k}"
        for k in d1k:
            compare(d1[k], d2[k], eps=eps)
    else:
        assert d1 == d2, \
            f"the two values of unknown types are different: {d1} != {d2}"


def _test_case(lines, gold):
    """
    Runs a test case.

    Arguments:
        lines (iterator-like object): a standard conlleval-style predict-gold
            text file.
        gold (dict): a dictionary data of desired evaluation results
    """
    res = conlleval.evaluate(lines)
    compare(res, gold, eps=EPS)
    

def test_all_cases():
    for fn in glob.iglob(os.path.join(__file__, "cases/*.txt")):
        gold_path = fn.replace(".txt", ".json")
        with open(gold_path, "r") as f:
            gold = json.load(f)
        with open(fn, "r") as f:
            lines = [line.rstrip("\n") for line in f]
        _test_case(lines, gold)

