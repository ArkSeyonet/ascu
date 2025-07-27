import os
import psutil
from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtCore import QTimer
from modules.header_right.config import layout, statusTable, metricsTable, buttons

def create_header_right(parent, x, y, w, h):
    container = QLabel(parent)
    container.setObjectName("header-right")
    container.setGeometry(x, y, w, h)

    row_h = statusTable.get("rowHeight", 16)
    row_spacing = statusTable.get("rowSpacing", 4)

    status_labels = {}

    # Table 1 – SteamCMD / ATLAS / REDIS
    for i, row in enumerate(statusTable.get("rows", [])):
        y_pos = statusTable["top"] + i * (row_h + row_spacing)

        label = QLabel(row["label"], container)
        label.setObjectName("label-status-prefix")
        label.setGeometry(statusTable["labelX"], y_pos, statusTable["labelWidth"], row_h)

        value = QLabel(row["value"], container)
        value.setObjectName(row["objectName"])
        value.setGeometry(statusTable["valueX"], y_pos, statusTable["valueWidth"], row_h)

        status_labels[row["objectName"]] = value

    # Table 2 – CPU & Memory
    metric_labels = {}
    for i, row in enumerate(metricsTable.get("rows", [])):
        y_pos = metricsTable["top"] + i * (row_h + row_spacing)

        label = QLabel(row["label"], container)
        label.setObjectName("label-status-prefix")
        label.setGeometry(metricsTable["labelX"], y_pos, metricsTable["labelWidth"], row_h)

        value = QLabel(row["value"], container)
        value.setObjectName(row["objectName"])
        value.setGeometry(metricsTable["valueX"], y_pos, metricsTable["valueWidth"], row_h)

        metric_labels[row["objectName"]] = value

    # Buttons
    for key, btn_info in buttons.items():
        btn = QPushButton(btn_info["text"], container)
        btn.setObjectName(btn_info["objectName"])
        btn.setGeometry(
            w - btn_info["offsetRight"] - btn_info["width"],
            btn_info["top"],
            btn_info["width"],
            btn_info["height"]
        )

    # --- Functional Logic ---

    def update_steamcmd_status():
        exe_path = os.path.join(os.getcwd(), "SteamCMD", "steamcmd.exe")
        installed = os.path.exists(exe_path)
        steam_label = status_labels.get("label-status-steamcmd")
        if steam_label:
            steam_label.setText("Installed" if installed else "Not Installed")
            steam_label.setObjectName("label-status-steamcmd-installed" if installed else "label-status-steamcmd-missing")
            steam_label.setStyleSheet("")  # refresh QSS

    def update_system_usage():
        cpu_label = metric_labels.get("label-cpu")
        mem_label = metric_labels.get("label-mem")
        if cpu_label:
            cpu_label.setText(f"{psutil.cpu_percent(interval=None)}%")
        if mem_label:
            mem = psutil.virtual_memory()
            mem_label.setText(f"{mem.percent}%")

    # Initialize psutil CPU tracking (required before using interval=None)
    psutil.cpu_percent(interval=None)

    update_steamcmd_status()
    update_system_usage()

    timer = QTimer(container)
    timer.timeout.connect(update_system_usage)
    timer.start(1000)  # Adjust to 2000 for less frequent polling

    return container
