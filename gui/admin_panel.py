import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, QMessageBox

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.token = None  # Store the token
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Bookings Table
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Event Type", "Guests", "Phone", "Child Name",
            "Program ID", "Add-ons", "Masterclasses", "Total Price"
        ])
        layout.addWidget(self.table)

        # Buttons
        self.refresh_btn = QPushButton("Refresh Bookings")
        self.refresh_btn.clicked.connect(self.load_bookings)
        layout.addWidget(self.refresh_btn)

        self.delete_btn = QPushButton("Delete Selected Booking")
        self.delete_btn.clicked.connect(self.delete_booking)
        layout.addWidget(self.delete_btn)

        self.add_program_btn = QPushButton("Add Program")
        self.add_program_btn.clicked.connect(self.add_program)
        layout.addWidget(self.add_program_btn)

        self.add_addon_btn = QPushButton("Add Add-on")
        self.add_addon_btn.clicked.connect(self.add_addon)
        layout.addWidget(self.add_addon_btn)

        self.add_masterclass_btn = QPushButton("Add Masterclass")
        self.add_masterclass_btn.clicked.connect(self.add_masterclass)
        layout.addWidget(self.add_masterclass_btn)

        self.delete_program_btn = QPushButton("Delete Program")
        self.delete_program_btn.clicked.connect(self.delete_program)
        layout.addWidget(self.delete_program_btn)

        self.delete_addon_btn = QPushButton("Delete Add-on")
        self.delete_addon_btn.clicked.connect(self.delete_addon)
        layout.addWidget(self.delete_addon_btn)

        self.delete_masterclass_btn = QPushButton("Delete Masterclass")
        self.delete_masterclass_btn.clicked.connect(self.delete_masterclass)
        layout.addWidget(self.delete_masterclass_btn)

        self.setLayout(layout)
        # Убрано self.load_bookings()

    def set_token(self, token):
        self.token = token
        self.load_bookings()  # Вызываем только после установки токена

    def load_bookings(self):
        try:
            print(f"Token used for request: {self.token}")  # Отладка
            headers = {"Authorization": f"Bearer {self.token}"}
            print(f"Sending request to http://localhost:8000/bookings/ with headers: {headers}")  # Отладка
            response = requests.get("http://localhost:8000/bookings/", headers=headers)
            print(f"Response status: {response.status_code}, Response text: {response.text}")  # Отладка
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
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load bookings: {str(e)}")

    def delete_booking(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a booking to delete")
            return
        booking_id = int(self.table.item(selected, 0).text())
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.delete(f"http://localhost:8000/bookings/{booking_id}", headers=headers)
            response.raise_for_status()
            self.load_bookings()
            QMessageBox.information(self, "Success", "Booking deleted")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete booking: {str(e)}")

    def add_program(self):
        name, ok = QInputDialog.getText(self, "Add Program", "Program Name:")
        if not ok or not name:
            return
        price, ok = QInputDialog.getInt(self, "Add Program", "Price (RUB):", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post("http://localhost:8000/programs/", json={"name": name, "price": price}, headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Program added")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add program: {str(e)}")

    def add_addon(self):
        name, ok = QInputDialog.getText(self, "Add Add-on", "Add-on Name:")
        if not ok or not name:
            return
        price, ok = QInputDialog.getInt(self, "Add Add-on", "Price (RUB):", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post("http://localhost:8000/addons/", json={"name": name, "price": price}, headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Add-on added")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add add-on: {str(e)}")

    def add_masterclass(self):
        name, ok = QInputDialog.getText(self, "Add Masterclass", "Masterclass Name:")
        if not ok or not name:
            return
        price, ok = QInputDialog.getInt(self, "Add Masterclass", "Price per Child (RUB):", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post("http://localhost:8000/masterclasses/", json={"name": name, "price_per_child": price}, headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Masterclass added")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add masterclass: {str(e)}")

    def delete_program(self):
        program_id, ok = QInputDialog.getInt(self, "Delete Program", "Program ID:", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.delete(f"http://localhost:8000/programs/{program_id}", headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Program deleted")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete program: {str(e)}")

    def delete_addon(self):
        addon_id, ok = QInputDialog.getInt(self, "Delete Add-on", "Add-on ID:", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.delete(f"http://localhost:8000/addons/{addon_id}", headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Add-on deleted")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete add-on: {str(e)}")

    def delete_masterclass(self):
        masterclass_id, ok = QInputDialog.getInt(self, "Delete Masterclass", "Masterclass ID:", 0, 0)
        if not ok:
            return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.delete(f"http://localhost:8000/masterclasses/{masterclass_id}", headers=headers)
            response.raise_for_status()
            QMessageBox.information(self, "Success", "Masterclass deleted")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete masterclass: {str(e)}")