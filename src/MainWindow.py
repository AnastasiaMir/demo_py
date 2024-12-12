

from db import get_partner_data, get_partner_type, get_discount, get_type_id, get_partner_id, alter_partner
from PyQt5.QtWidgets import (QListWidgetItem, QListWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
                             QPushButton, QDialog,
                             QMainWindow, QLineEdit, QTextEdit)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSlot, QSize
import validators
from MainMenu import MainMenu
from src.db import add_partner


class QCustomQWidget (QFrame):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.data = {}
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)
        lay = QHBoxLayout()
        self.text_lay = QVBoxLayout()
        self.text_lay.setSpacing(0)
        self.discount = QLabel()
        self.partner_name = QLabel()
        self.director = QLabel()
        self.phone = QLabel()
        self.rating = QLabel()
        self.text_lay.addWidget(self.partner_name)
        self.text_lay.addWidget(self.director)
        self.text_lay.addWidget(self.phone)
        self.text_lay.addWidget(self.rating)
        lay.addLayout(self.text_lay)
        lay.addWidget(self.discount)
        lay.setAlignment(self.discount, Qt.AlignTop | Qt.AlignRight)
        self.setLayout(lay)

        self.partner_name.setStyleSheet('''
            font-size: 24px;
        ''')
        self.discount.setStyleSheet('''
            font-size: 16px;
            margin: 10px;
        ''')

    def set_partner_name (self, text):
        self.partner_name.setText(text)

    def set_director(self, text):
        self.director.setText(text)

    def set_phone (self, text):
        self.phone.setText(text)
    def set_rating (self, text):
        self.rating.setText(text)

    def set_discount(self, text):
        self.discount.setText(text)

    def set_partner_id(self, id):
        self.__id = id

    @property
    def partner_id(self):
        self.id = None


    @partner_id.setter
    def get_partner_id(self):
        return self.id


class MainWindow (QMainWindow):
    def __init__ (self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("My Main Window")
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)
        main_menu.partner_add.triggered.connect(self.add_partner)
        self.setGeometry(100,100, 600, 800)
        self.current_data = []
        pixmap = QPixmap("icon.ico")
        pixmap = pixmap.scaled(QSize(16, 16))
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        self.myQListWidget = QListWidget(self)
        self.refresh()

        self.myQListWidget.setStyleSheet("""
            QListWidget::item:selected {
                background-color: #67BA80; 
            }
            QListWidget::item {
                background-color: #F4E8D3; 
                margin: 10px;
            }
        """)
        self.myQListWidget.itemClicked.connect(self.show_dialog)
        self.setCentralWidget(self.myQListWidget)

    @pyqtSlot()
    def add_partner(self):
        dialog = Dialog(parent=self)
        if dialog.exec_():
            self.refresh()
        else:
            print(f"Dialog cancelled")



    @pyqtSlot(QListWidgetItem)
    def show_dialog(self, item):
        item_widget = self.myQListWidget.itemWidget(item)
        if isinstance(item_widget, QCustomQWidget):
            dialog = Dialog(item_widget.data)
            if dialog.exec_():
                self.refresh()
            else:
                print(f"Dialog cancelled")
        else:
            print("Clicked item is not a QCustomQWidget")

    @pyqtSlot()
    def refresh(self):
        self.myQListWidget.clear()
        partners = get_partner_data()
        for p in partners:
            partner = list(p)
            partner_type = get_partner_type(int(partner[1]))
            discount = get_discount(partner[0])
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.set_partner_id(partner[0])
            myQCustomQWidget.data['type'] = partner_type[0]
            myQCustomQWidget.data['name'] = partner[2]
            myQCustomQWidget.data['director'] = partner[3]
            myQCustomQWidget.data['email'] = partner[4]
            myQCustomQWidget.data['phone'] = partner[5]
            myQCustomQWidget.data['address'] = partner[6]
            myQCustomQWidget.data['tax_number'] = partner[7]
            myQCustomQWidget.data['rating'] = partner[8]
            myQCustomQWidget.set_partner_name(f'{partner_type[0]} | {partner[2]}')
            myQCustomQWidget.set_director(f'{partner[3]}')
            myQCustomQWidget.set_phone(f'{partner[5]}')
            myQCustomQWidget.set_rating(f'Рейтинг: {partner[8]}')
            myQCustomQWidget.set_discount(discount)
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)


