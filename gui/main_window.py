from PyQt5.QtWidgets import QMainWindow, QTabWidget
from gui.login_form import LoginForm
from gui.booking_form import BookingForm
from gui.admin_panel import AdminPanel

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
        self.booking_form.setEnabled(True)
        self.booking_form.token = token  # Pass token to booking form
        self.admin_panel.setEnabled(role == "admin")
        self.admin_panel.token = token  # Pass token to admin panel
        self.tabs.setCurrentIndex(1)  # Switch to booking tab