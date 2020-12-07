import os
import subprocess

import aoc_ranking

MAIN = os.path.abspath(os.path.dirname(aoc_ranking.__file__))
TESTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

CHECK_PATHS = [MAIN, TESTS]


def test_black():
    process = subprocess.run(
        ["black", "--check", "--line-length", "88", *CHECK_PATHS],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.returncode == 0, (
        process.stdout.decode("utf-8") + "\n" + process.stderr.decode("utf-8")
    )
