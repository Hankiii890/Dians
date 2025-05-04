import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QCheckBox, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate

class BookingForm(QWidget):
    def __init__(self):
        super().__init__()
        self.token = None  # Store the token
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        # Event Type
        self.event_type = QComboBox()
        self.event_type.addItems(["Birthday", "Masterclass"])
        layout.addWidget(QLabel("Select Event:"))
        layout.addWidget(self.event_type)

        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumDate(QDate.currentDate())
        layout.addWidget(QLabel("Select Date:"))
        layout.addWidget(self.date_edit)

        # Guest Count
        self.guest_count = QLineEdit()
        self.guest_count.setPlaceholderText("Number of guests")
        layout.addWidget(QLabel("Number of Guests:"))
        layout.addWidget(self.guest_count)

        # Phone
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone number")
        layout.addWidget(QLabel("Phone Number:"))
        layout.addWidget(self.phone)

        # Child Name
        self.child_name = QLineEdit()
        self.child_name.setPlaceholderText("Child's name")
        layout.addWidget(QLabel("Child's Name:"))
        layout.addWidget(self.child_name)

        # Program
        self.program = QComboBox()
        layout.addWidget(QLabel("Select Program:"))
        layout.addWidget(self.program)

        # Add-ons
        self.addon_checkboxes = []
        layout.addWidget(QLabel("Select Add-ons:"))
        self.addon_layout = QVBoxLayout()
        layout.addLayout(self.addon_layout)

        # Masterclasses
        self.masterclass_checkboxes = []
        layout.addWidget(QLabel("Select Masterclasses:"))
        self.masterclass_layout = QVBoxLayout()
        layout.addLayout(self.masterclass_layout)

        # Submit Button
        self.submit_btn = QPushButton("Submit Booking")
        self.submit_btn.clicked.connect(self.submit_booking)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)

    def load_data(self):
        try:
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            # Load programs
            response = requests.get("http://localhost:8000/programs/", headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            programs = response.json()
            if not isinstance(programs, list):
                raise ValueError("Programs data is not a list")
            self.program.clear()
            self.program.addItems([f"{p['name']} ({p['price']} RUB)" for p in programs])
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
                checkbox = QCheckBox(f"{addon['name']} ({addon['price']} RUB)")
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
                checkbox = QCheckBox(f"{mc['name']} ({mc['price_per_child']} RUB/child)")
                checkbox.setProperty("masterclass_id", mc["id"])
                self.masterclass_layout.addWidget(checkbox)
                self.masterclass_checkboxes.append(checkbox)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
            self.program.setProperty("programs", [])  # Set an empty list to avoid NoneType errors

    def submit_booking(self):
        try:
            guest_count = int(self.guest_count.text())
            if guest_count <= 0:
                raise ValueError("Guest count must be positive")
            phone = self.phone.text().strip()
            if not phone:
                raise ValueError("Phone number is required")
            child_name = self.child_name.text().strip()
            if not child_name:
                raise ValueError("Child's name is required")

            program_idx = self.program.currentIndex()
            programs = self.program.property("programs")
            if not programs or program_idx < 0 or program_idx >= len(programs):
                raise ValueError("No valid program selected")
            program_id = programs[program_idx]["id"]

            addon_ids = [cb.property("addon_id") for cb in self.addon_checkboxes if cb.isChecked()]
            masterclass_ids = [cb.property("masterclass_id") for cb in self.masterclass_checkboxes if cb.isChecked()]

            booking_data = {
                "date": self.date_edit.date().toString("yyyy-MM-dd"),
                "event_type": self.event_type.currentText(),
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
            QMessageBox.information(self, "Success",
                f"Booking created! Total: {result['total_price']} RUB\n"
                "Payment due at the end of the event.\n"
                "An administrator will call to confirm.")
            self.clear_form()
        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to submit booking: {str(e)}")

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