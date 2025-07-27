from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from modules.side_controls_3_header.config import layout

def create_sideControls3Header(parent, x, y, w, h):
    panel = QLabel(parent)
    panel.setObjectName("sideControls3Header")
    panel.setGeometry(x, y, w, h)

    label = QLabel(panel)
    label.setObjectName("sideControls3Header-label")
    label.setText(layout.get("text", ""))
    label.setGeometry(
        layout.get("xOffset", 0),
        layout.get("yOffset", 0),
        layout.get("widthOverride", w) or w,
        layout.get("heightOverride", h) or h
    )
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    return panel