import sys
from pathlib import Path

from parser import parse_lockfile
from resolver import resolve_artifact
from fetcher import download_artifact
from verifier import verify_sha256
from sbom import generate_sbom


def fetch_uv_dependencies(project_path, output_dir):
    lockfile = Path(project_path) / "uv.lock"

    packages = parse_lockfile(lockfile)

    deps_dir = Path(output_dir) / "deps" / "uv"
    deps_dir.mkdir(parents=True, exist_ok=True)

    for pkg in packages:
        artifact = resolve_artifact(pkg)

        if not artifact:
            continue

        file_path = download_artifact(artifact["url"], deps_dir)

        if not verify_sha256(file_path, artifact["hash"]):
            raise RuntimeError(f"hash mismatch for {pkg['name']}")

    sbom_file = Path(output_dir) / "sbom.json"

    generate_sbom(packages, sbom_file)


if __name__ == "__main__":
    project_path = sys.argv[1]
    output_dir = sys.argv[2]

    fetch_uv_dependencies(project_path, output_dir)