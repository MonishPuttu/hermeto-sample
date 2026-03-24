from main import fetch_uv_dependencies
from pathlib import Path
import shutil


def test_full_pipeline():
    root = Path(__file__).resolve().parent.parent.parent

    project_dir = root / "sample-uv"
    output_dir = root / "test-output"

    if output_dir.exists():
        shutil.rmtree(output_dir)

    fetch_uv_dependencies(project_dir, output_dir)

    assert (output_dir / "deps" / "uv").exists()
    assert (output_dir / "sbom.json").exists()
    assert (output_dir / "uv.lock").exists()