from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from modules.side_controls_2_header.config import layout

def create_sideControls2Header(parent, x, y, w, h):
    panel = QLabel(parent)
    panel.setObjectName("sideControls2Header")
    panel.setGeometry(x, y, w, h)

    label = QLabel(panel)
    label.setObjectName("sideControls2Header-label")
    label.setText(layout.get("text", ""))
    label.setGeometry(
        layout.get("xOffset", 0),
        layout.get("yOffset", 0),
        layout.get("widthOverride", w) or w,
        layout.get("heightOverride", h) or h
    )
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    return panel