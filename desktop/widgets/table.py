from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class SummaryTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Metric", "Value"])
        self.verticalHeader().setVisible(False)

    def update_table(self, summary):
        rows = [
            ("Total Equipment", summary["total"]),
            ("Avg Flowrate", round(summary["avg_flowrate"], 2)),
            ("Avg Pressure", round(summary["avg_pressure"], 2)),
            ("Avg Temperature", round(summary["avg_temperature"], 2)),
        ]

        self.setRowCount(len(rows))

        for i, (key, value) in enumerate(rows):
            self.setItem(i, 0, QTableWidgetItem(str(key)))
            self.setItem(i, 1, QTableWidgetItem(str(value)))

        self.resizeColumnsToContents()
