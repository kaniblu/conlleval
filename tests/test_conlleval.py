import pathlib
import subprocess

from conlleval import *


def gold(lines):
    process = subprocess.Popen([
        "perl",
        str(pathlib.Path(__file__).parent.joinpath("conlleval.pl"))
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    gold, err = process.communicate(("\n".join(lines) + "\n").encode())
    return gold


def _test_evaluates(lines):
    """
    Perform a test case on a given result lines. Compares the result returned
    from this library with the results of the original perl script.

    Args:
        lines: lines of sequence tagging prediction file.
    """
    res = report(evaluate(lines))
    assert res.strip() == gold(lines).decode().strip()


def _test_scores(lines):
    """
    Perform a test case on a given result lines. Compares the result returned
    from this library with the results of the original perl script.

    Args:
        lines: lines of sequence tagging prediction file.
    """
    y_true, y_pred = zip(*[l.split()[-2:] for l in lines if len(l) > 0])
    res = report(score(y_true, y_pred))
    assert res.strip() == gold(lines).decode().strip()


def test_all_cases():
    for fn in pathlib.Path(__file__).parent.joinpath("cases").glob("*.txt"):
        with open(fn, "r") as f:
            lines = [line.rstrip("\n") for line in f]
        _test_evaluates(lines)
        _test_scores(lines)


if __name__ == "__main__":
    test_all_cases()
