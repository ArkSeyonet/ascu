from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtCore import Qt as QtCore
from PyQt6.QtGui import QTextCharFormat, QTextCursor, QColor
from modules.logger.config import layout

class Logger(QPlainTextEdit):
    _instance = None
    _pending = []  # holds (message, color) until instance is ready

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("loggerOutput")
        self.setReadOnly(True)

        cfg = layout["output"]
        x = cfg["offset_x"]
        y = cfg["offset_y"]
        width = cfg["width"]
        height = cfg["height"]

        align = cfg["align"]
        if align == "bottom-left":
            self.setGeometry(x, parent.height() - height - y, width, height)
        elif align == "top-left":
            self.setGeometry(x, y, width, height)
        elif align == "bottom-right":
            self.setGeometry(parent.width() - width - x, parent.height() - height - y, width, height)
        elif align == "top-right":
            self.setGeometry(parent.width() - width - x, y, width, height)
        else:
            self.setGeometry(x, y, width, height)

        self.setVerticalScrollBarPolicy(QtCore.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

        Logger._instance = self
        self.log("Checking data...", layout["format"]["info"]["color"])

        for msg, color in Logger._pending:
            self.log(msg, color)
        Logger._pending.clear()

    def log(self, message: str, color: str = "white"):
        if not message:
            return

        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))

        self.moveCursor(QTextCursor.MoveOperation.End)
        self.setCurrentCharFormat(fmt)
        self.appendPlainText(message)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    @staticmethod
    def global_log(message: str, color: str = "white"):
        if Logger._instance:
            Logger._instance.log(message, color)
        else:
            Logger._pending.append((message, color))

    @staticmethod
    def _log_with_format(level: str, message: str):
        fmt = layout.get("format", {}).get(level, {})
        symbol = fmt.get("symbol", "")
        color = fmt.get("color", "white")
        partial = fmt.get("partial", False)

        if partial:
            parts = message.rsplit(" ", 1)
            if len(parts) == 2:
                head, tail = parts
                Logger.global_log(f"{symbol} {head}", layout["format"]["info"]["color"])
                Logger.global_log(tail, color)
                return

        # fallback or full-color if partial disabled or can't split
        formatted = f"{symbol} {message}"
        Logger.global_log(formatted, color)

    @staticmethod
    def info(message: str):
        Logger._log_with_format("info", message)

    @staticmethod
    def success(message: str):
        Logger._log_with_format("success", message)

    @staticmethod
    def warn(message: str):
        Logger._log_with_format("warn", message)

    @staticmethod
    def error(message: str):
        Logger._log_with_format("error", message)