class Dialog(QDialog):
    def __init__(self, frame_data ={}, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle('Изменить данные партнера')

        type_lbl = QLabel('Форма организации предприятия', parent=self)
        self.type_edt = QLineEdit(parent=self)

        name_lbl = QLabel('Наименование предприятия', parent=self)
        self.name_edt = QLineEdit(parent=self)

        director_lbl = QLabel('Директор', parent=self)
        self.director_edt = QLineEdit(parent=self)

        email_lbl = QLabel('e-mail', parent=self)
        self.email_edt = QLineEdit(parent=self)

        phone_lbl = QLabel('Телефон', parent=self)
        self.phone_edt = QLineEdit(parent=self)

        address_lbl = QLabel('Адрес', parent=self)
        self.address_edt = QTextEdit(parent=self)

        tax_number_lbl = QLabel('ИНН', parent=self)
        self.tax_number_edt = QLineEdit(parent=self)

        rating_lbl = QLabel('Рейтинг', parent=self)
        self.rating_edt = QLineEdit(parent=self)

        ok_btn = QPushButton('Ok', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)
        cancel_btn.clicked.connect(self.reject)

        self.frame_data = frame_data
        self.type = frame_data.get('type', '')
        self.type_id = None if not bool(self.type) else get_type_id(self.type)
        self.name = frame_data.get('name', '')
        self.id = None if not bool(self.name) else get_partner_id(self.name)
        self.director = frame_data.get('director', '')
        self.email = frame_data.get('email', '')
        self.phone = frame_data.get('phone', '')
        self.address = frame_data.get('address', '')
        self.tax_number = frame_data.get('tax_number', '')
        self.rating = frame_data.get('rating', '')

        lay = QVBoxLayout(self)
        lay.setSpacing(5)
        lay.addWidget(type_lbl)
        lay.addWidget(self.type_edt)
        lay.addWidget(name_lbl)
        lay.addWidget(self.name_edt)
        lay.addWidget(director_lbl)
        lay.addWidget(self.director_edt)
        lay.addWidget(email_lbl)
        lay.addWidget(self.email_edt)
        lay.addWidget(phone_lbl)
        lay.addWidget(self.phone_edt)
        lay.addWidget(address_lbl)
        lay.addWidget(self.address_edt)
        lay.addWidget(tax_number_lbl)
        lay.addWidget(self.tax_number_edt)
        lay.addWidget(rating_lbl)
        lay.addWidget(self.rating_edt)

        hlay = QHBoxLayout()
        hlay.addWidget(ok_btn)
        hlay.addWidget(cancel_btn)
        hlay.addStretch()
        hlay.setSpacing(25)
        lay.addLayout(hlay)
        self.setLayout(lay)

        ok_btn.clicked.connect(self.finish)

    @pyqtSlot()
    def finish(self):

        def is_valid_email_validators(email):
            """Email validation using the 'validators' library."""
            return validators.email(email)

        if self.type not in ['ООО', 'ПАО', 'ОАО', 'ЗАО']:
            QMessageBox.information(self, 'Ошибка', 'Поле "Форма организации предприятия" заполнено неверно! Данной форма организации не существует!')
            return

        if self.name is None:
            QMessageBox.information(self, 'Ошибка', 'Поле "Наименование" не может быть пустым!')
            return

        if not is_valid_email_validators(self.email):
            QMessageBox.information(self, 'Ошибка', 'Заполните поле "Email" корректно!')
            return

        if self.id:
            alter_partner(self.id, self.type_id, self.name, self.director, self.email, self.phone, self.address, self.tax_number, self.rating)
        else:
            self.type_id = None if not bool(self.type) else get_type_id(self.type)
            add_partner(self.type_id, self.name, self.director, self.email, self.phone, self.address, self.tax_number, self.rating)
        self.accept()

    @property
    def type(self):
        result = self.type_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @type.setter
    def type(self, value):
        self.type_edt.setText(value)

    @property
    def name(self):
        result = self.name_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @name.setter
    def name(self, value):
        self.name_edt.setText(value)

    @property
    def director(self):
        result = self.director_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @director.setter
    def director(self, value):
        self.director_edt.setText(value)

    @property
    def email(self):
        result = self.email_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @email.setter
    def email(self, value):
        self.email_edt.setText(value)

    @property
    def phone(self):
        result = self.phone_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @phone.setter
    def phone(self, value):
        self.phone_edt.setText(value)

    @property
    def address(self):
        result = self.address_edt.toPlainText().strip()
        if result == '':
            return None
        else:
            return result

    @address.setter
    def address(self, value):
        self.address_edt.setText(value)

    @property
    def tax_number(self):
        result = self.tax_number_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @tax_number.setter
    def tax_number(self, value):
        self.tax_number_edt.setText(value)

    @property
    def rating(self):
        result = self.rating_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @rating.setter
    def rating(self, value):
        self.rating_edt.setText(str(value))

