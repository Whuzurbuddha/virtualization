import os

os.environ["QT_API"] = "pyside6"
import mysql.connector
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *


def get_weather_data():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user= username,
        password= ****,
        database= db.name
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM temperatures')
    results = cursor.fetchall()
    conn.close()
    return results


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('black')
        self.axes = fig.add_subplot(111, facecolor='black')
        self.axes.tick_params(axis='x', colors='silver')
        self.axes.tick_params(axis='y', colors='silver')
        super(MplCanvas, self).__init__(fig)


def retranslateUi(Main_Window):
    Main_Window.setWindowTitle(QCoreApplication.translate("MainWindow",
                                                          u"Weather Data Virtualization",
                                                          None))


class Ui_MainWindow(object):
    def __init__(self):
        self.verticalLayout = None
        self.centralwidget = None

    def setupUi(self, Main_Window):
        if not Main_Window.objectName():
            Main_Window.setObjectName(u"MainWindow")
        Main_Window.resize(847, 555)
        self.centralwidget = QWidget(Main_Window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")

        Main_Window.setCentralWidget(self.centralwidget)

        retranslateUi(Main_Window)

        QMetaObject.connectSlotsByName(Main_Window)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.add_plot()

    def add_plot(self):
        data = get_weather_data()
        dates = [entry[1] for entry in data]
        temperatures = [entry[2] for entry in data]

        sc = MplCanvas(self, width=8, height=6, dpi=100)
        sc.axes.plot(dates, temperatures, color='silver', linestyle='solid', marker='.', linewidth=1)
        sc.axes.set_title("Temperatures", color='silver')
        sc.axes.set_xlabel("Date", color='silver')
        sc.axes.set_ylabel("Temperature", color='silver')

        self.ui.verticalLayout.addWidget(sc)

        sc.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
