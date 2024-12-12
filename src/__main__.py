import sys
from Application import Application
from MainWindow import MainWindow
from PyQt5.QtGui import QFont

app = Application(sys.argv)
app.setFont(QFont("Segoe UI", 12))

main_window = MainWindow()
main_window.show()
result = app.exec()
sys.exit(result)


