# system
import sys
import os
import atexit
import json
import re

#
from src.pyclic import _labview as lv

# ui
from ui_mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtUiTools import loadUiType
from PySide6.QtCore import QThread, Signal

# server
import socket

# def resource_path(relative_path):
#     try:
#         # PyInstaller creates a temp folder and stores its path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

# # Dynamically load the layout structure and the base class directly from the UI file
# ui_path = resource_path("mainwindow.ui")
# Ui_MainWindow, MainWindowBase = loadUiType(ui_path)

class TCPServerWorker(QThread):
    log_signal = Signal(str)
    command_received_signal = Signal(dict)

    def __init__(self, host="127.0.0.1", port=65432):
        super().__init__()
        self.host = host
        self.port = port
        self.running = False
        self.server_socket = None
        self.systems = {"clic"}

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket .bind((self.host, self.port))
            self.server_socket .listen(5)
            self.running = True
            self.log_signal.emit(f'[TCP Info]TCP server online')
        except Exception as e:
            self.log_signal.emit(f'TCP error: {e}')
            return


        while self.running:
            try:
                self.server_socket.settimeout(0.5) 
                client_socket, client_addr = self.server_socket.accept()
                
            except socket.timeout:
                continue

            # need to read message from the clinet
            data = client_socket.recv(4096).decode()
            if not data:
                client_socket.close()
                continue

            try:
                command = json.loads(data)
                self.command_received_signal.emit(command)
                response = {"status": "ok", "result": 'passed'}

            except Exception as e:
                print(e)            
                response = {"status": "error",  "message": f"No such method"}

            finally:
                client_socket.send(json.dumps(response).encode())
                client_socket.close()

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass # Already shut down or not connected

            self.server_socket.close()

# Inherit from both the base class and your specific UI design
#class MainWindow(MainWindowBase, Ui_MainWindow):
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # set variables before initiating
        self.config_path = None
        self.state_setup_clic = False
        global clic_device

        # setup Ui design
        self.setupUi(self) 

        # buttons
        self.btn_browse.clicked.connect(self.open_file_dialog)
        self.btn_clic_connect.clicked.connect(self.call_clic_init)

        self.btn_home.clicked.connect(self.clic_home)
        self.btn_test.clicked.connect(self.clic_test)

        self.btn_tcp_elements.clicked.connect(self.call_tcp_init)
        
        self.btn_changevoltage.clicked.connect(self.manual_changeVoltage)

        # console
        self.textconsole.setReadOnly(True)  # Keeps it as a non-editable log terminal

        # server worker thread
        self.server_thread = None

        # quit
        self.btn_quit.clicked.connect(self.close)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "All Files (*);;Text Files (*.txt)"
        )
        if file_path:
            self.line_edit_file.setText(file_path)
            self.config_path = self.line_edit_file.text()
            
    def call_clic_init(self):
        self.state_setup_clic = lv.initCLiC(self.config_path)
        self.textconsole.appendPlainText("[CLiC Info] SUCCESS! \n CliC Initiated!")
        if self.state_setup_clic == True:
            atexit.register(lv.deconstructCLiC)
        else:
            self.state_setup_clic = False
            self.textconsole.appendPlainText("[CLiC Info] ERROR!! \n CliC not Initiated...")

    def clic_home(self):
        if self.state_setup_clic == True:
            self.textconsole.appendPlainText("[CLiC Info] CliC homing to 0V...")
            lv.changeVoltage(0, 25)

    def clic_test(self):
        if self.state_setup_clic == True:
            lv.changeVoltage(100, 25)
            self.textconsole.appendPlainText("[CLiC Info] CliC test initated...")

    def manual_changeVoltage(self):
        if self.state_setup_clic == True:
            try:
                curr_target = float(self.line_edit_targetVoltage.text())
                curr_rate = float(self.line_edit_rampRate.text()) 
                lv.changeVoltage(curr_target, curr_rate)
                self.textconsole.appendPlainText(rf"[CLiC Info] Success! \n Setting CLiC to {curr_target} with rate {curr_rate}")

            except Exception as e:
                print('bad')
                self.textconsole.appendPlainText("[CLiC Info] Error in inputs")

    def call_tcp_init(self):
        if self.server_thread and self.server_thread.isRunning():
            self.textconsole.appendPlainText("[TCP Info] Stopping TCP Server...")
            self.server_thread.stop()
            self.server_thread.wait()
            self.btn_tcp_elements.setText("Start TCP Server")
        else:
            # Instantiate and start the thread worker
            self.server_thread = TCPServerWorker(host='127.0.0.1', port=65432)
            
            # Direct signals safely from background memory space to UI methods
            self.server_thread.log_signal.connect(self.log_to_console)
            self.server_thread.command_received_signal.connect(self.execute_device_command)
            
            self.server_thread.start()
            self.btn_tcp_elements.setText("Stop TCP Server")

    def execute_device_command(self, command_dict):
        class_key = command_dict.get("class")   # e.g., 'clic'
        method_name = command_dict.get("method") # e.g., 'changeVoltage'
        args = command_dict.get("args", [])      # e.g., [100, 10]
        kwargs = command_dict.get("kwargs", {})  # e.g., {}

        self.textconsole.appendPlainText(f"[Network Input] Received: {class_key}, {method_name}")

        device_map = {
            "clic": lv 
        }

        target_device = device_map.get(class_key)

        try:
            target_method = getattr(target_device, method_name)
            execution_result = target_method(*args, **kwargs)
            self.textconsole.appendPlainText("[CLiC Info] TCP Command Accepted and Ran.")

        except Exception as e:
            print(e)

    def log_to_console(self, text):
        """Safely updates text console from the network thread logs."""
        self.textconsole.appendPlainText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())