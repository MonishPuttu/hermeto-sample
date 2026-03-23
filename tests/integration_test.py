from main import fetch_uv_dependencies
from pathlib import Path
import shutil


def test_full_pipeline():
    output_dir = Path("test-output")

    if output_dir.exists():
        shutil.rmtree(output_dir)

    fetch_uv_dependencies("sample-uv", output_dir)

    assert (output_dir / "deps" / "uv").exists()
    assert (output_dir / "sbom.json").exists()
    assert (output_dir / "uv.lock").exists()