import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from modules.console_popup.worker import SubprocessWorker


class ConsolePopup(QDialog):
    def __init__(self, title="Console Output", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(800, 500)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: black; color: white; font-family: Consolas;")

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancel_process)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.cancelButton)

        layout = QVBoxLayout()
        layout.addWidget(self.console)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.worker = None
        self._logger = None
        self._on_finished_callback = None

    def _print(self, text):
        self.console.appendPlainText(text.rstrip())

    def _safe_log(self, logger, message):
        if not logger:
            return
        try:
            logger.log(message)
        except Exception:
            try:
                logger(message)
            except Exception:
                pass

    def start_async(self, cmd, working_directory=None, logger=None, on_finished=None):
        try:
            self._print(f"[ASCU] Running: {' '.join(cmd)}\n")

            if not os.path.exists(cmd[0]):
                raise FileNotFoundError(f"Executable not found: {cmd[0]}")

            self._logger = logger
            self._on_finished_callback = on_finished

            self.worker = SubprocessWorker(cmd, working_directory)
            self.worker.output_signal.connect(self._print)
            self.worker.error_signal.connect(self._print)
            self.worker.finished_signal.connect(self.on_process_finished)
            self.worker.log_signal.connect(lambda msg: self._safe_log(self._logger, msg))

            self.worker.start()
            self.show()

        except Exception as e:
            self._print(f"[Popup Error] {str(e)}")
            self._safe_log(logger, f"[Popup Error] {str(e)}")

    def cancel_process(self):
        if self.worker:
            self.worker.terminate_process()

    def on_process_finished(self, code):
        if callable(self._on_finished_callback):
            self._on_finished_callback(code)

        self.close()

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.terminate_process()
            self.worker.wait(3000)
        event.accept()
