import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QCheckBox, QDateEdit, QMessageBox, QGridLayout, QGroupBox
from PyQt5.QtCore import QDate, Qt


class BookingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.token = None  # Store the token
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        # Группа для выбора события
        event_group = QGroupBox("Детали мероприятия")
        event_layout = QGridLayout()
        event_layout.setSpacing(10)

        # Event Type
        self.event_type = QComboBox()
        self.event_type.addItems(["День рождения", "Мастер-класс"])
        event_layout.addWidget(QLabel("Тип мероприятия:"), 0, 0)
        event_layout.addWidget(self.event_type, 0, 1)

        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumDate(QDate.currentDate())
        event_layout.addWidget(QLabel("Дата:"), 1, 0)
        event_layout.addWidget(self.date_edit, 1, 1)

        # Guest Count
        self.guest_count = QLineEdit()
        self.guest_count.setPlaceholderText("Количество гостей")
        event_layout.addWidget(QLabel("Количество гостей:"), 2, 0)
        event_layout.addWidget(self.guest_count, 2, 1)

        # Phone
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Номер телефона")
        event_layout.addWidget(QLabel("Номер телефона:"), 3, 0)
        event_layout.addWidget(self.phone, 3, 1)

        # Child Name
        self.child_name = QLineEdit()
        self.child_name.setPlaceholderText("Имя ребенка")
        event_layout.addWidget(QLabel("Имя ребенка:"), 4, 0)
        event_layout.addWidget(self.child_name, 4, 1)

        # Program
        self.program = QComboBox()
        event_layout.addWidget(QLabel("Программа:"), 5, 0)
        event_layout.addWidget(self.program, 5, 1)

        event_group.setLayout(event_layout)
        layout.addWidget(event_group)

        # Группа для дополнительных услуг
        addons_group = QGroupBox("Дополнительные услуги")
        self.addon_layout = QVBoxLayout()
        self.addon_checkboxes = []
        self.addon_layout.addWidget(QLabel("Выберите дополнительные услуги:"))
        addons_group.setLayout(self.addon_layout)
        layout.addWidget(addons_group)

        # Группа для мастер-классов
        masterclass_group = QGroupBox("Мастер-классы")
        self.masterclass_layout = QVBoxLayout()
        self.masterclass_checkboxes = []
        self.masterclass_layout.addWidget(QLabel("Выберите мастер-классы:"))
        masterclass_group.setLayout(self.masterclass_layout)
        layout.addWidget(masterclass_group)

        # Submit Button
        self.submit_btn = QPushButton("Создать заказ")
        self.submit_btn.clicked.connect(self.submit_booking)
        layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        # Применение стилей
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                font-family: Arial;
                font-size: 14px;
            }
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
                color: #333;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QCheckBox {
                spacing: 5px;
            }
            QLabel {
                color: #333;
            }
        """)

    def set_token(self, token):
        self.token = token
        self.load_data()

    def load_data(self):
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            # Load programs
            response = requests.get("http://localhost:8000/programs/", headers=headers)
            response.raise_for_status()
            programs = response.json()
            if not isinstance(programs, list):
                raise ValueError("Programs data is not a list")
            self.program.clear()
            self.program.addItems([f"{p['name']} ({p['price']} руб.)" for p in programs])
            self.program.setProperty("programs", programs)

            # Load add-ons
            response = requests.get("http://localhost:8000/addons/", headers=headers)
            response.raise_for_status()
            addons = response.json()
            if not isinstance(addons, list):
                raise ValueError("Addons data is not a list")
            for checkbox in self.addon_checkboxes:
                checkbox.deleteLater()
            self.addon_checkboxes = []
            for addon in addons:
                checkbox = QCheckBox(f"{addon['name']} ({addon['price']} руб.)")
                checkbox.setProperty("addon_id", addon["id"])
                self.addon_layout.addWidget(checkbox)
                self.addon_checkboxes.append(checkbox)

            # Load masterclasses
            response = requests.get("http://localhost:8000/masterclasses/", headers=headers)
            response.raise_for_status()
            masterclasses = response.json()
            if not isinstance(masterclasses, list):
                raise ValueError("Masterclasses data is not a list")
            for checkbox in self.masterclass_checkboxes:
                checkbox.deleteLater()
            self.masterclass_checkboxes = []
            for mc in masterclasses:
                checkbox = QCheckBox(f"{mc['name']} ({mc['price_per_child']} руб./ребенок)")
                checkbox.setProperty("masterclass_id", mc["id"])
                self.masterclass_layout.addWidget(checkbox)
                self.masterclass_checkboxes.append(checkbox)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")
            self.program.setProperty("programs", [])

    def submit_booking(self):
        try:
            guest_count = int(self.guest_count.text())
            if guest_count <= 0:
                raise ValueError("Количество гостей должно быть больше 0")
            phone = self.phone.text().strip()
            if not phone:
                raise ValueError("Требуется номер телефона")
            child_name = self.child_name.text().strip()
            if not child_name:
                raise ValueError("Требуется имя ребенка")

            program_idx = self.program.currentIndex()
            programs = self.program.property("programs")
            if not programs or program_idx < 0 or program_idx >= len(programs):
                raise ValueError("Выберите действительную программу")
            program_id = programs[program_idx]["id"]

            addon_ids = [cb.property("addon_id") for cb in self.addon_checkboxes if cb.isChecked()]
            masterclass_ids = [cb.property("masterclass_id") for cb in self.masterclass_checkboxes if cb.isChecked()]

            booking_data = {
                "date": self.date_edit.date().toString("yyyy-MM-dd"),
                "event_type": "День рождения" if self.event_type.currentText() == "День рождения" else "Мастер-класс",
                "guest_count": guest_count,
                "phone": phone,
                "child_name": child_name,
                "program_id": program_id,
                "addon_ids": addon_ids,
                "masterclass_ids": masterclass_ids
            }

            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post("http://localhost:8000/bookings/", json=booking_data, headers=headers)
            response.raise_for_status()
            result = response.json()
            QMessageBox.information(self, "Успех",
                f"Заказ создан! Итого: {result['total_price']} руб.\n"
                "Оплата в конце мероприятия.\n"
                "Администратор позвонит для подтверждения.")
            self.clear_form()
        except ValueError as ve:
            QMessageBox.warning(self, "Ошибка ввода", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать заказ: {str(e)}")

    def clear_form(self):
        self.guest_count.clear()
        self.phone.clear()
        self.child_name.clear()
        self.program.setCurrentIndex(0)
        for cb in self.addon_checkboxes:
            cb.setChecked(False)
        for cb in self.masterclass_checkboxes:
            cb.setChecked(False)
        self.date_edit.setDate(QDate.currentDate())