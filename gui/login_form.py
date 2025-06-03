import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QGridLayout
from PyQt5.QtCore import Qt

class LoginForm(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.init_ui()

    def init_ui(self):
        # Основной макет
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        # GridLayout для полей ввода
        grid = QGridLayout()
        grid.setSpacing(10)

        # Username
        self.username = QLineEdit()
        self.username.setPlaceholderText("Имя пользователя")
        grid.addWidget(QLabel("Имя пользователя:"), 0, 0)
        grid.addWidget(self.username, 0, 1)

        # Password
        self.password = QLineEdit()
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QLineEdit.Password)
        grid.addWidget(QLabel("Пароль:"), 1, 0)
        grid.addWidget(self.password, 1, 1)

        # Role (for registration) - initially hidden
        self.role_label = QLabel("Роль (для регистрации):")
        self.role = QComboBox()
        self.role.addItems(["Пользователь", "Администратор"])
        self.role_label.setVisible(False)
        self.role.setVisible(False)
        grid.addWidget(self.role_label, 2, 0)
        grid.addWidget(self.role, 2, 1)

        layout.addLayout(grid)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.login)
        btn_layout.addWidget(self.login_btn)

        self.register_btn = QPushButton("Зарегистрироваться")
        self.register_btn.clicked.connect(self.show_register_fields)
        btn_layout.addWidget(self.register_btn)

        self.register_confirm_btn = QPushButton("Подтвердить регистрацию")
        self.register_confirm_btn.clicked.connect(self.register)
        self.register_confirm_btn.setVisible(False)
        btn_layout.addWidget(self.register_confirm_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Применение стилей
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QLabel {
                color: #333;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
            }
        """)

    def show_register_fields(self):
        self.role_label.setVisible(True)
        self.role.setVisible(True)
        self.register_btn.setVisible(False)
        self.register_confirm_btn.setVisible(True)

    def login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка ввода", "Требуются имя пользователя и пароль")
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
            QMessageBox.information(self, "Успех", f"Вы вошли как {username} ({'Администратор' if role == 'admin' else 'Пользователь'})")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось войти: {str(e)}")

    def register(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        role = "admin" if self.role.currentText() == "Администратор" else "user"
        if not username or not password:
            QMessageBox.warning(self, "Ошибка ввода", "Требуются имя пользователя и пароль")
            return

        try:
            response = requests.post("http://localhost:8000/register/", json={
                "username": username,
                "password": password,
                "role": role
            })
            response.raise_for_status()
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно. Пожалуйста, войдите.")
            # Скрываем поле роли после успешной регистрации
            self.role_label.setVisible(False)
            self.role.setVisible(False)
            self.register_btn.setVisible(True)
            self.register_confirm_btn.setVisible(False)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось зарегистрироваться: {str(e)}")