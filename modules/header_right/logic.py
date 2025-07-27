import os
import json
import psutil
import subprocess
from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtCore import QTimer
from modules.header_right.config import layout, statusTable, metricsTable, buttons
from modules.logger.logic import Logger

_logger_logged = False  # one-time guard for logger output

def get_config_value(key: str):
    try:
        with open("configuration.json", "r") as f:
            config = json.load(f)
        return config.get(key, "")
    except Exception:
        return ""

def initial_status_class(value: str, base: str):
    val = value.lower().strip()
    if "not installed" in val:
        return f"label-status-{base}-missing"
    elif "installed" in val:
        return f"label-status-{base}-installed"
    elif "not running" in val:
        return f"label-status-{base}-stopped"
    elif "running" in val:
        return f"label-status-{base}-running"
    else:
        return f"label-status-{base}-unknown"

def start_redis():
    base_dir = get_config_value("AtlasInstallDirectory")
    redis_dir = os.path.normpath(os.path.join(base_dir, "AtlasTools", "RedisDatabase"))
    exe_path = os.path.join(redis_dir, "redis-server.exe")
    conf_path = os.path.join(redis_dir, "redis.conf")

    if not os.path.exists(exe_path):
        return

    subprocess.Popen(
        [exe_path, conf_path],
        cwd=redis_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
    )

def stop_redis():
    base_dir = get_config_value("AtlasInstallDirectory")
    redis_path = os.path.normpath(os.path.join(base_dir, "AtlasTools", "RedisDatabase", "redis-server.exe"))

    for proc in psutil.process_iter(["pid", "name", "exe"]):
        try:
            if proc.info["name"] == "redis-server.exe" and proc.info["exe"] == redis_path:
                proc.terminate()
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return False

