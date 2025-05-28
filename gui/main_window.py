from PyQt5.QtWidgets import QMainWindow, QTabWidget
from gui.login_form import LoginForm
from gui.booking_form import BookingForm
from gui.admin_panel import AdminPanel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для бронирования мероприятий")
        self.setGeometry(100, 100, 600, 700)
        self.token = None
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Login/Register Tab
        self.login_form = LoginForm(self.on_login_success)
        self.tabs.addTab(self.login_form, "Вход/Регистрация")

        # Book Event Tab
        self.booking_form = BookingForm()
        self.booking_form.setEnabled(False)
        self.tabs.addTab(self.booking_form, "Создать заказ")

        # Admin Panel Tab
        self.admin_panel = AdminPanel()
        self.admin_panel.setEnabled(False)
        self.tabs.addTab(self.admin_panel, "Панель администратора")

        # Set background image using QPalette
        palette = QPalette()
        pixmap = QPixmap("static/images/Fon_application.jpg")
        pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

        # Apply stylesheet for transparency and tab styling
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 5px;
                background: transparent;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #4a90e2;
                color: white;
            }
            QWidget {
                background: transparent;
            }
        """)

    def resizeEvent(self, event):
        # Update background image on resize
        palette = self.palette()
        pixmap = QPixmap("static/images/Fon_application.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)
        super().resizeEvent(event)

    def on_login_success(self, token, role):
        self.token = token
        self.booking_form.setEnabled(True)
        self.booking_form.token = token
        self.admin_panel.setEnabled(role == "admin")
        self.admin_panel.token = token

        def set_tokens():
            self.booking_form.set_token(token)
            if role == "admin":
                self.admin_panel.set_token(token)

        def switch_tab():
            self.tabs.setCurrentIndex(1)

        QTimer.singleShot(1000, set_tokens)
        QTimer.singleShot(1000, switch_tab)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())