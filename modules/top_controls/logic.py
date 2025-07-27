from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtCore import Qt
from modules.top_controls.config import layout, controls

def create_topControls(parent, x, y, w, h):
    panel = QLabel(parent)
    panel.setObjectName("topControls")
    panel.setGeometry(x, y, w, h)

    label_cfg = controls.get("label", {})
    label = QLabel(label_cfg.get("text", ""), panel)
    label.setObjectName("topControls-label")
    label.setGeometry(label_cfg.get("x", 10), 5, label_cfg.get("width", 60), h - 10)
    label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

    for key, cfg in controls.get("buttons", {}).items():
        text = cfg["text"]
        xpos = cfg["x"]
        width = cfg.get("width", 70)
        height = cfg.get("height", h - 8)
        border = cfg.get("border", "#000000")

        object_name = f"topControls-btn-{key}"
        btn = QPushButton(text, panel)
        btn.setObjectName(object_name)
        btn.setGeometry(xpos, 4, width, height)

        # Add border via inline style, background stays in QSS
        btn.setStyleSheet(f"""
            QPushButton#{object_name} {{
                border: 1px solid {border};
            }}
        """)

    return panel
