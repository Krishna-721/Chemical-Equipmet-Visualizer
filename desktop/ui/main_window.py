from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QMessageBox, QLabel
)

from services.analysis import analyze_csv
from widgets.chart import PieChartWidget
from widgets.table import SummaryTable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(200, 150, 1000, 600)

        container = QWidget()
        main_layout = QVBoxLayout()

        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        main_layout.addWidget(title)

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        main_layout.addWidget(self.upload_btn)

        content_layout = QHBoxLayout()

        self.chart = PieChartWidget()
        self.table = SummaryTable()

        content_layout.addWidget(self.chart, 1)
        content_layout.addWidget(self.table, 1)

        main_layout.addLayout(content_layout)

        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            summary = analyze_csv(file_path)
            self.chart.update_chart(summary["distribution"])
            self.table.update_table(summary)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
