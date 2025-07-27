from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap

def create_header_left(parent, x, y, w, h):
    container = QLabel(parent)
    container.setObjectName("header-left")
    container.setGeometry(x, y, w, h)

    logo = QLabel(container)
    logo.setObjectName("atlas-logo")
    logo.setGeometry(10, 14, 32, 32)
    logo.setPixmap(QPixmap("img/atlas_ico.png").scaled(32, 32))

    title = QLabel("ATLAS SERVER CONTROLLER UTILITY", container)
    title.setObjectName("atlas-title")
    title.setGeometry(50, 14, w - 60, 32)

    return container
