__version__ = "0.8.0"

from argparse import ArgumentParser
from pathlib import Path

from .ktfmtprecommithook import DEFAULT_KTFMT_VERSION, ktfmtprecommithook


def _main():
    parser = ArgumentParser("ktfmt-precommit-hook")
    parser.add_argument("input_files", nargs="+", type=Path)
    parser.add_argument("--version", default=DEFAULT_KTFMT_VERSION, type=str)
    knownargs, unknownargs = parser.parse_known_args()
    ktfmtprecommithook(
        knownargs.input_files, version=knownargs.version, extra_args=unknownargs
    )


__all__ = ["ktfmtprecommithook"]
