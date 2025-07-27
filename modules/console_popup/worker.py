import subprocess
import os
import sys
from PyQt6.QtCore import QThread, pyqtSignal

class SubprocessWorker(QThread):
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)
    log_signal = pyqtSignal(str)

    def __init__(self, cmd, working_directory=None):
        super().__init__()
        self.cmd = cmd
        self.working_directory = working_directory
        self.process = None

    def run(self):
        try:
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"

            self.process = subprocess.Popen(
                self.cmd,
                cwd=self.working_directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                env=env
            )

            self.log_signal.emit(f"[Subprocess Started] {' '.join(self.cmd)}")

            for line in self.process.stdout:
                if line:
                    self.output_signal.emit(line.rstrip())

            self.process.wait()
            self.finished_signal.emit(self.process.returncode)

        except Exception as e:
            self.error_signal.emit(f"[Exception] {str(e)}")
            self.log_signal.emit(f"[Error] {str(e)}")
            self.finished_signal.emit(-1)

    def terminate_process(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.kill()
                self.log_signal.emit("[Process Killed]")
            except Exception:
                pass
