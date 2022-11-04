import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from addEditCoffeeForm import Ui_Form
from Main1 import Ui_coffee


class New_coffee(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_btn.clicked.connect(self.new_coffee)
        self.show_btn.clicked.connect(self.show_coffee)
        self.save_btn.clicked.connect(self.save_coffee)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.modified = {}
        self.titles = None

    def new_coffee(self):
        con = sqlite3.connect('./data/coffee.sqlite')
        cursor = con.cursor()
        name = self.name_coff.text()
        deg = self.degree_of_roasting_coff.text()
        typecoff = self.type_coff.text()
        taste = self.taste_coff.text()
        price = self.price_coff.text()
        valume = self.volume_coff.text()
        try:
            assert name != ''
            assert deg != '' and deg.isdigit()
            assert typecoff != '' and typecoff.isalpha()
            assert taste != ''
            assert price != '' and price.isdigit()
            assert valume != '' and valume.isdigit()
            zapr = f"""INSERT INTO coffee(name, degree_of_roasting, type, taste, price, volume) 
            VALUES('{name}', '{deg}', '{typecoff}', '{taste}', '{price}', '{valume}')"""
            cursor.execute(zapr)
            self.mistake.setText('Запись успешно добавлен.')
            con.commit()
        except Exception:
            self.mistake.setText('Неправильно заполнена форма')

    def show_coffee(self):
        con = sqlite3.connect('./data/coffee.sqlite')
        cursor = con.cursor()
        self.id = self.id_coffe.text()
        try:
            assert self.id != '' and self.id.isdigit()
            res = cursor.execute(f"""SELECT * FROM coffee WHERE id = {self.id}""").fetchall()
            title = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                     'описание вкуса', 'цена', 'объем упаковки']
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            self.titles = [description[0] for description in cursor.description]
            for i, row in enumerate(res):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))
        except Exception:
            pass

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_coffee(self):
        con = sqlite3.connect('./data/coffee.sqlite')
        if self.modified:
            cur = con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            cur.execute(que, (self.id,))
            con.commit()
            self.modified.clear()


class MyWidget(QWidget, Ui_coffee):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show_btn.clicked.connect(self.showtable)
        self.add_btn.clicked.connect(self.newcoff)

    def showtable(self):
        con = sqlite3.connect('./data/coffee.sqlite')
        cursor = con.cursor()
        title = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                 'описание вкуса', 'цена', 'объем упаковки']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        res = cursor.execute("""SELECT * FROM coffee""").fetchall()
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def newcoff(self):
        self.neww = New_coffee()
        self.neww.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
