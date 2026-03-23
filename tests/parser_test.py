from parser import parse_lockfile
from pathlib import Path


def test_parse_lockfile():
    lockfile = Path("sample-uv/uv.lock")

    result = parse_lockfile(lockfile)

    assert "packages" in result
    assert isinstance(result["packages"], list)
    assert len(result["packages"]) > 0

    pkg = result["packages"][0]

    assert "name" in pkg
    assert "version" in pkg