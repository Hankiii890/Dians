from PyQt5.QtWidgets import QMainWindow, QTabWidget
from gui.login_form import LoginForm
from gui.booking_form import BookingForm
from gui.admin_panel import AdminPanel
from PyQt5.QtCore import QTimer  # Добавьте этот импорт


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Booking App")
        self.setGeometry(100, 100, 400, 600)
        self.token = None  # Store the token after login
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Login/Register Tab
        self.login_form = LoginForm(self.on_login_success)
        self.tabs.addTab(self.login_form, "Login/Register")

        # Book Event Tab
        self.booking_form = BookingForm()
        self.booking_form.setEnabled(False)  # Disable until login
        self.tabs.addTab(self.booking_form, "Book Event")

        # Admin Panel Tab
        self.admin_panel = AdminPanel()
        self.admin_panel.setEnabled(False)  # Disable until login
        self.tabs.addTab(self.admin_panel, "Admin Panel")

    def on_login_success(self, token, role):
        self.token = token

        # Включение форм
        self.booking_form.setEnabled(True)
        self.booking_form.token = token
        self.admin_panel.setEnabled(role == "admin")
        self.admin_panel.token = token

        # Функция для установки токенов
        def set_tokens():
            self.booking_form.set_token(token)
            if role == "admin":
                self.admin_panel.set_token(token)

        # Функция для переключения таба
        def switch_tab():
            self.tabs.setCurrentIndex(1)

        # Запускаем с задержкой
        QTimer.singleShot(1000, set_tokens)
        QTimer.singleShot(1000, switch_tab)