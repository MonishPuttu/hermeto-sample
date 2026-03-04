import json

def generate_sbom(packages, output="sbom.json"):
    components = []

    for pkg in packages:
        components.append({
            "name": pkg["name"],
            "version": pkg["version"]
        })

    sbom = {"components": components}

    with open(output, "w") as f:
        json.dump(sbom, f, indent=2)
