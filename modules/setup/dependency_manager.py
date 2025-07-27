import subprocess
import sys
import os
import urllib.request
import shutil

REQUIRED_MODULES = {
    "PyQt6": {
        "whl_url": "https://files.pythonhosted.org/packages/8e/0d/f1dd790255f345310313e5b793f7a5b9d6c8c90d4b55de4246d17405dc2c/PyQt6-6.6.1-cp311-abi3-win_amd64.whl"
    },
    "psutil": {
        "whl_url": "https://files.pythonhosted.org/packages/50/1b/6921afe68c74868b4c9fa424dad3be35b095e16687989ebbb50ce4fceb7c/psutil-7.0.0-cp311-cp311-win_amd64.whl"
    }
}

def install_from_url(module, url):
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
        try:
            __import__(module)
        except ImportError:
            print(f"[WARN] Module '{module}' not found. Attempting pip install...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            except Exception as e:
                print(f"[ERROR] Pip install failed: {e}")
                print(f"[INFO] Attempting direct wheel download for '{module}'...")
                if not install_from_url(module, meta["whl_url"]):
                    print(f"[FATAL] Cannot continue without '{module}'")
                    sys.exit(1)
            print(f"[OK] Installed: {module}. Restarting script...")
            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit(0)
