import json


def generate_purl(name, version):
    return f"pkg:pypi/{name}@{version}"


def generate_sbom(packages, output="sbom.json"):
    components = []

    for pkg in packages:
        component = {
            "name": pkg["name"],
            "version": pkg["version"],
            "purl": generate_purl(pkg["name"], pkg["version"])
        }

        components.append(component)

    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "components": components
    }

    with open(output, "w") as f:
        json.dump(sbom, f, indent=2)