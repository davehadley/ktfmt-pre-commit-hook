import os
import shutil
import urllib.request
from pathlib import Path
from subprocess import run
from typing import Iterable, Optional

from filelock import FileLock  # type: ignore

DEFAULT_KTFMT_VERSION = "0.29"


def ktfmtprecommithook(
    input_files: Iterable[Path],
    version: str = DEFAULT_KTFMT_VERSION,
    extra_args: Optional[Iterable[str]] = None,
) -> None:
    if extra_args is None:
        extra_args = []
    ktfmt = _get_ktfmt(version=version)
    cmd = (
        ["java", "-jar", str(ktfmt)] + list(extra_args) + [str(f) for f in input_files]
    )
    run(cmd, check=True)
    return


def _get_ktfmt(version: str) -> Path:
    try:
        dst = _cache_directory() / f"ktfmt-{version}-jar-with-dependencies.jar"
        with FileLock(str(dst.resolve()) + ".lock"):
            if not dst.exists():
                url = f"https://search.maven.org/remotecontent?filepath=com/facebook/ktfmt/{version}/ktfmt-{version}-jar-with-dependencies.jar"
                tempfilename, _ = urllib.request.urlretrieve(url=url)
                shutil.move(tempfilename, dst)
            assert dst.exists()
    except Exception as ex:
        raise Exception(f"failed to find ktfmt version {version}") from ex
    return dst


def _cache_directory() -> Path:
    # try the same places that pre-commit tries https://github.com/pre-commit/pre-commit/blob/master/pre_commit/store.py
    try:
        precommitcachedirectory = Path(os.environ.get("PRE_COMMIT_HOME"))  # type: ignore
    except TypeError:
        precommitcachedirectory = (
            Path(os.environ.get("XDG_CACHE_HOME") or (Path.home() / ".cache"))
            / "pre-commit"
        )
    directory = precommitcachedirectory / "ktfmtprecommithook"
    directory.mkdir(parents=True, exist_ok=True)
    return directory
