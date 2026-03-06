import tomllib

def parse_lockfile(lockfile_path):
    with open(lockfile_path, "rb") as f:
        data = tomllib.load(f)

    packages = []

    for pkg in data.get("package", []):
        packages.append({
            "name": pkg["name"],
            "version": pkg["version"],
            "wheels": pkg.get("wheels", []),
            "sdist": pkg.get("sdist")
        })

    return packages