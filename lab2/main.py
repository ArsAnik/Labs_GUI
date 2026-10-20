import os
import sys

import PyQt5
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtWidgets import QApplication, QFormLayout, QLineEdit, QMainWindow, QWidget

import cl1
import cl2


pyqt_dir = os.path.dirname(PyQt5.__file__)
os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", os.path.join(pyqt_dir, "Qt5", "plugins"))


class Currency:
    def __init__(self):
        self.rates = {"USD": 0.012, "RUB": 1.0, "EUR": 0.011}
        self.currency_names = list(self.rates)
        self.currency = {}

    def getCurrency(self):
        return self.currency.copy()

    def getCurrencyNames(self):
        return self.currency_names.copy()

    def convert(self, text, source):
        norm = str(text).strip().replace(",", ".")
        amount = float(norm)

        base_amount = amount / self.rates[source]
        self.currency = {
            code: base_amount * rate for code, rate in self.rates.items()
        }
        return self.currency.copy()


class CurrencyCalc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер валют")
        self.resize(400, 150)

        self.currency_data = Currency()
        self.fields = {}
        form = QFormLayout()

        for code in self.currency_data.getCurrencyNames():
            field = QLineEdit()
            field.setValidator(
                QRegularExpressionValidator(
                    QRegularExpression(r"[0-9]*[.,]?[0-9]*"), field
                )
            )
            field.textEdited.connect(
                lambda text, currency=code: self.input_handler.on_text_edited(currency, text)
            )
            self.fields[code] = field
            form.addRow(code, field)

        central = QWidget()
        central.setLayout(form)
        self.setCentralWidget(central)

        self.input_handler = cl1.CurrencyInput(self)
        self.calculator = cl2.CurrencyCalculator(self.currency_data, self)
        self.input_handler.conversionRequested.connect(self.calculator.convert)
        self.calculator.conversionReady.connect(self.update_fields)

    def update_fields(self, source, values):
        for code, value in values.items():
            if code != source:
                self.fields[code].setText(f"{value:.2f}".rstrip("0").rstrip("."))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyCalc()
    window.show()
    sys.exit(app.exec_())