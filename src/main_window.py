class MainWindow (QMainWindow):
    def __init__ (self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("My Main Window")
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)
        main_menu.partner_add.triggered.connect(self.add_partner)
        self.setGeometry(100,100, 600, 800)
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

    def _create_list_item(self, data):
         myQCustomQWidget = QCustomQWidget()
         myQCustomQWidget.set_data(data)
         discount = get_discount(data['id'])
         myQCustomQWidget.set_discount(discount)
         myQListWidgetItem = QListWidgetItem(self.myQListWidget)
         myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
         self.myQListWidget.addItem(myQListWidgetItem)
         self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

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
            dialog = Dialog(item_widget.data, parent=self)
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
           partner_data = {
              'id': partner[0],
               'type': partner_type[0],
               'name': partner[2],
              'director': partner[3],
                'email': partner[4],
               'phone': partner[5],
               'address': partner[6],
               'tax_number': partner[7],
               'rating': partner[8]
           }
           self._create_list_item(partner_data)