import sqlite3
import sys

from PyQt5.Qt import QMainWindow, QApplication

from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.fill_table()
        self.edit = None

        self.pushButton.clicked.connect(self.change_table)

    def fill_table(self):
        sql = """SELECT * FROM coffee"""
        data = self.cur.execute(sql).fetchall()
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        for i in range(len(data)):
            for j in range(len(data[0])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))
        self.tableWidget.resizeColumnsToContents()

    def change_table(self):
        edit_data = []
        if self.tableWidget.currentRow() != -1:
            i = self.tableWidget.currentRow()
            for j in range(self.tableWidget.columnCount()):
                edit_data.append(self.tableWidget.item(i, j).text())

        self.edit = EditCoffee(edit_data, self)
        self.edit.show()


class EditCoffee(QWidget):
    def __init__(self, data, p):
        super().__init__()

        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()
        self.p = p

        uic.loadUi('addEditCoffeeForm.ui', self)
        self.lineEdits = [self.lineEdit, self.lineEdit_2, self.lineEdit_3,
                          self.lineEdit_4, self.lineEdit_5, self.lineEdit_6,
                          self.lineEdit_7]
        if data:
            for i in range(len(self.lineEdits)):
                self.lineEdits[i].setText(data[i])

        self.pushButton.clicked.connect(self.save_btn)

    def save_btn(self):
        data = [line.text() for line in self.lineEdits]
        # print(data)
        try:
            data[0] = int(data[0])
            data[5] = int(data[5])
            data[6] = int(data[6])
            if not self.cur.execute("SELECT id FROM coffee WHERE id = ?", (data[0],)).fetchall():
                sql = """INSERT INTO coffee
                        VALUES (?, ?, ?, ?, ?, ?, ?)"""
                self.cur.execute(sql, (*data,))
            else:
                sql = """UPDATE coffee
                        SET name = ?, degree_of_roast = ?, ground_or_whole = ?,
                        taste = ?, price = ?, volume = ?
                        WHERE id = ?"""
                self.cur.execute(sql, (*data[1:], data[0]))
            self.con.commit()
            self.p.fill_table()
            self.close()

        except ValueError:
            self.error_label.setText('WARNING! Wrong Input!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
