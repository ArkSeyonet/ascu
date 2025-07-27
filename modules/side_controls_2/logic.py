from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtGui import QFont
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

        font_cfg = cfg.get("font", {})
        font = QFont(font_cfg.get("family", "Arial"), font_cfg.get("size", 10))
        font.setBold(font_cfg.get("bold", False))
        btn.setFont(font)

    return panel
