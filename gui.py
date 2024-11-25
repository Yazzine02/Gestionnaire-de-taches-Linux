import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QHBoxLayout, QPushButton, QWidget, QLabel, QMessageBox, QProgressBar
)
from PyQt5.QtCore import QTimer
from backend import (
    get_processes, get_cpu_usage, get_memory_usage, get_disk_usage, 
    get_network_usage, kill_process
)

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux Task Manager")
        self.setGeometry(100, 100, 1000, 600)

        self.init_ui()

    def init_ui(self):
        # Main Layout
        self.main_layout = QVBoxLayout()

        # Process Table
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels(["PID", "Name", "CPU (%)", "Memory (%)"])
        self.process_table.cellDoubleClicked.connect(self.show_process_details)
        self.main_layout.addWidget(self.process_table)

        # Buttons for managing processes
        self.button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_process_table)
        self.kill_button = QPushButton("Kill Process")
        self.kill_button.clicked.connect(self.kill_selected_process)
        self.button_layout.addWidget(self.refresh_button)
        self.button_layout.addWidget(self.kill_button)
        self.main_layout.addLayout(self.button_layout)

        # System Metrics Section
        self.metrics_layout = QVBoxLayout()

        self.cpu_label = QLabel("CPU Usage:")
        self.cpu_bar = QProgressBar()
        self.metrics_layout.addWidget(self.cpu_label)
        self.metrics_layout.addWidget(self.cpu_bar)

        self.memory_label = QLabel("Memory Usage:")
        self.memory_bar = QProgressBar()
        self.metrics_layout.addWidget(self.memory_label)
        self.metrics_layout.addWidget(self.memory_bar)

        self.disk_label = QLabel("Disk Usage:")
        self.disk_bar = QProgressBar()
        self.metrics_layout.addWidget(self.disk_label)
        self.metrics_layout.addWidget(self.disk_bar)

        self.network_label = QLabel("Network Usage:")
        self.network_info = QLabel("")
        self.metrics_layout.addWidget(self.network_label)
        self.metrics_layout.addWidget(self.network_info)

        self.main_layout.addLayout(self.metrics_layout)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Start updating metrics
        self.start_metrics_update()

        # Initial Table Refresh
        self.refresh_process_table()

    def refresh_process_table(self):
        """Fetch and display the latest processes."""
        processes = get_processes()
        self.process_table.setRowCount(len(processes))

        for row, process in enumerate(processes):
            self.process_table.setItem(row, 0, QTableWidgetItem(str(process['pid'])))
            self.process_table.setItem(row, 1, QTableWidgetItem(process['name']))
            self.process_table.setItem(row, 2, QTableWidgetItem(str(process['cpu_percent'])))
            self.process_table.setItem(row, 3, QTableWidgetItem(str(process['memory_percent'])))

    def show_process_details(self, row, column):
        """Show detailed info about a process when double-clicked."""
        pid = self.process_table.item(row, 0).text()
        name = self.process_table.item(row, 1).text()
        cpu = self.process_table.item(row, 2).text()
        memory = self.process_table.item(row, 3).text()

        QMessageBox.information(
            self, "Process Details", 
            f"PID: {pid}\nName: {name}\nCPU Usage: {cpu}%\nMemory Usage: {memory}%"
        )

    def kill_selected_process(self):
        """Terminate the selected process."""
        selected_row = self.process_table.currentRow()
        if selected_row >= 0:
            pid = int(self.process_table.item(selected_row, 0).text())
            success, message = kill_process(pid)
            if success:
                QMessageBox.information(self, "Success", f"Process {pid} terminated.")
                self.refresh_process_table()
            else:
                QMessageBox.warning(self, "Error", f"Failed to terminate process: {message}")
        else:
            QMessageBox.warning(self, "Error", "No process selected.")

    def update_metrics(self):
        """Fetch and update system metrics."""
        # CPU Usage
        self.cpu_bar.setValue(int(get_cpu_usage()))

        # Memory Usage
        memory = get_memory_usage()
        self.memory_bar.setValue(int(memory['percent']))

        # Disk Usage
        disk = get_disk_usage()
        self.disk_bar.setValue(int(disk['percent']))

        # Network Usage
        network = get_network_usage()
        self.network_info.setText(
            f"Bytes Sent: {network['bytes sent']} | Bytes Received: {network['bytes received']}"
        )

    def start_metrics_update(self):
        """Start a timer to refresh system metrics."""
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self.update_metrics)
        self.metrics_timer.start(1000)  # Refresh every second

if __name__ == "__main__":
    app = QApplication(sys.argv)
    task_manager = TaskManager()
    task_manager.show()
    sys.exit(app.exec_())

