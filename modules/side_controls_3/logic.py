import os
import urllib.request
import zipfile
import json
from functools import partial
from PyQt6.QtWidgets import QLabel, QPushButton, QMessageBox
from modules.side_controls_3.config import layout, controls
from modules.console_popup.logic import ConsolePopup
from modules.logger.logic import Logger

STEAMCMD_URL = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
STEAMCMD_FOLDER = os.path.join(BASE_DIR, "SteamCMD")
STEAMCMD_EXE = os.path.join(STEAMCMD_FOLDER, "steamcmd.exe")
ZIP_PATH = os.path.join(STEAMCMD_FOLDER, "steamcmd.zip")

_steamcmd_popup = None

def create_sideControls3(parent, x, y, w, h, root, logger):
    panel = QLabel(parent)
    panel.setObjectName("sideControls3")
    panel.setGeometry(x, y, w, h)

    for key, cfg in controls["buttons"].items():
        object_name = f"sideControls3-btn-{key}"
        btn = QPushButton(cfg["text"], panel)
        btn.setObjectName(object_name)
        btn.setGeometry(cfg["x"], cfg["y"], cfg["width"], cfg["height"])

        if key == "update-steamcmd":
            btn.clicked.connect(update_steamcmd)
        elif key == "update-atlas":
            btn.clicked.connect(update_atlas)
        elif key == "update-mods":
            btn.clicked.connect(update_mods)

    return panel

def update_steamcmd():
    global _steamcmd_popup

    Logger.info("Checking for SteamCMD...")

    if not os.path.exists(STEAMCMD_EXE):
        try:
            os.makedirs(STEAMCMD_FOLDER, exist_ok=True)
            if os.path.exists(ZIP_PATH):
                os.remove(ZIP_PATH)

            Logger.info("Downloading SteamCMD...")
            with urllib.request.urlopen(STEAMCMD_URL) as response, open(ZIP_PATH, 'wb') as out_file:
                out_file.write(response.read())

            Logger.info("Extracting SteamCMD...")
            with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
                zip_ref.extractall(STEAMCMD_FOLDER)

            os.remove(ZIP_PATH)
            Logger.success("SteamCMD installed successfully.")

        except Exception as e:
            Logger.error(f"Failed to install SteamCMD: {str(e)}")
            QMessageBox.critical(None, "SteamCMD", f"Failed to install:\n{e}")
            return
    else:
        Logger.info("SteamCMD already installed.")

    Logger.info("Launching SteamCMD to self-update...")

    if _steamcmd_popup and _steamcmd_popup.isVisible():
        Logger.info("SteamCMD update already in progress.")
        return

    def handle_finished(code):
        if code == 0:
            Logger.success("SteamCMD auto-update completed successfully.")
        else:
            Logger.error(f"SteamCMD auto-update failed (exit code {code}).")

    _steamcmd_popup = ConsolePopup("SteamCMD Auto-Update")
    _steamcmd_popup.start_async(
        [STEAMCMD_EXE, "+quit"],
        working_directory=STEAMCMD_FOLDER,
        logger=Logger,
        on_finished=handle_finished
    )

def update_atlas():
    global _steamcmd_popup

    config_path = os.path.join(BASE_DIR, "configuration.json")
    if not os.path.exists(config_path):
        Logger.error("configuration.json not found.")
        return

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            install_dir = config.get("AtlasInstallDirectory")
    except Exception as e:
        Logger.error(f"Failed to read configuration.json: {str(e)}")
        return

    if not install_dir:
        Logger.error("AtlasInstallDirectory not set in configuration.json.")
        return

    Logger.info("Launching SteamCMD to update ATLAS...")

    if _steamcmd_popup and _steamcmd_popup.isVisible():
        Logger.info("ATLAS update already in progress.")
        return

    steamcmd_script = [
        f"force_install_dir {install_dir}",
        "login anonymous",
        "app_update 1006030 validate",
        "quit"
    ]

    script_path = os.path.join(STEAMCMD_FOLDER, "update_atlas_script.txt")
    try:
        with open(script_path, "w", newline="\r\n") as f:
            for line in steamcmd_script:
                f.write(line.strip() + "\r\n")
    except Exception as e:
        Logger.error(f"Failed to write ATLAS update script: {str(e)}")
        return

    def handle_finished(code):
        if code == 0:
            Logger.success("ATLAS server update completed successfully.")
        else:
            Logger.error(f"ATLAS server update failed (exit code {code}).")

    _steamcmd_popup = ConsolePopup("ATLAS Server Update")
    _steamcmd_popup.start_async(
        [STEAMCMD_EXE, "+runscript", script_path],
        working_directory=STEAMCMD_FOLDER,
        logger=Logger,
        on_finished=handle_finished
    )

def update_mods():
    Logger.info("Update MODS logic not implemented.")
