from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PieChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.figure = Figure(figsize=(4, 4))
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_chart(self, distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        labels = distribution.keys()
        sizes = distribution.values()

        ax.pie(sizes, labels=labels, autopct="%1.1f%%")
        ax.set_title("Equipment Type Distribution")

        self.canvas.draw()
