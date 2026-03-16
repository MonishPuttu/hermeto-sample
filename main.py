import sys
from pathlib import Path
import asyncio

from parser import parse_lockfile
from resolver import resolve_artifact
from verifier import verify_sha256
from sbom import generate_sbom
from dep_graph import build_dependency_graph, remove_dev_dependencies
from source_classifier import classify_source
from git_fetcher import clone_as_tarball
from fetcher import download_many


def fetch_uv_dependencies(project_path, output_dir):
    lockfile = Path(project_path) / "uv.lock"

    parsed = parse_lockfile(lockfile)
    packages = parsed["packages"]

    graph = build_dependency_graph(packages)

    dev_group = []

    for pkg in packages:
        dev_deps = pkg.get("dev-dependencies", {})
        for group in dev_deps.values():
            dev_group.extend(group)

    runtime_nodes = remove_dev_dependencies(graph, dev_group)

    packages = [p for p in packages if p["name"] in runtime_nodes]

    deps_dir = Path(output_dir) / "deps" / "uv"
    deps_dir.mkdir(parents=True, exist_ok=True)

    download_jobs = []
    pkg_map = {}

    for pkg in packages:

        source_type = classify_source(pkg)

        if source_type == "git":
            source = pkg.get("source")

            repo = source.get("git")
            commit = source.get("rev")

            clone_as_tarball(repo, commit, deps_dir, pkg["name"])
            continue

        artifact = resolve_artifact(pkg)

        if not artifact:
            continue

        download_jobs.append(artifact["url"])
        pkg_map[artifact["url"]] = pkg

    files = asyncio.run(download_many(download_jobs, deps_dir))

    for file_path, url in zip(files, download_jobs):

        pkg = pkg_map[url]

        artifact = resolve_artifact(pkg)

        if not verify_sha256(file_path, artifact["hash"]):
            raise RuntimeError(f"hash mismatch for {pkg['name']}")

    sbom_file = Path(output_dir) / "sbom.json"

    generate_sbom(packages, sbom_file)


if __name__ == "__main__":
    project_path = sys.argv[1]
    output_dir = sys.argv[2]

    fetch_uv_dependencies(project_path, output_dir)