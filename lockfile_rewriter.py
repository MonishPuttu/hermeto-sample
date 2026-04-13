from pathlib import Path
import tomllib


def rewrite_lockfile(input_path, output_path, deps_root):
    with open(input_path, "rb") as f:
        data = tomllib.load(f)

    for pkg in data.get("package", []):
        name = pkg.get("name")
        version = pkg.get("version")

        base_path = Path(deps_root) / name / version

        if "wheels" in pkg:
            for wheel in pkg["wheels"]:
                url = wheel.get("url")
                if url:
                    filename = url.split("/")[-1]
                    local_path = base_path / filename
                    wheel["url"] = f"file://{local_path.resolve()}"

        if "sdist" in pkg and pkg["sdist"]:
            url = pkg["sdist"].get("url")
            if url:
                filename = url.split("/")[-1]
                local_path = base_path / filename
                pkg["sdist"]["url"] = f"file://{local_path.resolve()}"

    def write_value(v):
        if isinstance(v, str):
            return f'"{v}"'
        if isinstance(v, list):
            return "[" + ", ".join(write_value(i) for i in v) + "]"
        if isinstance(v, dict):
            return "{" + ", ".join(f"{k} = {write_value(val)}" for k, val in v.items()) + "}"
        return str(v)

    with open(output_path, "w") as f:
        for key, value in data.items():
            f.write(f"{key} = {write_value(value)}\n")