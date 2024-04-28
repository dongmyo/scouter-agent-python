import os
from pathlib import Path


def get_app_path():
    """Returns the current program path"""
    scouter_agent_home = os.getenv("SCOUTER_AGENT_HOME")
    if not scouter_agent_home:
        try:
            scouter_agent_home = os.getcwd()
        except Exception as e:
            return "", e
    return scouter_agent_home, None


def get_scouter_path():
    """Returns the Scouter path, creates the directory if it does not exist"""
    scouter_path = os.getenv("SCOUTER_AGENT_HOME")
    if not scouter_path:
        app_path, err = get_app_path()
        if err:
            app_path = os.tempdir()
        scouter_path = Path(app_path) / "scouter"
    make_dir(scouter_path)
    return str(scouter_path)


def make_dir(path):
    """Creates a directory at the specified path, handling errors."""
    try:
        os.makedirs(path, mode=0o755, exist_ok=True)
    except Exception as e:
        print(f"cannot create folder {path}")
