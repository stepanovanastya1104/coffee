import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        print('scasa')
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cursor = self.con.cursor()
        self.title = ['ID', 'Название', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                      'описание вкуса', 'цена', 'объем упаковки']
        self.show_btn.clicked.connect(self.show)

    def show(self):
        self.tableWidget.setColumnCount(len(self.title))
        self.tableWidget.setHorizontalHeaderLabels(self.title)
        self.tableWidget.setRowCount(0)
        res = self.cursor.execute("""SELECT * FROM coffee""").fetchall()
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())