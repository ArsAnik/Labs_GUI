import os
import sys

import PyQt5
from PyQt5.QtSql import  QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import (
    QApplication, QAction, QWidget, QMainWindow, QFileDialog,
    QTabWidget, QTableView, QVBoxLayout, QPushButton, QGridLayout,
    QComboBox, QDialog, QDialogButtonBox, QPlainTextEdit
)


pyqt_dir = os.path.dirname(PyQt5.__file__)
os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", os.path.join(pyqt_dir, "Qt5", "plugins"))


QUERY_1 = "SELECT * FROM users"
QUERY_2 = "SELECT name FROM users"
QUERY_3 = "SELECT * FROM users WHERE name like '%Петров%'"
QUERY_4 = "SELECT * FROM users WHERE age > 30"
QUERY_GET_COLUMS = "PRAGMA table_info(users)"
QUERY_COLUMS = 'SELECT "{colum_name}" FROM users'


class QueryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(400, 200)
        self.editor = QPlainTextEdit()

        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def sql(self):
        return self.editor.toPlainText().strip()


class DBWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(900, 400)
        self.db = None
        self.tabs = {}
        self.tables = []
        self.models = {}

        self.ui_init()

    def ui_init(self):
        central_widget = QWidget()
        box = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        menu = self.menuBar().addMenu("Menu")
        self.act_db_set = QAction("Set connection", self)
        self.act_db_close = QAction("Close connection", self)
        self.act_db_set.triggered.connect(self.set_connection)
        self.act_db_close.triggered.connect(self.close_connection)
        menu.addAction(self.act_db_set)
        menu.addAction(self.act_db_close)

        grid = QGridLayout()
        self.bt1 = QPushButton(QUERY_2)
        self.bt2 = QPushButton(QUERY_3)
        self.bt3 = QPushButton(QUERY_4)
        self.bt4 = QPushButton("Свой запрос")
        self.bt1.clicked.connect(self.on_bt1)
        self.bt2.clicked.connect(self.on_bt2)
        self.bt3.clicked.connect(self.on_bt3)
        self.bt4.clicked.connect(self.on_custom_query)
        grid.addWidget(self.bt1, 0, 0)
        grid.addWidget(self.bt2, 1, 0)
        grid.addWidget(self.bt3, 1, 1)
        grid.addWidget(self.bt4, 2, 0, 1, 2)

        self.list = QComboBox()
        grid.addWidget(self.list, 0, 1)
        self.list.activated.connect(self.on_colum_selected)
        box.addLayout(grid)

        self.tabs = QTabWidget()
        for i in range(1, 7):
            view = QTableView()
            view.setEditTriggers(QTableView.NoEditTriggers)
            self.tables.append(view)
            self.tabs.addTab(view, f"Tab{i}")
        box.addWidget(self.tabs, 1)
        self.setCentralWidget(central_widget)


    def add_colums(self):
        query = QSqlQuery(self.db)
        query.exec_(QUERY_GET_COLUMS)
        while query.next():
            self.list.addItem(query.value(1))
        query.finish() 


    def on_bt1(self):
        self.run_db_query(2, QUERY_2)

    def on_bt2(self):
        self.run_db_query(3, QUERY_3)

    def on_bt3(self):
        self.run_db_query(4, QUERY_4)

    def on_custom_query(self):
        modal_window = QueryDialog()
        if modal_window.exec_() == QDialog.Accepted and modal_window.sql():
            self.run_db_query(6, modal_window.sql())

    def on_colum_selected(self, index):
        colum_name = self.list.itemText(index)
        self.run_db_query(4, QUERY_COLUMS.format(colum_name=colum_name))


    def set_connection(self):
        file_name, file_extension = QFileDialog.getOpenFileName(self)

        db = QSqlDatabase.addDatabase("QSQLITE", "connection")
        db.setDatabaseName(file_name)
        db.open()
        self.db = db

        self.run_db_query(1, QUERY_1)
        self.tabs.setCurrentIndex(0)
        self.add_colums()


    def run_db_query(self, tab, sql):
        model = QSqlQueryModel(self)
        model.setQuery(sql, self.db)

        self.tables[tab - 1].setModel(model)
        self.models[tab] = model

        self.tables[tab - 1].resizeColumnsToContents()
        self.tabs.setCurrentIndex(tab - 1)

    def close_connection(self):
        for view in self.tables:
            view.setModel(None)
        for model in self.models.values():
            model.clear()
            model.deleteLater()
        self.models.clear()
        self.list.clear()

        self.db.close()
        self.db = None
        QSqlDatabase.removeDatabase("connection")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DBWindow()
    window.show()
    sys.exit(app.exec_())