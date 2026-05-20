import sys
from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QSpinBox, QDateEdit,
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Учет клиентов в ателье")
        self.resize(1050, 520)

        title = QLabel("Автоматизированная система учета клиентов в ателье")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Поля ввода
        self.clientEdit = QLineEdit()
        self.clientEdit.setPlaceholderText("Например: Иванова Мария Сергеевна")

        self.phoneEdit = QLineEdit()
        self.phoneEdit.setPlaceholderText("+7-913-111-22-33")

        self.serviceCombo = QComboBox()
        self.serviceCombo.addItems([
            "Ушить платье",
            "Подшить брюки",
            "Пошив юбки",
            "Замена молнии",
            "Ремонт пиджака",
            "Индивидуальный пошив"
        ])

        self.dateEdit = QDateEdit()
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit.setCalendarPopup(True)

        self.deadlineEdit = QDateEdit()
        self.deadlineEdit.setDate(QDate.currentDate().addDays(3))
        self.deadlineEdit.setCalendarPopup(True)

        self.statusCombo = QComboBox()
        self.statusCombo.addItems(["Принят", "В работе", "Готов", "Выдан", "Отменен"])

        self.priceSpin = QSpinBox()
        self.priceSpin.setRange(0, 1000000)
        self.priceSpin.setSuffix(" руб.")
        self.priceSpin.setValue(1500)

        self.prepaymentSpin = QSpinBox()
        self.prepaymentSpin.setRange(0, 1000000)
        self.prepaymentSpin.setSuffix(" руб.")

        self.commentEdit = QLineEdit()
        self.commentEdit.setPlaceholderText("Комментарий к заказу")

        addButton = QPushButton("Добавить заказ")
        deleteButton = QPushButton("Удалить выбранный заказ")
        clearButton = QPushButton("Очистить поля")

        addButton.clicked.connect(self.add_record)
        deleteButton.clicked.connect(self.delete_record)
        clearButton.clicked.connect(self.clear_fields)

        # Таблица заказов
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels([
            "№", "Клиент", "Телефон", "Услуга", "Дата приема",
            "Дата готовности", "Статус", "Стоимость", "Предоплата"
        ])
        self.table.setColumnWidth(0, 45)
        self.table.setColumnWidth(1, 210)
        self.table.setColumnWidth(2, 140)
        self.table.setColumnWidth(3, 160)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 130)
        self.table.setColumnWidth(6, 100)
        self.table.setColumnWidth(7, 100)
        self.table.setColumnWidth(8, 100)

        # Макет формы
        formLayout = QGridLayout()
        formLayout.addWidget(QLabel("ФИО клиента:"), 0, 0)
        formLayout.addWidget(self.clientEdit, 0, 1)
        formLayout.addWidget(QLabel("Телефон:"), 0, 2)
        formLayout.addWidget(self.phoneEdit, 0, 3)

        formLayout.addWidget(QLabel("Услуга:"), 1, 0)
        formLayout.addWidget(self.serviceCombo, 1, 1)
        formLayout.addWidget(QLabel("Статус:"), 1, 2)
        formLayout.addWidget(self.statusCombo, 1, 3)

        formLayout.addWidget(QLabel("Дата приема:"), 2, 0)
        formLayout.addWidget(self.dateEdit, 2, 1)
        formLayout.addWidget(QLabel("Дата готовности:"), 2, 2)
        formLayout.addWidget(self.deadlineEdit, 2, 3)

        formLayout.addWidget(QLabel("Стоимость:"), 3, 0)
        formLayout.addWidget(self.priceSpin, 3, 1)
        formLayout.addWidget(QLabel("Предоплата:"), 3, 2)
        formLayout.addWidget(self.prepaymentSpin, 3, 3)

        formLayout.addWidget(QLabel("Комментарий:"), 4, 0)
        formLayout.addWidget(self.commentEdit, 4, 1, 1, 3)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(deleteButton)
        buttonLayout.addWidget(clearButton)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(title)
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.table)

    def add_record(self):
        client = self.clientEdit.text().strip()
        phone = self.phoneEdit.text().strip()

        if not client:
            QMessageBox.warning(self, "Ошибка ввода", "Введите ФИО клиента.")
            return

        if not phone:
            QMessageBox.warning(self, "Ошибка ввода", "Введите телефон клиента.")
            return

        row = self.table.rowCount()
        self.table.insertRow(row)

        values = [
            str(row + 1),
            client,
            phone,
            self.serviceCombo.currentText(),
            self.dateEdit.date().toString("dd.MM.yyyy"),
            self.deadlineEdit.date().toString("dd.MM.yyyy"),
            self.statusCombo.currentText(),
            str(self.priceSpin.value()),
            str(self.prepaymentSpin.value())
        ]

        for column, value in enumerate(values):
            self.table.setItem(row, column, QTableWidgetItem(value))

        self.clear_fields()

    def delete_record(self):
        selected_row = self.table.currentRow()

        if selected_row < 0:
            QMessageBox.information(self, "Удаление", "Выберите заказ для удаления.")
            return

        self.table.removeRow(selected_row)

        # Перенумерация заказов после удаления
        for row in range(self.table.rowCount()):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))

    def clear_fields(self):
        self.clientEdit.clear()
        self.phoneEdit.clear()
        self.commentEdit.clear()
        self.serviceCombo.setCurrentIndex(0)
        self.statusCombo.setCurrentIndex(0)
        self.dateEdit.setDate(QDate.currentDate())
        self.deadlineEdit.setDate(QDate.currentDate().addDays(3))
        self.priceSpin.setValue(1500)
        self.prepaymentSpin.setValue(0)
        self.clientEdit.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
