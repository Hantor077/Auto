from abc import ABC, abstractmethod
from datetime import datetime
from getpass import getuser

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from settings import AppConfig


class Transport(ABC):
    @abstractmethod
    def describe(self):
        pass


class Car(Transport):
    def __init__(self, brand, model, year, price):
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price

    @property
    def brand(self):
        return self.__brand

    @brand.setter
    def brand(self, value):
        self.__brand = value.strip()

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value.strip()

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = int(value)

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = int(value)

    def describe(self):
        return f"{self.brand} {self.model} — {self.year} год, {self.price} руб."

    def __str__(self):
        return self.describe()

    def __eq__(self, other):
        if not isinstance(other, Car):
            return NotImplemented

        return (
            self.brand == other.brand
            and self.model == other.model
            and self.year == other.year
        )

    def __lt__(self, other):
        if not isinstance(other, Car):
            return NotImplemented

        return self.price < other.price


class Garage:
    def __init__(self):
        self.__cars = []

    def add_car(self, car):
        self.__cars.append(car)

    def get_car(self, index):
        return self.__cars[index]

    def __iter__(self):
        return iter(self.__cars)

    def __len__(self):
        return len(self.__cars)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(AppConfig.WINDOW_TITLE)
        self.resize(AppConfig.WINDOW_WIDTH, AppConfig.WINDOW_HEIGHT)

        self.login = getuser()
        self.time_in = datetime.now()

        self.garage = Garage()

        start_cars = [
            Car("Toyota", "Camry", 2020, 2500000),
            Car("Lada", "Vesta", 2022, 1300000),
            Car("Kia", "Rio", 2019, 1500000),
            Car("Hyundai", "Solaris", 2021, 1700000),
            Car("Volkswagen", "Polo", 2018, 1200000),
            Car("Renault", "Logan", 2017, 900000),
            Car("Skoda", "Octavia", 2020, 2100000),
            Car("Nissan", "Qashqai", 2019, 2200000),
            Car("Ford", "Focus", 2016, 850000),
            Car("Mazda", "CX-5", 2021, 2800000),
        ]

        for car in start_cars:
            self.garage.add_car(car)

        title = QLabel("Мини-автосалон")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText("Например, Toyota")

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Например, Camry")

        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Например, 2020")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Например, 2500000")

        form_layout = QFormLayout()
        form_layout.addRow("Марка:", self.brand_input)
        form_layout.addRow("Модель:", self.model_input)
        form_layout.addRow("Год:", self.year_input)
        form_layout.addRow("Цена в рублях:", self.price_input)

        add_button = QPushButton("Добавить машину")
        add_button.clicked.connect(self.add_car)

        self.new_price_input = QLineEdit()
        self.new_price_input.setPlaceholderText("Введи новую цену")

        change_price_button = QPushButton("Изменить цену выбранной машины")
        change_price_button.clicked.connect(self.change_price)

        price_layout = QHBoxLayout()
        price_layout.addWidget(self.new_price_input)
        price_layout.addWidget(change_price_button)

        self.car_list = QListWidget()

        for car in self.garage:
            self.car_list.addItem(str(car))

        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(add_button)
        main_layout.addWidget(self.car_list)
        main_layout.addLayout(price_layout)
        main_layout.addWidget(self.info_label)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.update_info()

    def add_car(self):
        brand = self.brand_input.text().strip()
        model = self.model_input.text().strip()
        year_text = self.year_input.text().strip()
        price_text = self.price_input.text().strip()

        if not brand or not model or not year_text or not price_text:
            QMessageBox.warning(
                self,
                "Не хватает данных",
                "Заполни все четыре поля.",
            )
            return

        try:
            year = int(year_text)
            price = int(price_text)
        except ValueError:
            QMessageBox.warning(
                self,
                "Проверь данные",
                "Год и цена должны быть числами.",
            )
            return

        if year < 1886 or year > 2100:
            QMessageBox.warning(
                self,
                "Неверный год",
                "Введи год от 1886 до 2100.",
            )
            return

        if price <= 0:
            QMessageBox.warning(
                self,
                "Неверная цена",
                "Цена должна быть больше нуля.",
            )
            return

        car = Car(brand, model, year, price)
        self.garage.add_car(car)
        self.car_list.addItem(str(car))

        self.brand_input.clear()
        self.model_input.clear()
        self.year_input.clear()
        self.price_input.clear()

        self.update_info()

    def change_price(self):
        selected_row = self.car_list.currentRow()

        if selected_row == -1:
            QMessageBox.warning(
                self,
                "Машина не выбрана",
                "Сначала нажми на машину в списке.",
            )
            return

        price_text = self.new_price_input.text().strip()

        try:
            new_price = int(price_text)
        except ValueError:
            QMessageBox.warning(
                self,
                "Проверь цену",
                "Введи цену целым числом.",
            )
            return

        if new_price <= 0:
            QMessageBox.warning(
                self,
                "Неверная цена",
                "Цена должна быть больше нуля.",
            )
            return

        car = self.garage.get_car(selected_row)
        car.price = new_price

        self.car_list.item(selected_row).setText(str(car))
        self.new_price_input.clear()

    def update_info(self):
        self.info_label.setText(f"Машин в автосалоне: {len(self.garage)}")

    def closeEvent(self, event):
        time_out = datetime.now()

        try:
            file_is_empty = (
                not AppConfig.REPORT_PATH.exists()
                or AppConfig.REPORT_PATH.stat().st_size == 0
            )

            with AppConfig.REPORT_PATH.open("a", encoding="utf-8") as report:
                if file_is_empty:
                    report.write("login | time_in | time_out\n")

                report.write(
                    f"{self.login} | "
                    f"{self.time_in.strftime('%d.%m.%Y %H:%M:%S')} | "
                    f"{time_out.strftime('%d.%m.%Y %H:%M:%S')}\n"
                )

            event.accept()

        except OSError as error:
            QMessageBox.critical(
                self,
                "Не удалось сохранить отчёт",
                f"Программа не смогла записать report.txt.\n{error}",
            )
            event.ignore()

    def resizeEvent(self, event):
        self.update_info()
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.brand_input.clear()
            self.model_input.clear()
            self.year_input.clear()
            self.price_input.clear()
            self.new_price_input.clear()
            event.accept()
        else:
            super().keyPressEvent(event)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()