import subprocess
import sys
import os
import urllib.request
import shutil

# Dynamically detect current ABI tag, e.g. 'cp311', 'cp313'
PY_ABI = f"cp{sys.version_info.major}{sys.version_info.minor}"

REQUIRED_MODULES = {
    "PyQt6": {
        "base_name": "PyQt6",
        "version": "6.6.1",
        "abi": "abi3",  # PyQt6 wheels use abi3 for compatibility
        "platform": "win_amd64"
    },
    "psutil": {
        "base_name": "psutil",
        "version": "7.0.0",
        "abi": PY_ABI,
        "platform": "win_amd64"
    },
    "pyqtconsole": {
        "base_name": "pyqtconsole",
        "version": None,  # pip-only for now
        "abi": None,
        "platform": None
    }
}

def build_wheel_url(module, meta):
    if meta["version"] and meta["abi"] and meta["platform"]:
        file_name = f"{meta['base_name']}-{meta['version']}-{meta['abi']}-{meta['abi']}-{meta['platform']}.whl"
        return f"https://files.pythonhosted.org/packages/latest/{file_name}"
    return None

def is_installed(module_name):
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", module_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False

def install_from_url(module, url):
    if not url:
        return False

    files_dir = os.path.join(os.getcwd(), "files")
    os.makedirs(files_dir, exist_ok=True)

    filename = url.split("/")[-1]
    whl_path = os.path.join(files_dir, filename)

    print(f"[INFO] Downloading {module} wheel from PyPI...")
    try:
        with urllib.request.urlopen(url) as response, open(whl_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as e:
        print(f"[ERROR] Failed to download wheel for {module}: {e}")
        return False

    print(f"[INFO] Installing {module} from downloaded wheel...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", whl_path])
        return True
    except Exception as e:
        print(f"[ERROR] Failed to install {module} from wheel: {e}")
        return False

def ensure_dependencies():
    for module, meta in REQUIRED_MODULES.items():
        if not is_installed(module):
            print(f"[WARN] Module '{module}' not found. Attempting pip install...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except Exception as e:
                print(f"[ERROR] Pip install failed for '{module}': {e}")
                print(f"[INFO] Attempting direct wheel install...")
                wheel_url = build_wheel_url(module, meta)
                if not install_from_url(module, wheel_url):
                    print(f"[FATAL] Cannot continue without '{module}'")
                    sys.exit(1)
            print(f"[OK] Installed: {module}. Restarting script...")
            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit(0)
