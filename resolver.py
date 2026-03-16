def resolve_artifact(package):
    sdist = package.get("sdist")
    wheels = package.get("wheels", [])

    if sdist:
        return sdist

    if wheels:
        return wheels[0]

    return None