import sqlite3
import sys

from PyQt5.Qt import QMainWindow, QApplication

from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.fill_table()

    def fill_table(self):
        sql = """SELECT * FROM coffee"""
        data = self.cur.execute(sql).fetchall()
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        for i in range(len(data)):
            for j in range(len(data[0])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
