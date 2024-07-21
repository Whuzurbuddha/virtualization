import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import get


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1005, 607)

        self.centralwidget = QWidget(MainWindow)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.main_frame = QFrame(self.centralwidget)
        self.main_frame.setLayout(QVBoxLayout())

        self.menu_frame = QFrame(self.main_frame)
        self.menu_frame.setFrameShape(QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QFrame.Raised)
        self.menu_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.menu_frame.setFixedHeight(50)

        self.data_button = QPushButton(self.menu_frame)
        self.data_button.setText("Start")
        self.data_button.setGeometry(QRect(10, 8, 88, 34))
        self.data_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.data_frame = QFrame(self.main_frame)
        self.data_frame.setFrameShape(QFrame.StyledPanel)
        self.data_frame.setFrameShadow(QFrame.Raised)
        self.data_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.data_frame.setLayout(QVBoxLayout())

        self.main_frame.layout().addWidget(self.menu_frame)
        self.main_frame.layout().addWidget(self.data_frame)

        self.horizontalLayout.addWidget(self.main_frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    class MplCanvas(FigureCanvas):
        def __init__(self, parent=None, width=5, height=4, dpi=100):
            fig = Figure(figsize=(width, height), dpi=dpi)
            self.axes = fig.add_subplot(111, projection='3d')
            super(Ui_MainWindow.MplCanvas, self).__init__(fig)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow",
            "Weather Data Visualization",
            None))

    def add_plot_to_data_frame(self, plot_widget):
        layout = self.data_frame.layout()
        for i in reversed(range(layout.count())):
            widget_to_remove = layout.itemAt(i).widget()
            layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
        layout.addWidget(plot_widget)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setStyleSheet("""
            QPushButton {
                color: rgb(0, 0, 0);
            }
            QFrame{
                border-radius: 5px;
            }
            QPushButton:hover {
                color: rgb(255, 255, 255);
            }
        """)
        self.ui.data_button.clicked.connect(self.data)

    def add_plot(self, data):
        dates = [entry[0].__format__("%d.%m.%Y") for entry in data]
        cases = [entry[1] for entry in data]
        deaths = [entry[2] for entry in data]
        mortality = [entry[3] for entry in data]

        sc = Ui_MainWindow.MplCanvas(self, width=8, height=6, dpi=100)
        ax = sc.axes

        np.random.seed(19680801)
        n = 300
        rng = np.random.default_rng()
        xs = rng.uniform(min(cases), max(cases), n)
        ys = rng.uniform(min(deaths), max(deaths), n)
        zs = rng.uniform(min(mortality), max(mortality), n)

        norm = plt.Normalize(min(ys), max(ys))
        colors = cm.coolwarm(norm(ys))

        ax.scatter(xs, ys, zs, c=colors, marker='o')

        ax.set_xlabel('Diseases')
        ax.set_ylabel('Deaths')
        ax.set_zlabel('Mortality')
        ax.set_title('Corona analysis: diseases, deaths and mortality')

        self.ui.add_plot_to_data_frame(sc)

    def data(self):
        temp_result = get.data()
        self.add_plot(temp_result)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
