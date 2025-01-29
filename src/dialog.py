from db import  get_type_id, alter_partner
from PyQt5.QtWidgets import ( QMessageBox, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
                             QPushButton, QDialog,
                             QLineEdit, QTextEdit)

from PyQt5.QtCore import Qt, pyqtSlot, QSize
import validators

from src.db import add_partner
class Dialog(QDialog):
   def __init__(self, frame_data ={}, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle('Изменить данные партнера')
        self.fields = {
              'type': {'label': QLabel('Форма организации предприятия', parent=self), 'widget': QLineEdit(parent=self)},
              'name': {'label': QLabel('Наименование предприятия', parent=self), 'widget': QLineEdit(parent=self)},
              'director': {'label': QLabel('Директор', parent=self), 'widget': QLineEdit(parent=self)},
              'email': {'label': QLabel('e-mail', parent=self), 'widget': QLineEdit(parent=self)},
              'phone': {'label': QLabel('Телефон', parent=self), 'widget': QLineEdit(parent=self)},
              'address': {'label': QLabel('Адрес', parent=self), 'widget': QTextEdit(parent=self)},
              'tax_number': {'label': QLabel('ИНН', parent=self), 'widget': QLineEdit(parent=self)},
              'rating': {'label': QLabel('Рейтинг', parent=self), 'widget': QLineEdit(parent=self)}
           }
        ok_btn = QPushButton('Ok', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)
        cancel_btn.clicked.connect(self.reject)
        self.frame_data = frame_data
        lay = QVBoxLayout(self)
        lay.setSpacing(5)
        for field_name, field_config in self.fields.items():
            lay.addWidget(field_config['label'])
            lay.addWidget(field_config['widget'])
            field_config['widget'].setText(str(self.frame_data.get(field_name, "")))
        hlay = QHBoxLayout()
        hlay.addWidget(ok_btn)
        hlay.addWidget(cancel_btn)
        hlay.addStretch()
        hlay.setSpacing(25)
        lay.addLayout(hlay)
        self.setLayout(lay)
        ok_btn.clicked.connect(self.finish)
   def _is_valid_email_validators(self, email):
        """Email validation using the 'validators' library."""
        return validators.email(email)
   @pyqtSlot()
   def finish(self):
       if not self.name:
           QMessageBox.information(self, 'Ошибка', 'Поле "Наименование" не может быть пустым!')
           return

       if not self._is_valid_email_validators(self.email):
           QMessageBox.information(self, 'Ошибка', 'Заполните поле "Email" корректно!')
           return

       data = {field_name: field_config['widget'].text().strip() for field_name, field_config in self.fields.items()}
       partner_id = self.frame_data.get('id')
       if partner_id:
           alter_partner(partner_id, None, data['name'], data['director'], data['email'], data['phone'], data['address'], data['tax_number'], data['rating'])
       else:
          partner_type_id = None if not bool(data['type']) else get_type_id(data['type'])
          add_partner(partner_type_id, data['name'], data['director'], data['email'], data['phone'], data['address'], data['tax_number'], data['rating'])
       self.accept()
   @property
   def name(self):
        result = self.fields['name']['widget'].text().strip()
        if result == '':
           return None
        else:
            return result
   @property
   def email(self):
        result = self.fields['email']['widget'].text().strip()
        if result == '':
           return None
        else:
            return result