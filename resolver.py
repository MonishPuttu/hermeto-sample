def resolve_artifact(package):
    wheels = package.get("wheels", [])

    if wheels:
        return wheels[0]

    return package.get("sdist")