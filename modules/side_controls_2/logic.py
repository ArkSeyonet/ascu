from PyQt6.QtWidgets import QLabel, QPushButton
from modules.side_controls_2.config import layout, controls

def create_sideControls2(parent, x, y, w, h):
    panel = QLabel(parent)
    panel.setObjectName("sideControls2")
    panel.setGeometry(x, y, w, h)

    for key, cfg in controls["buttons"].items():
        object_name = f"sideControls2-btn-{key}"
        btn = QPushButton(cfg["text"], panel)
        btn.setObjectName(object_name)
        btn.setGeometry(cfg["x"], cfg["y"], cfg["width"], cfg["height"])

    return panel
