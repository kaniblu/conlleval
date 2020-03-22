import pathlib
import subprocess

from conlleval import *


def _test_case(lines):
    """
    Perform a test case on a given result lines. Compares the result returned
    from this library with the results of the original perl script.

    Args:
        lines: lines of sequence tagging prediction file.
    """
    res = report(evaluate(lines))
    process = subprocess.Popen([
        "perl",
        str(pathlib.Path(__file__).parent.joinpath("conlleval.pl"))
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    gold, err = process.communicate(("\n".join(lines) + "\n").encode())
    assert res.strip() == gold.decode().strip()


def test_all_cases():
    for fn in pathlib.Path(__file__).parent.joinpath("cases").glob("*.txt"):
        with open(fn, "r") as f:
            lines = [line.rstrip("\n") for line in f]
        _test_case(lines)


if __name__ == "__main__":
    test_all_cases()
