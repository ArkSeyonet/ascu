from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from modules.server_grid_header.config import layout

def create_serverGridHeader(parent, x, y, w, h):
    panel = QLabel(parent)
    panel.setObjectName("serverGridHeader")
    panel.setGeometry(x, y, w, h)

    label = QLabel(panel)
    label.setObjectName("serverGridHeader-label")
    label.setText(layout.get("text", ""))
    label.setGeometry(
        layout.get("xOffset", 0),
        layout.get("yOffset", 0),
        layout.get("widthOverride", w) or w,
        layout.get("heightOverride", h) or h
    )
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    return panel