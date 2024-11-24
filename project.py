import io
import csv
import sys
import sqlite3 
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidgetItem, QMainWindow, QGridLayout
from PyQt6.QtCore import QTimer, QTime
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QCoreApplication, Qt


class MainWindow_1(QMainWindow):
    '''
    Вступительное окно с приёмом паролей.
    '''
    def __init__(self,
                 /
            ) -> None: 
        '''
        Инициализация первого главного окна.  
        '''
        super().__init__()
        uic.loadUi('k_mainwindow.ui', self) 
        # подключаем все кнопки
        self.button_welcome.clicked.connect(self.winnum2)
        self.setGeometry(300, 400, 300, 400)
        self.label_pas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_pas.setProperty('class', 'enter')
        

    def winnum2(self,
                /
            ) -> None:
        '''
        Вызов второго главного окна.
        '''
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        s = csv.reader(open('projec1.csv'), delimiter=';')
        for i in s:
            if i[0] == name and i[1] == password:
                global dewinnum1, dewinnum2
                dewinnum2 = PasswordManager()
                dewinnum2.show()
                dewinnum1.hide() 
        self.lineEdit.clear()
        self.lineEdit_2.clear()


class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('password_manager1.ui', self)
        self.connection = sqlite3.connect("passwords.db")
        self.setWindowTitle('Парольный менеджер')

        self.line_write_it_down = QLineEdit('добавить пароль:')
        self.line_save = QLineEdit('сохранить пароль:')
        self.pushButton.clicked.connect(self.show_window_2)
        self.view_button = QPushButton('Просмотреть пароли')
        self.pushButton_2.clicked.connect(self.view)
        self.pushButton_3.clicked.connect(self.ism)
        self.pushButton_4.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.zapusk)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
        self.zapusk()
        self.modified = {}
        self.titles = None
        self.load_data()
    
    def update_time(self):
        time = QTime.currentTime()
        current_time = time.toString('hh:mm:ss')
        self.label.setText(current_time)

    def load_data(self):
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()

        # Получаем данные из базы данных
        cursor.execute("SELECT * FROM passwords")
        data = cursor.fetchall()
        # Заполним размеры таблицы
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.connection.close()
    
    def view(self):
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        # здесь мы обновляем данные в базе данных
        cursor.execute("SELECT * FROM passwords")
        data = cursor.fetchall()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))

        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

        conn.close()
    
    
    def zapusk(self):
        password_name = self.line_1Edit.text()
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()

    # Ищем пароли с заданным названием
        cursor.execute("SELECT * FROM passwords WHERE name=?", (password_name,))
        results = cursor.fetchall()

    # Очищаем таблицу перед добавлением новых данных
        self.tableWidget.setRowCount(0)

    # Добавляем найденные пароли в таблицу
        for row_num, row_data in enumerate(results):
            self.tableWidget.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_num, col_num, item)

    # Закрываем соединение с базой данных
        conn.close()
    
    def show_window_2(self):
        self.w2 = PasswordManager1()
        self.w2.show()
    
    def ism(self):
        self.w3 = PasswordManager2()
        self.w3.show()
    
    def delete(self):
        self.w4 = PasswordManager3()
        self.w4.show()
        
        
