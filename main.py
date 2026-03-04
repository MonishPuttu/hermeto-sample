import sys
from parser import parse_lockfile
from resolver import resolve_artifact
from fetcher import download
from verifier import verify
from sbom import generate_sbom

project_path = sys.argv[1]
lockfile = f"{project_path}/uv.lock"

packages = parse_lockfile(lockfile)

for pkg in packages:
    artifact = resolve_artifact(pkg)

    if not artifact:
        continue

    file = download(artifact["url"])

    if verify(file, artifact["hash"]):
        print("verified:", pkg["name"])
    else:
        raise Exception("hash mismatch")

generate_sbom(packages)
