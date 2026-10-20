from PyQt5.QtCore import QObject, pyqtSignal


class CurrencyInput(QObject):
    conversionRequested = pyqtSignal(str, str)

    def on_text_edited(self, currency, text):
        if not text.strip():
            return
        self.conversionRequested.emit(currency, text)
