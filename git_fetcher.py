import subprocess
import tempfile
import tarfile
from pathlib import Path


def clone_as_tarball(repo_url, commit, output_dir, name):
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir) / name

        subprocess.run(
            ["git", "clone", repo_url, repo_path],
            check=True
        )

        subprocess.run(
            ["git", "checkout", commit],
            cwd=repo_path,
            check=True
        )

        tar_path = Path(output_dir) / f"{name}-{commit}.tar.gz"

        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(repo_path, arcname=name)

        return tar_path