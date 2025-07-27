#########################################################################################
####                             MAIN.PY - By ArkSeyonet                             ####
#########################################################################################

from modules.setup.dependency_manager import ensure_dependencies
ensure_dependencies()

import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QFontDatabase, QFont, QIcon

from config.layout_config import layout, WINDOW_WIDTH, WINDOW_HEIGHT

from modules.header_left.logic import create_header_left
from modules.header_right.logic import create_header_right
from modules.top_controls.logic import create_topControls
from modules.side_controls_1_header.logic import create_sideControls1Header
from modules.side_controls_2_header.logic import create_sideControls2Header
from modules.side_controls_3_header.logic import create_sideControls3Header
from modules.server_grid_header.logic import create_serverGridHeader
from modules.other_grid_header.logic import create_otherGridHeader

from modules.side_controls_1.logic import create_sideControls1
from modules.side_controls_2.logic import create_sideControls2
from modules.side_controls_3.logic import create_sideControls3

from modules.header_left.config import layout as layout_header_left
from modules.header_right.config import layout as layout_header_right
from modules.top_controls.config import layout as layout_topControls
from modules.side_controls_1_header.config import layout as layout_sideControls1Header
from modules.side_controls_2_header.config import layout as layout_sideControls2Header
from modules.side_controls_3_header.config import layout as layout_sideControls3Header
from modules.server_grid_header.config import layout as layout_serverGridHeader
from modules.other_grid_header.config import layout as layout_otherGridHeader

from modules.side_controls_1.config import layout as layout_sideControls1
from modules.side_controls_2.config import layout as layout_sideControls2
from modules.side_controls_3.config import layout as layout_sideControls3

from modules.logger.config import layout as layout_logger
from modules.logger.logic import Logger

class ServerControllerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle("ATLAS SERVER CONTROLLER UTILITY (v1.0_DEV)")
        self.setWindowIcon(QIcon("img/atlas_ico.ico"))
        self.set_font()

        self.init_ui()       # build all UI panels except logger
        self.init_logger()   # create logger panel and output
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
        elif name == "topControls":
            return create_topControls(self, x, y, w, h)
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
        elif name == "sideControls1":
            return create_sideControls1(self, x, y, w, h)
        elif name == "sideControls2":
            return create_sideControls2(self, x, y, w, h)
        elif name == "sideControls3":
            return create_sideControls3(self, x, y, w, h, self, getattr(self, "logger", None))
        else:
            panel = QLabel(self)
            panel.setObjectName(name)
            panel.setGeometry(x, y, w, h)
            return panel

    def init_ui(self):
        merged_layout = layout.copy()
        merged_layout["header-left"] = layout_header_left
        merged_layout["header-right"] = layout_header_right
        merged_layout["topControls"] = layout_topControls
        merged_layout["sideControls1Header"] = layout_sideControls1Header
        merged_layout["sideControls2Header"] = layout_sideControls2Header
        merged_layout["sideControls3Header"] = layout_sideControls3Header
        merged_layout["serverGridHeader"] = layout_serverGridHeader
        merged_layout["otherGridHeader"] = layout_otherGridHeader
        merged_layout["sideControls1"] = layout_sideControls1
        merged_layout["sideControls2"] = layout_sideControls2
        merged_layout["sideControls3"] = layout_sideControls3
        # logger is not included in this loop anymore

        for name, info in merged_layout.items():
            position = info["position"]
            offset_x, offset_y = info["offset"]
            width, height = info["size"]

            x = offset_x if "left" in position else WINDOW_WIDTH - offset_x - width if "right" in position else 0
            y = offset_y if "top" in position else WINDOW_HEIGHT - offset_y - height if "bottom" in position else 0

            self.create_panel(name, x, y, width, height)

    def init_logger(self):
        panel_cfg = layout_logger["panel"]
        x = panel_cfg["offset"][0]
        y = WINDOW_HEIGHT - panel_cfg["offset"][1] - panel_cfg["size"][1]
        width = panel_cfg["size"][0]
        height = panel_cfg["size"][1]

        logger_panel = QLabel(self)
        logger_panel.setObjectName("logger")
        logger_panel.setGeometry(x, y, width, height)

        self.logger = Logger(logger_panel)
        self.logger.show()

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
            "modules/top_controls/stylesheet.qss",
            "modules/side_controls_1_header/stylesheet.qss",
            "modules/side_controls_2_header/stylesheet.qss",
            "modules/side_controls_3_header/stylesheet.qss",
            "modules/server_grid_header/stylesheet.qss",
            "modules/other_grid_header/stylesheet.qss",
            "modules/side_controls_1/stylesheet.qss",
            "modules/side_controls_2/stylesheet.qss",
            "modules/side_controls_3/stylesheet.qss",
            "modules/logger/stylesheet.qss"
        ]
        module_qss = "\n".join(read_qss(path) for path in qss_modules)
        self.setStyleSheet(global_qss + "\n" + module_qss)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerControllerUI()
    window.show()
    sys.exit(app.exec())
