import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import get_data
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Ui_MainWindow(object):
    def __init__(self):
        self.horizontalLayout = None
        self.centralwidget = None
        self.main_frame = None
        self.menu_frame = None
        self.data_frame = None
        self.temp_button = None
        self.preci_button = None

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.resize(1005, 607)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.main_frame = QFrame(self.centralwidget)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setStyleSheet(u"background-color: rgb(32, 32, 32);")  # brighter black
        self.main_frame.setLayout(QVBoxLayout())

        self.menu_frame = QFrame(self.main_frame)
        self.menu_frame.setObjectName(u"menu_frame")
        self.menu_frame.setFrameShape(QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QFrame.Raised)
        self.menu_frame.setStyleSheet(u"background-color: rgb(44, 44, 44);")
        self.menu_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.menu_frame.setFixedHeight(50)

        self.data_frame = QFrame(self.main_frame)
        self.data_frame.setObjectName(u"data_frame")
        self.data_frame.setFrameShape(QFrame.StyledPanel)
        self.data_frame.setFrameShadow(QFrame.Raised)
        self.data_frame.setStyleSheet(u"background-color: rgb(44, 44, 44);")
        self.data_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.temp_button = QPushButton(self.menu_frame)
        self.temp_button.setText("Temperature")
        self.temp_button.setGeometry(QRect(10, 8, 88, 34))
        self.temp_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.preci_button = QPushButton(self.menu_frame)
        self.preci_button.setText("Precipitation")
        self.preci_button.setGeometry(QRect(105, 8, 88, 34))
        self.preci_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.main_frame.layout().addWidget(self.menu_frame)
        self.main_frame.layout().addWidget(self.data_frame)

        self.horizontalLayout.addWidget(self.main_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    class MplCanvas(FigureCanvas):
        def __init__(self, parent=None, width=5, height=4, dpi=100):
            fig = Figure(figsize=(width, height), dpi=dpi)
            fig.patch.set_facecolor((44/255, 44/255, 44/255))
            self.axes = fig.add_subplot(111, facecolor=(44/255, 44/255, 44/255))
            self.axes.tick_params(axis='x', colors='silver')
            self.axes.tick_params(axis='y', colors='silver')

            for spine in self.axes.spines.values():
                spine.set_edgecolor('silver')

            super(Ui_MainWindow.MplCanvas, self).__init__(fig)

    def retranslateUi(self, Main_Window):
        Main_Window.setWindowTitle(QCoreApplication.translate(
            "MainWindow",
            u"Weather Data Virtualization",
            None))

    def add_plot_to_data_frame(self, plot_widget):
        self.data_frame.setLayout(QVBoxLayout())
        layout = self.data_frame.layout()
        layout.addWidget(plot_widget)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.current_plot_widget = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setStyleSheet("""
            QPushButton {
                color: rgb(184, 184, 184);
            }
            QFrame{
                border-radius: 5px;
            }
            QPushButton:hover {
                color: rgb(255, 255, 255);
            }
        """)
        self.ui.temp_button.clicked.connect(self.temperature)
        self.ui.preci_button.clicked.connect(self.precipitation)

    def add_plot(self, data, type):
        dates = [entry[1].__format__("%d.%m.%Y") for entry in data]
        second_value = [entry[2] for entry in data]

        sc = Ui_MainWindow.MplCanvas(self, width=8, height=6, dpi=100)
        sc.axes.plot(dates, second_value, color='silver', linestyle='solid', marker='.', linewidth=1)
        sc.axes.set_title(type, color='silver')
        sc.axes.set_xlabel("Date", color='silver')

        if type == 'Precipitation':
            type = type.replace('Precipitation', 'Precipitation in l/m²')
        if type == 'Temperature':
            type = type.replace('Temperature', 'Temperature in °C')

        sc.axes.set_ylabel(type, color='silver')

        if self.current_plot_widget is not None:
            self.ui.data_frame.layout().removeWidget(self.current_plot_widget)
            self.current_plot_widget.deleteLater()
        
        self.ui.add_plot_to_data_frame(sc)
        self.current_plot_widget = sc

    def temperature(self):
        temp_result = get_data.temperature()
        self.add_plot(temp_result, "Temperature")

    def precipitation(self):
        preci_result = get_data.precipitation()
        self.add_plot(preci_result, "Precipitation")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
