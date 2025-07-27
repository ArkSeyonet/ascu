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

        font_cfg = cfg.get("font", {})
        font = QFont(font_cfg.get("family", "Arial"), font_cfg.get("size", 10))
        font.setBold(font_cfg.get("bold", False))
        btn.setFont(font)

        btn.setStyleSheet(f"""
            QPushButton#{object_name} {{
                background-color: {cfg.get("bg", "#1C7293")};
                color: {cfg.get("fg", "#FFFFFF")};
                border: 1px solid {cfg.get("border", "#000000")};
            }}
        """)

    return panel
