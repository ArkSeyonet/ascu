from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from modules.other_grid_header.config import layout

def create_otherGridHeader(parent, x, y, w, h):
    panel = QLabel(parent)
    panel.setObjectName("otherGridHeader")
    panel.setGeometry(x, y, w, h)

    label = QLabel(panel)
    label.setObjectName("otherGridHeader-label")
    label.setText(layout.get("text", ""))
    label.setGeometry(
        layout.get("xOffset", 0),
        layout.get("yOffset", 0),
        layout.get("widthOverride", w) or w,
        layout.get("heightOverride", h) or h
    )
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    return panel
