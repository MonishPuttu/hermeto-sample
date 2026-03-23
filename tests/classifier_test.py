from source_classifier import classify_source


def test_registry_source():
    pkg = {"source": {"registry": "https://pypi.org/simple"}}
    assert classify_source(pkg) == "registry"


def test_git_source():
    pkg = {"source": {"git": "https://github.com/test/repo"}}
    assert classify_source(pkg) == "git"


def test_url_source():
    pkg = {"source": {"url": "https://example.com/file.tar.gz"}}
    assert classify_source(pkg) == "https"