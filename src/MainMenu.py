from PyQt5.QtWidgets import QMenuBar

class MainMenu(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        help_menu = self.addMenu('Справка')
        partner_menu = self.addMenu('Партнеры')

        self.__about = help_menu.addAction('Об этой программе')
        self.__about_qt = help_menu.addAction('О программе Qt...')
        self.__partner_add = partner_menu.addAction('Добавить')

    @property
    def about(self):
        return self.__about

    @property
    def about_qt(self):
        return self.__about_qt

    @property
    def partner_add(self):
        return self.__partner_add
