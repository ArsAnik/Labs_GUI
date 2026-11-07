import os
import sys
from datetime import datetime

import PyQt5
from PyQt5.QtCore import QObject, QTimer, QRect
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickItem


class Interface(QObject):
    def __init__(self, engine, timer_value):
        super().__init__()
        self.engine = engine
        
        self.save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.timer = QTimer()
        self.timer.setInterval(timer_value)
        self.timer.timeout.connect(self.capture_and_save)
        self.timer.start()

    def capture_and_save(self):
        root_objects = self.engine.rootObjects()

        window = root_objects[0]

        canvas_item = None
        for child in window.findChildren(QQuickItem):
            if "Canvas" in child.metaObject().className():
                canvas_item = child

        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(window.winId())

        x = int(canvas_item.property("x"))
        y = int(canvas_item.property("y"))
        width = int(canvas_item.property("width"))
        height = int(canvas_item.property("height"))

        crop_rect = QRect(x, y, width, height)
        final_pixmap = pixmap.copy(crop_rect)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"canvas_{timestamp}.png"
        full_path = os.path.join(self.save_dir, filename)

        final_pixmap.save(full_path)


if __name__ == '__main__':
    pyqt_dir = os.path.dirname(PyQt5.__file__)
    os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", os.path.join(pyqt_dir, "Qt5", "plugins"))

    # Создаем экземпляр приложения
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    interface = Interface(engine, 10000)

    engine.rootContext().setContextProperty("_backend", interface)

    qml_path = os.path.join(pyqt_dir, "Qt5/qml")
    if os.path.exists(qml_path):
        engine.addImportPath(qml_path)

    # Загружаем QML
    engine.load("mainWindow.qml")

    # Проверка успешной загрузки QML
    if not engine.rootObjects():
        print("Ошибка: Не удалось загрузить QML файл!")
        sys.exit(-1)

    sys.exit(app.exec())