from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtGui import QFont
from modules.side_controls_1.config import layout, controls

def create_sideControls1(parent, x, y, w, h):
    panel = QLabel(parent)
    panel.setObjectName("sideControls1")
    panel.setGeometry(x, y, w, h)

    for key, cfg in controls["buttons"].items():
        object_name = f"sideControls1-btn-{key}"
        btn = QPushButton(cfg["text"], panel)
        btn.setObjectName(object_name)
        btn.setGeometry(cfg["x"], cfg["y"], cfg["width"], cfg["height"])

    return panel

