import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from PyQt5.QtGui import QIcon

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set the application icon
    app.setWindowIcon(QIcon("static/images/yarlik.icocd"))  # Path to the icon file
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    