import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, QMessageBox


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.token = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Bookings Table
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "ID", "Дата", "Тип", "Гости", "Телефон", "Имя ребенка",
            "ID программы", "Доп. услуги", "Мастер-классы", "Итого", "Статус"
        ])
        layout.addWidget(self.table)

        # Buttons Layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.refresh_btn = QPushButton("Обновить заказы")
        self.refresh_btn.clicked.connect(self.load_bookings)
        btn_layout.addWidget(self.refresh_btn)

        self.delete_btn = QPushButton("Удалить заказ")
        self.delete_btn.clicked.connect(self.delete_booking)
        btn_layout.addWidget(self.delete_btn)

        self.complete_btn = QPushButton("Отметить как завершенное")
        self.complete_btn.clicked.connect(self.mark_completed)
        btn_layout.addWidget(self.complete_btn)

        layout.addLayout(btn_layout)

        # Admin Actions
        admin_layout = QHBoxLayout()
        admin_layout.setSpacing(10)

        self.add_program_btn = QPushButton("Добавить программу")
        self.add_program_btn.clicked.connect(self.add_program)
        admin_layout.addWidget(self.add_program_btn)

        self.add_addon_btn = QPushButton("Добавить доп. услугу")
        self.add_addon_btn.clicked.connect(self.add_addon)
        admin_layout.addWidget(self.add_addon_btn)

        self.add_masterclass_btn = QPushButton("Добавить мастер-класс")
        self.add_masterclass_btn.clicked.connect(self.add_masterclass)
        admin_layout.addWidget(self.add_masterclass_btn)

        self.delete_program_btn = QPushButton("Удалить программу")
        self.delete_program_btn.clicked.connect(self.delete_program)
        admin_layout.addWidget(self.delete_program_btn)

        self.delete_addon_btn = QPushButton("Удалить доп. услугу")
        self.delete_addon_btn.clicked.connect(self.delete_addon)
        admin_layout.addWidget(self.delete_addon_btn)

        self.delete_masterclass_btn = QPushButton("Удалить мастер-класс")
        self.delete_masterclass_btn.clicked.connect(self.delete_masterclass)
        admin_layout.addWidget(self.delete_masterclass_btn)

        layout.addLayout(admin_layout)
        self.setLayout(layout)

        # Применение стилей
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                font-family: Arial;
                font-size: 14px;
            }
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QPushButton {
                background-color: #ff6f61;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e65b50;
            }
            QPushButton#complete_btn {
                background-color: #28a745;
            }
            QPushButton#complete_btn:hover {
                background-color: #218838;
            }
        """)

    def set_token(self, token):
        self.token = token
        self.load_bookings()

    def load_bookings(self):
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get("http://localhost:8000/bookings/", headers=headers)
            response.raise_for_status()
            bookings = response.json()
            self.table.setRowCount(len(bookings))
            for row, booking in enumerate(bookings):
                self.table.setItem(row, 0, QTableWidgetItem(str(booking["id"])))
                self.table.setItem(row, 1, QTableWidgetItem(booking["date"]))
                self.table.setItem(row, 2, QTableWidgetItem(booking["event_type"]))
                self.table.setItem(row, 3, QTableWidgetItem(str(booking["guest_count"])))
                self.table.setItem(row, 4, QTableWidgetItem(booking["phone"]))
                self.table.setItem(row, 5, QTableWidgetItem(booking["child_name"]))
                self.table.setItem(row, 6, QTableWidgetItem(str(booking["program_id"])))
                self.table.setItem(row, 7, QTableWidgetItem(str(booking["addon_ids"])))
                self.table.setItem(row, 8, QTableWidgetItem(str(booking["masterclass_ids"])))
                self.table.setItem(row, 9, QTableWidgetItem(str(booking["total_price"])))
                status = "Завершено" if booking["completed"] else "Активно"
                self.table.setItem(row, 10, QTableWidgetItem(status))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить заказы: {str(e)}")

    def delete_booking(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка выбора", "Выберите заказ для удаления")
            return
        booking_id = int(self.table.item(selected, 0).text())
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.delete(f"http://localhost:8000/bookings/{booking_id}", headers=headers)
            response.raise_for_status()
            self.load_bookings()
            QMessageBox.information(self, "Успех", "Заказ удален")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить заказ: {str(e)}")

    def mark_completed(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка выбора", "Выберите заказ для отметки")
            return
        booking_id = int(self.table.item(selected, 0).text())
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.put(f"http://localhost:8000/bookings/{booking_id}/complete", headers=headers)
            response.raise_for_status()
            self.load_bookings()
            QMessageBox.information(self, "Успех", "Заказ отмечен как завершенный")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось отметить заказ: {str(e)}")

    def add_program(self):
        name, ok = QInputDialog.getText(self, "Добавить программу", "Название программы:")
        if not ok or not name:
            return
        price, ok = QInputDialog.getInt(self, "Добавить программу", "Цена (руб.):", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post("http://localhost:8000/programs/", json={"name": name, "price": price}, headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Успех", "Программа добавлена")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить программу: {str(e)}")

    def add_addon(self):
        name, ok = QInputDialog.getText(self, "Добавить доп. услугу", "Название услуги:")
        if not ok or not name:
            return
        price, ok = QInputDialog.getInt(self, "Добавить доп. услугу", "Цена (руб.):", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post("http://localhost:8000/addons/", json={"name": name, "price": price}, headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Успех", "Доп. услуга добавлена")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить доп. услугу: {str(e)}")

    def add_masterclass(self):
        name, ok = QInputDialog.getText(self, "Добавить мастер-класс", "Название мастер-класса:")
        if not ok or not name:
            return
        price, ok = QInputDialog.getInt(self, "Добавить мастер-класс", "Цена за ребенка (руб.):", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post("http://localhost:8000/masterclasses/", json={"name": name, "price_per_child": price}, headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Успех", "Мастер-класс добавлен")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить мастер-класс: {str(e)}")

    def delete_program(self):
        program_id, ok = QInputDialog.getInt(self, "Удалить программу", "ID программы:", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.delete(f"http://localhost:8000/programs/{program_id}", headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Успех", "Программа удалена")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить программу: {str(e)}")

    def delete_addon(self):
        addon_id, ok = QInputDialog.getInt(self, "Удалить доп. услугу", "ID услуги:", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.delete(f"http://localhost:8000/addons/{addon_id}", headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Успех", "Доп. услуга удалена")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить доп. услугу: {str(e)}")

    def delete_masterclass(self):
        masterclass_id, ok = QInputDialog.getInt(self, "Удалить мастер-класс", "ID мастер-класса:", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.delete(f"http://localhost:8000/masterclasses/{masterclass_id}", headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Успех", "Мастер-класс удален")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить мастер-класс: {str(e)}")