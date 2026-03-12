from urllib.parse import urlparse


def classify_source(pkg):
    source = pkg.get("source")

    if not source:
        return "registry"

    if "git" in source:
        return "git"

    if "path" in source:
        return "local"

    if "url" in source:
        parsed = urlparse(source["url"])

        if parsed.scheme in ("http", "https"):
            return "https"

    return "registry"