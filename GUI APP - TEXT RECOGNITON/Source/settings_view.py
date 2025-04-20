from PyQt6 import QtWidgets, QtCore
from typing import Any, Callable
from PyQt6.QtGui import QPixmap
from PIL import ImageQt


class SettingsView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.filter: Any

        self.setWindowTitle("Ustawienia filtra")
        self.setGeometry(100, 100, 800, 600)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.preview = QtWidgets.QLabel()
        # add max size but keep aspect ratio
        self.preview.setScaledContents(True)
        self.preview.setMaximumSize(720, 480)

        self.main_layout.addWidget(self.preview)

        # add ok button
        self.ok_button = QtWidgets.QPushButton("OK")
        # postiion the button
        self.main_layout.addWidget(self.ok_button)

        # connect the button to the function
        self.ok_button.clicked.connect(self.ok_button_clicked)

    def attach_filter(self, filter: Any):
        self.filter = filter

    def ok_button_clicked(self):
        self.filter.update_settings()
        self.hide()

    def update_preview(self):
        # scale image to fit the preview
        imgqt = ImageQt.ImageQt(self.filter.image)

        imgqt = imgqt.scaled(  # type: ignore
            1920, 1080, QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )  # type: ignore
        pixmap = QPixmap.fromImage(imgqt)  # type: ignore
        self.preview.setPixmap(pixmap)  # type: ignore

    def add_slider(
        self,
        name: str,
        min_value: int,
        max_value: int,
        default_value: int,
        callback: Callable[[int], None],
    ):
        label = QtWidgets.QLabel(name)
        label.setText(name)
        self.main_layout.addWidget(label)
        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(default_value)
        slider.setTickInterval(1)
        slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.main_layout.addWidget(slider)
        slider.valueChanged.connect(callback)
