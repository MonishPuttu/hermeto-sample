def resolve_artifact(package):
    if package["wheels"]:
        return package["wheels"][0]
    return package["sdist"]
