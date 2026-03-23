from resolver import resolve_artifact


def test_resolver_prefers_sdist():
    pkg = {
        "name": "testpkg",
        "version": "1.0.0",
        "sdist": {"url": "sdist-url", "hash": "abc"},
        "wheels": [{"url": "wheel-url", "hash": "def"}]
    }

    artifact = resolve_artifact(pkg)

    assert artifact["url"] == "sdist-url"


def test_resolver_fallback_to_wheel():
    pkg = {
        "name": "testpkg",
        "version": "1.0.0",
        "sdist": None,
        "wheels": [{"url": "wheel-url", "hash": "def"}]
    }

    artifact = resolve_artifact(pkg)

    assert artifact["url"] == "wheel-url"