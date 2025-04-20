from PyQt6 import QtWidgets
from typing import Any

class FiltersView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dodaj filtr")
        self.setGeometry(100, 100, 800, 600)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.filter_list = QtWidgets.QListWidget()
        self.filter_list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.main_layout.addWidget(self.filter_list)

        self.filter_button = QtWidgets.QPushButton("Dodaj filtr")
        self.main_layout.addWidget(self.filter_button)

        self.filter_button.clicked.connect(self.add_filter)
        
    def attach_controller(self, controller: Any):
        self.controller = controller
        
    def add_filter(self):
        #check if only 1 item is selected
        if len(self.filter_list.selectedItems()) == 1:
            self.controller.filter_added(self.filter_list.currentItem().text())
        else:
            QtWidgets.QMessageBox.warning(self, "Błąd", "Wybierz dokładnie jeden filtr")
            
            
        
    def populate_filters_list(self, filters: list[str]):
        self.filter_list.clear()
        self.filter_list.addItems(filters)