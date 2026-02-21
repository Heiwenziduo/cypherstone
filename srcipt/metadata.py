import tomllib
from pathlib import Path

def get_app_version():
    """Reads version from pyproject.toml"""
    try:
        path = Path("pyproject.toml")
        if path.exists():
            with open(path, "rb") as f:
                data = tomllib.load(f)
                return data.get("project", {}).get("version", "1.0.0")
    except Exception:
        pass
    return "1.0.0"