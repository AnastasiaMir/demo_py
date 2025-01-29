from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel

from PyQt5.QtCore import Qt


class QCustomQWidget(QFrame):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.data = {}
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)
        lay = QHBoxLayout()
        self.text_lay = QVBoxLayout()
        self.text_lay.setSpacing(0)
        self.discount = QLabel()
        self.labels = {
            "partner_name": QLabel(),
            "director": QLabel(),
            "phone": QLabel(),
            "rating": QLabel(),
        }
        self.text_lay.addWidget(self.labels["partner_name"])
        self.text_lay.addWidget(self.labels["director"])
        self.text_lay.addWidget(self.labels["phone"])
        self.text_lay.addWidget(self.labels["rating"])
        lay.addLayout(self.text_lay)
        lay.addWidget(self.discount)
        lay.setAlignment(self.discount, Qt.AlignTop | Qt.AlignRight)
        self.setLayout(lay)

        self.labels["partner_name"].setStyleSheet(
            """
            font-size: 24px;
        """
        )
        self.discount.setStyleSheet(
            """
            font-size: 24px;
        """
        )

    def set_data(self, data):
        self.data = data
        self.labels["partner_name"].setText(
            f'{data.get("type", "")} | {data.get("name", "")}'
        )
        self.labels["director"].setText(f'{data.get("director", "")}')
        self.labels["phone"].setText(f'{data.get("phone", "")}')
        self.labels["rating"].setText(f'Рейтинг: {data.get("rating", "")}')

    def set_discount(self, text):
        self.discount.setText(text)
