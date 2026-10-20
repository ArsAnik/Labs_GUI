from PyQt5.QtCore import QObject, pyqtSignal


class CurrencyCalculator(QObject):
    conversionReady = pyqtSignal(str, dict)

    def __init__(self, currency, parent=None):
        super().__init__(parent)
        self.currency = currency

    def convert(self, source_currency, text):
        values = self.currency.convert(text, source_currency)
        if values is not None:
            self.conversionReady.emit(source_currency, values)