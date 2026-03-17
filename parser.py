import tomllib


def parse_lockfile(path):
    with open(path, "rb") as f:
        raw_text = f.read()
        data = tomllib.loads(raw_text.decode())

    packages = []

    lock_revision = None
    if "metadata" in data:
        lock_revision = data["metadata"].get("revision")

    for pkg in data.get("package", []):
        name = pkg.get("name")
        version = pkg.get("version")

        wheels = []
        sdist = None

        if "wheels" in pkg:
            wheels = pkg["wheels"]

        if "sdist" in pkg:
            sdist = pkg["sdist"]

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

                if dist.get("type") == "sdist":
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
        "revision": lock_revision,
        "raw": raw_text
    }