def create_header_right(parent, x, y, w, h):
    panel = QLabel(parent)
    panel.setObjectName("header-right")
    panel.setGeometry(x, y, w, h)

    row_h = statusTable.get("rowHeight", 18)
    row_spacing = statusTable.get("rowSpacing", 4)

    status_labels = {}

    # Table 1 – SteamCMD / ATLAS / REDIS
    for i, row in enumerate(statusTable.get("rows", [])):
        y_pos = statusTable["top"] + i * (row_h + row_spacing)

        prefix_name = row["label"].lower().replace(":", "").replace(" ", "-")
        label = QLabel(row["label"], panel)
        label.setObjectName(f"label-prefix-{prefix_name}")
        label.setGeometry(statusTable["labelX"], y_pos, statusTable["labelWidth"], row_h)

        base_key = row["objectName"].split("-")[-1]
        object_name = initial_status_class(row["value"], base_key)

        value = QLabel(row["value"], panel)
        value.setObjectName(object_name)
        value.setGeometry(statusTable["valueX"], y_pos, statusTable["valueWidth"], row_h)

        status_labels[row["objectName"]] = value

    # Table 2 – CPU & Memory
    metric_labels = {}
    for i, row in enumerate(metricsTable.get("rows", [])):
        y_pos = metricsTable["top"] + i * (row_h + row_spacing)

        prefix_name = row["label"].lower().replace(":", "").replace(" ", "-")
        label = QLabel(row["label"], panel)
        label.setObjectName(f"label-prefix-{prefix_name}")
        label.setGeometry(metricsTable["labelX"], y_pos, metricsTable["labelWidth"], row_h)

        value = QLabel(row["value"], panel)
        value.setObjectName(row["objectName"])
        value.setGeometry(metricsTable["valueX"], y_pos, metricsTable["valueWidth"], row_h)

        metric_labels[row["objectName"]] = value

    # Buttons
    for key, btn_cfg in buttons.items():
        btn = QPushButton(btn_cfg["text"], panel)
        btn.setObjectName(btn_cfg["objectName"])
        btn.setGeometry(
            w - btn_cfg["offsetRight"] - btn_cfg["width"],
            btn_cfg["top"],
            btn_cfg["width"],
            btn_cfg["height"]
        )

        if btn_cfg["objectName"] == "btn-redis-start":
            btn.clicked.connect(start_redis)
        elif btn_cfg["objectName"] == "btn-redis-stop":
            btn.clicked.connect(stop_redis)

    def update_steamcmd_status():
        exe_path = os.path.join(os.getcwd(), "SteamCMD", "steamcmd.exe")
        installed = os.path.exists(exe_path)
        label = status_labels.get("label-status-steamcmd")
        if label:
            label.setText("Installed" if installed else "Not Installed")
            label.setObjectName("label-status-steamcmd-installed" if installed else "label-status-steamcmd-missing")
            label.style().unpolish(label)
            label.style().polish(label)

        if not _logger_logged:
            if installed:
                Logger.success("SteamCMD is installed.")
            else:
                Logger.error("SteamCMD is missing.")

    def update_atlas_status():
        atlas_label = status_labels.get("label-status-atlas")
        if not atlas_label:
            return

        base_dir = get_config_value("AtlasInstallDirectory")
        full_path = os.path.normpath(os.path.join(base_dir, "ShooterGame", "Binaries", "Win64", "ShooterGameServer.exe"))
        installed = os.path.exists(full_path)
        atlas_label.setText("Installed" if installed else "Not Installed")
        atlas_label.setObjectName("label-status-atlas-installed" if installed else "label-status-atlas-missing")
        atlas_label.style().unpolish(atlas_label)
        atlas_label.style().polish(atlas_label)

        if not _logger_logged:
            if installed:
                Logger.success("ATLAS Dedicated Server is installed.")
            else:
                Logger.error("ATLAS Dedicated Server is not installed.")

    def update_redis_status():
        redis_label = status_labels.get("label-status-redis")
        if not redis_label:
            return

        base_dir = get_config_value("AtlasInstallDirectory")
        full_path = os.path.normpath(os.path.join(base_dir, "AtlasTools", "RedisDatabase", "redis-server.exe"))

        running = False
        if os.path.exists(full_path):
            for proc in psutil.process_iter(['name', 'exe']):
                try:
                    if proc.info['name'] == "redis-server.exe" and proc.info['exe'] == full_path:
                        running = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        redis_label.setText("Running" if running else "Not Running")
        redis_label.setObjectName("label-status-redis-running" if running else "label-status-redis-stopped")
        redis_label.style().unpolish(redis_label)
        redis_label.style().polish(redis_label)

        if not _logger_logged:
            if os.path.exists(full_path):
                if running:
                    Logger.success("Redis is running.")
                else:
                    Logger.error("Redis is not running.")
            else:
                Logger.error("Redis check skipped (ATLAS not installed — N/A).")

    def update_system_usage():
        cpu_label = metric_labels.get("label-cpu")
        mem_label = metric_labels.get("label-mem")
        if cpu_label:
            cpu_label.setText(f"{psutil.cpu_percent(interval=None)}%")
        if mem_label:
            mem = psutil.virtual_memory()
            mem_label.setText(f"{mem.percent}%")

    # Initialize
    psutil.cpu_percent(interval=None)
    update_steamcmd_status()
    update_atlas_status()
    update_redis_status()
    update_system_usage()

    # Timers
    metrics_timer = QTimer(panel)
    metrics_timer.timeout.connect(update_system_usage)
    metrics_timer.start(1000)

    redis_timer = QTimer(panel)
    redis_timer.timeout.connect(update_redis_status)
    redis_timer.start(250)

    status_timer = QTimer(panel)
    status_timer.timeout.connect(update_steamcmd_status)
    status_timer.timeout.connect(update_atlas_status)
    status_timer.start(3000)

    panel.trigger_steamcmd_update = update_steamcmd_status
    panel.trigger_atlas_update = update_atlas_status

    global _logger_logged
    _logger_logged = True

    return panel
