from pathlib import Path
from subprocess import CalledProcessError, run
from tempfile import TemporaryDirectory
from typing import List

import pytest

from ktfmtprecommithook import ktfmtprecommithook


@pytest.mark.parametrize(
    "extra_args",
    [
        [],
        ["--dropbox-style"],
        ["--google-style"],
        ["--kotlinlang-style"],
        ["--version=0.27"],
    ],
)
def test_ktfmtprecommithook(extra_args: List[str]):
    with TemporaryDirectory() as dirstr:
        directory = Path(dirstr)
        src = create_example_kotlin_file(directory / "example1.kt")
        initial = open(src).read()
        ktfmtprecommithook([src], extra_args=extra_args)
        final = open(src).read()
        assert initial != final


def test_ktfmtprecommithook_with_multiple_files():
    with TemporaryDirectory() as dirstr:
        directory = Path(dirstr)
        source_files = [
            create_example_kotlin_file(directory / "example{num}.kt")
            for num in range(3)
        ]
        initial = [open(src).read() for src in source_files]
        ktfmtprecommithook(source_files)
        final = [open(src).read() for src in source_files]
        assert all(ini != fin for ini, fin in zip(initial, final))


def test_precommit():
    # Note: this test clones the current commit of the working repository.
    # It will only test committed changes.
    with TemporaryDirectory() as dirstr:
        directory = Path(dirstr)
        src = create_example_kotlin_file(directory / "example.kt")
        initial = open(src).read()
        path_to_repo = Path.cwd()
        precommit_config_file(directory, path_to_repo)
        run(["git", "init", "--initial-branch=main"], check=True, cwd=directory)
        run(["git", "add", "."], check=True, cwd=directory)
        # first pass should fail
        with pytest.raises(CalledProcessError):
            run(["pre-commit", "run", "--all", "-v"], check=True, cwd=directory)
        firstpass = open(src).read()
        assert initial != firstpass
        # second pass should succeed
        run(["pre-commit", "run", "--all", "-v"], check=True, cwd=directory)
        secondpass = open(src).read()
        assert firstpass == secondpass


def precommit_config_text(path_to_repo: Path) -> str:
    commithash = (
        run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            cwd=path_to_repo,
        )
        .stdout.decode()
        .strip()
    )
    return f"""
repos:
- repo: {path_to_repo.resolve()}
  rev: {commithash}
  hooks:
  - id: ktfmt
"""


def precommit_config_file(directory: Path, path_to_repo: Path) -> Path:
    content = precommit_config_text(path_to_repo)
    outpath = directory / ".pre-commit-config.yaml"
    with open(outpath, "w") as f:
        f.write(content)
    return outpath


def example_kotlin_hello_world() -> str:
    return """
// ktfmt should reformat this all to a single line
fun
main()
=
println("Hello World")
"""


def create_example_kotlin_file(filepath: Path) -> Path:
    with open(filepath, "w") as f:
        f.write(example_kotlin_hello_world())
    return filepath
