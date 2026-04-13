import tomllib


class InvalidLockfileFormat(Exception):
    pass


def parse_lockfile(path):
    if not path.exists():
        raise FileNotFoundError("uv.lock not found")

    with open(path, "rb") as f:
        raw_text = f.read()
        data = tomllib.loads(raw_text.decode())

    version = data.get("version")
    if version != 1:
        raise InvalidLockfileFormat("Unsupported uv.lock version")

    requires_python = data.get("requires-python")

    packages = []

    for pkg in data.get("package", []):
        name = pkg.get("name")
        version = pkg.get("version")

        wheels = pkg.get("wheels", [])
        sdist = pkg.get("sdist")

        if not wheels and not sdist:
            source = pkg.get("source", {})
            if "url" in source:
                sdist = {
                    "url": source["url"],
                    "hash": source.get("hash")
                }

        if "distributions" in pkg:
            for dist in pkg["distributions"]:
                if dist.get("type") == "wheel":
                    wheels.append(dist)
                elif dist.get("type") == "sdist":
                    sdist = dist

        packages.append({
            "name": name,
            "version": version,
            "wheels": wheels,
            "sdist": sdist,
            "marker": pkg.get("marker"),
            "source": pkg.get("source"),
            "dependencies": pkg.get("dependencies", [])
        })

    return {
        "packages": packages,
        "requires_python": requires_python,
        "raw": raw_text
    }