import sys
from PyQt6.QtWidgets import QApplication
from Source.main_controller import Controller


def load_stylesheet(file_path: str) -> str:
    """Load a stylesheet from a file."""
    with open(file_path, "r") as file:
        return file.read()

class App(QApplication):
    def __init__(self):
        super(App, self).__init__([])
        self.setStyle("Fusion") # Set the style to Fusion
        self.stylesheet: object = load_stylesheet("Style/stylesheet.qss")
        self.setStyleSheet(self.stylesheet)
        self.controller: Controller = Controller()
        self.controller.view.show()

    

if __name__ == '__main__':
    app: QApplication = App()
    sys.exit(app.exec()) 