class PasswordManager3(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pasdelete')
        self.setGeometry(100, 100, 300, 150)
        layout = QVBoxLayout()
        self.label_name = QLabel('название:')
        self.edit_name = QLineEdit()
        layout.addWidget(self.label_name)
        layout.addWidget(self.edit_name)
        # создаем кнопку для удаления данных из базы данных
        self.btn_save = QPushButton('удалить')
        self.btn_save.clicked.connect(self.delete_to_db)
        layout.addWidget(self.btn_save)
        self.setLayout(layout)
        
    
    def delete_to_db(self):
        name2 = self.edit_name.text()
        if name2:
            conn = sqlite3.connect('passwords.db')
            cursor = conn.cursor()
            # в этой функции удаляем пароль по названию
            cursor.execute("DELETE FROM passwords WHERE name = ?", (name2,  ))
            conn.commit()
        # здесь очищаем ввод данных после ввода данных в них
        self.edit_name.clear()
    
    
class PasswordManager2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pas')
        self.setGeometry(100, 100, 300, 150)
        # создаем вид окна
        # создаем кнопки для окна
        layout = QVBoxLayout()
        
        self.label_name = QLabel('название:')
        self.edit_name = QLineEdit()
        layout.addWidget(self.label_name)
        layout.addWidget(self.edit_name)

        self.label_password = QLabel('пароль:')
        self.edit_password = QLineEdit()
        layout.addWidget(self.label_password)
        layout.addWidget(self.edit_password)

        self.btn_save = QPushButton('изменить')
        # делаем кнопку для изменений в базе данных
        self.btn_save.clicked.connect(self.isme_to_db)    
        layout.addWidget(self.btn_save)

        self.setLayout(layout)
    
    
    def isme_to_db(self):
        name1 = self.edit_name.text()
        password1 = self.edit_password.text()
        if name1.strip() and password1.strip():
            conn = sqlite3.connect('passwords.db')
            cursor = conn.cursor()
            # в этой функции обновляем данные в базе данных
            cursor.execute("UPDATE passwords SET password = ? WHERE name = ? ", (password1, name1))
            conn.commit()
        # здесь очищаем ввод данных после ввода данных в них
        self.edit_name.clear()
        self.edit_password.clear()


class PasswordManager1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Password Manager')
        # создаем вид окна
        self.setGeometry(100, 100, 300, 150)
        layout = QVBoxLayout()
        self.label_name = QLabel('название:')
        self.edit_name = QLineEdit()
        layout.addWidget(self.label_name)
        layout.addWidget(self.edit_name)
        self.label_password = QLabel('пароль:')
        self.edit_password = QLineEdit()
        layout.addWidget(self.label_password)
        layout.addWidget(self.edit_password)
        # делаем кнопку для сохоанения в базу данных
        self.btn_save = QPushButton('Save')
        self.btn_save.clicked.connect(self.save_to_db)
        layout.addWidget(self.btn_save)
        self.setLayout(layout)

    def save_to_db(self):
        name = self.edit_name.text()
        password = self.edit_password.text()
        # создаем таблицу и записываем туда значения
        if name.strip() and password.strip():
            connection = sqlite3.connect('passwords.db')
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS passwords (name TEXT, password TEXT)")
            cursor.execute("INSERT INTO passwords VALUES (?, ?)", (name, password))
            connection.commit()
        # здесь очищаем ввод данных после ввода данных в них
        self.edit_name.clear()
        self.edit_password.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dewinnum1 = MainWindow_1()
    dewinnum1.setStyleSheet('''
            .enter {
                color: #0c31ed;
                font-size: 25px;
            }                
                            
            QMainWindow{
                background-color: QLinearGradient(x0: 0, y0: 0, x1: 0, y1: 1, stop: 0 #97D9E1, stop: 1 #D9AFD9);
            }

            QPushButton {
                background-color: QLinearGradient(x0: 0, y0: 0, x1: 0, y1: 1, stop: 0 #85FFBD, stop: 1 #FFFB7D);
                padding: 5px;
                border: none;
                border-radius: 5px;
                margin: 10px 0 0 0;
                color: black;
            }

            QLineEdit {
                background-color: QLinearGradient(x0: 0, y0: 0, x1: 0, y1: 1, stop: 0 #85FFBD, stop: 1 #FFFB7D);
                padding: 5px;
                border: none;
                border-radius: 5px;
                margin: 10px 0 0 0;
                color: black;
            }
            
            QLabel {
                color: black;
                font-size: 14px;
            }
            '''
        )
    dewinnum1.show() 
    sys.exit(app.exec())

