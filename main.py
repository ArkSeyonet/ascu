#########################################################################################
####                             MAIN.PY - By ArkSeyonet                             ####
#########################################################################################

#######################################
##      AUTO INSTALL ENTRYPOINT      ##
#######################################
from modules.setup.dependency_manager import ensure_dependencies
ensure_dependencies()

#######################################
##              IMPORTS              ##
#######################################
import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QFontDatabase, QFont, QIcon
from PyQt6.QtCore import QFile, QTextStream

from config.layout_config import layout, WINDOW_WIDTH, WINDOW_HEIGHT
from modules.header_left.logic import create_header_left
from modules.header_right.logic import create_header_right
from modules.header_left.config import layout as layout_header_left
from modules.header_right.config import layout as layout_header_right
from modules.side_controls_1_header.logic import create_sideControls1Header
from modules.side_controls_2_header.logic import create_sideControls2Header
from modules.side_controls_3_header.logic import create_sideControls3Header
from modules.server_grid_header.logic import create_serverGridHeader
from modules.other_grid_header.logic import create_otherGridHeader
from modules.side_controls_1_header.config import layout as layout_sideControls1Header
from modules.side_controls_2_header.config import layout as layout_sideControls2Header
from modules.side_controls_3_header.config import layout as layout_sideControls3Header
from modules.server_grid_header.config import layout as layout_serverGridHeader
from modules.other_grid_header.config import layout as layout_otherGridHeader

#######################################
##      ServerControllerUI Class     ##
#######################################
class ServerControllerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle("ATLAS SERVER CONTROLLER UTILITY (v1.0_DEV)")
        self.setWindowIcon(QIcon("img/atlas_ico.ico"))
        self.set_font()
        self.init_ui()
        self.apply_stylesheet()

    def set_font(self):
        font_id = QFontDatabase.addApplicationFont("fonts/Montserrat-Bold.ttf")
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                font = QFont(families[0], 10)
                font.setBold(True)
                self.setFont(font)
        else:
            fallback = QFont("Arial", 10)
            fallback.setBold(True)
            self.setFont(fallback)

    def create_panel(self, name, x, y, w, h):
        if name == "header-left":
            return create_header_left(self, x, y, w, h)
        elif name == "header-right":
            return create_header_right(self, x, y, w, h)
        elif name == "sideControls1Header":
            return create_sideControls1Header(self, x, y, w, h)
        elif name == "sideControls2Header":
            return create_sideControls2Header(self, x, y, w, h)
        elif name == "sideControls3Header":
            return create_sideControls3Header(self, x, y, w, h)
        elif name == "serverGridHeader":
            return create_serverGridHeader(self, x, y, w, h)
        elif name == "otherGridHeader":
            return create_otherGridHeader(self, x, y, w, h)
        else:
            panel = QLabel(self)
            panel.setObjectName(name)
            panel.setGeometry(x, y, w, h)
            return panel

    def init_ui(self):
        merged_layout = layout.copy()
        merged_layout["header-left"] = layout_header_left
        merged_layout["header-right"] = layout_header_right
        merged_layout["sideControls1Header"] = layout_sideControls1Header
        merged_layout["sideControls2Header"] = layout_sideControls2Header
        merged_layout["sideControls3Header"] = layout_sideControls3Header
        merged_layout["serverGridHeader"] = layout_serverGridHeader
        merged_layout["otherGridHeader"] = layout_otherGridHeader

        for name, info in merged_layout.items():
            position = info["position"]
            offset_x, offset_y = info["offset"]
            width, height = info["size"]

            if "left" in position:
                x = offset_x
            elif "right" in position:
                x = WINDOW_WIDTH - offset_x - width
            else:
                x = 0

            if "top" in position:
                y = offset_y
            elif "bottom" in position:
                y = WINDOW_HEIGHT - offset_y - height
            else:
                y = 0

            self.create_panel(name, x, y, width, height)

    def apply_stylesheet(self):
        def read_qss(path):
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            return ""

        global_qss = read_qss("config/stylesheet.qss")
        qss_modules = [
            "modules/header_left/stylesheet.qss",
            "modules/header_right/stylesheet.qss",
            "modules/side_controls_1_header/stylesheet.qss",
            "modules/side_controls_2_header/stylesheet.qss",
            "modules/side_controls_3_header/stylesheet.qss",
            "modules/server_grid_header/stylesheet.qss",
            "modules/other_grid_header/stylesheet.qss",
        ]
        module_qss = "\n".join(read_qss(path) for path in qss_modules)
        self.setStyleSheet(global_qss + "\n" + module_qss)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerControllerUI()
    window.show()
    sys.exit(app.exec())
