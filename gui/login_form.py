import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox

class LoginForm(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Username
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)

        # Password
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)

        # Role (for registration)
        self.role = QComboBox()
        self.role.addItems(["user", "admin"])
        layout.addWidget(QLabel("Role (for registration):"))
        layout.addWidget(self.role)

        # Buttons
        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login)
        btn_layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.register)
        btn_layout.addWidget(self.register_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password are required")
            return

        try:
            response = requests.post("http://localhost:8000/login/", json={
                "username": username,
                "password": password
            })
            response.raise_for_status()
            data = response.json()
            token = data["access_token"]
            role = data["role"]
            self.on_login_success(token, role)
            QMessageBox.information(self, "Success", f"Logged in as {username} ({role})")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")

    def register(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        role = self.role.currentText()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password are required")
            return

        try:
            response = requests.post("http://localhost:8000/register/", json={
                "username": username,
                "password": password,
                "role": role
            })
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Registration successful. Please log in.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Registration failed: {str(e)}")