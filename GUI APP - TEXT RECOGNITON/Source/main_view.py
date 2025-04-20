from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtGui import QPixmap
from Source.mainwindow import Ui_MainWindow
from typing import Any
from PIL.ImageQt import ImageQt
from PIL.Image import Image
from typing import Optional


class UpdateThread(QtCore.QThread):
    update_signal = QtCore.pyqtSignal(QPixmap)

    def __init__(self, image: Image):
        super().__init__()
        self.image = image

    def run(self):
        """Perform the task."""
        try:
            if self.image:
                # Create the pixmap from the image
                imgqt = ImageQt(self.image)

                # Reduce the size of the image
                imgqt: ImageQt = imgqt.scaled(  # type: ignore
                    640, 640, QtCore.Qt.AspectRatioMode.KeepAspectRatio
                )  # type: ignore

                pixmap = QPixmap.fromImage(imgqt)  # type: ignore

                # Emit the signal with the pixmap
                self.update_signal.emit(pixmap)
        except Exception as e:
            print(f"Error in UpdateThread: {e}")


class View:
    def __init__(self, window: Ui_MainWindow):
        self.ui = window
        self.main_window: QtWidgets.QMainWindow = QtWidgets.QMainWindow()
        self.ui.setupUi(self.main_window)  # type: ignore
        self.main_window.setWindowTitle("Rozpoznawanie tekstu - projekt")

        # change text on buttons
        self.ui.filter_button.setText("Dodaj filtr")
        self.ui.file_button.setText("Otwórz plik")
        self.ui.results.setText("Wykonaj")

        # Attach signal for export button
        self.ui.export_button.clicked.connect(self.export_text_clicked)

        # Thread for updating the image preview
        self.update_thread: Optional[UpdateThread] = None

        # Image preview setup
        self.scene: QtWidgets.QGraphicsScene = QtWidgets.QGraphicsScene()
        self.ui.preview.setScene(self.scene)
        self.ui.preview.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.ui.preview.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        self.pixmap_item = self.scene.addPixmap(QPixmap())

        # Make scrollbars always invisible
        self.ui.preview.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.ui.preview.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.ui.preview.resizeEvent = self.on_resize  # type: ignore
        self._resize_timer = QtCore.QTimer()
        self._resize_timer.setSingleShot(True)
        self._resize_timer.timeout.connect(self.update_preview_size)

        # righ click menu on preview
        self.context_menu = QtWidgets.QMenu()
        self.context_menu.addAction("Open", self.open_image)
        self.ui.preview.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.ui.preview.customContextMenuRequested.connect(
            self.show_preview_context_menu
        )

        # right click menu on filter list
        self.filter_context_menu = QtWidgets.QMenu()
        self.filter_context_menu.addAction("Edit", self.edit_filter)
        self.filter_context_menu.addAction("Delete", self.delete_filter)
        self.ui.filter_list.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.ui.filter_list.customContextMenuRequested.connect(
            self.show_filter_context_menu
        )

        # attach signals
        self.ui.filter_button.clicked.connect(self.add_filter_clicked)
        self.ui.file_button.clicked.connect(self.open_file_clicked)
        self.ui.results.clicked.connect(self.show_results_clicked)
        self.ui.filter_list.itemClicked.connect(self.filter_list_item_clicked)
        self.ui.results_list.itemClicked.connect(self.results_list_item_clicked)
        
        self.ui.segmentation_combo.currentIndexChanged.connect(self.segmentation_combobox_changed)
        self.ui.recognition_combo.currentIndexChanged.connect(self.recognition_combobox_changed)

    def show(self):
        """Show the main window."""
        self.main_window.show()

    def attach_controller(self, controller: Any):
        """Attach a controller to the view."""
        from Source.main_controller import Controller

        self.controller: Controller = controller

    def open_file_dialog(self) -> str:
        """Open a file dialog and return the selected file path."""
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        file_dialog.setViewMode(QtWidgets.QFileDialog.ViewMode.Detail)
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptMode.AcceptOpen)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            return file_path
        return ""

    """
    Preview handling
    
    """

    def show_preview_context_menu(self, pos: QtCore.QPoint):
        """Show context menu on right-click."""
        self.context_menu.exec(self.ui.preview.mapToGlobal(pos))

    def perform_preview_update(self, image: Image):
        """Start the thread to update the preview."""
        if self.update_thread is None or not self.update_thread.isRunning():
            # Create the thread only once and only start it if it's not already running
            self.update_thread = UpdateThread(image)
            self.update_thread.update_signal.connect(self.update_image_preview)

            # Start the thread
            self.update_thread.start()

    def open_image(self):
        print("Open image clicked")
        self.controller.display_full_image()

    def update_image_preview(self, pixmap: QPixmap):
        try:
            print("Updating image preview")
            self.pixmap_item.setPixmap(pixmap)
            self.ui.preview.fitInView(
                self.pixmap_item, QtCore.Qt.AspectRatioMode.KeepAspectRatio
            )

        except Exception as e:
            print(f"Error in update_image_preview: {e}")

    def update_preview_size(self):
        self.ui.preview.fitInView(
            self.pixmap_item, QtCore.Qt.AspectRatioMode.KeepAspectRatio
        )

    def add_filter_clicked(self):
        self.controller.add_filter_clicked()

    def open_file_clicked(self):
        print("Open file clicked")
        path = self.open_file_dialog()
        if path:
            self.controller.load_file(path)

    """
    Filter handling
    
    """

    def show_filter_context_menu(self, pos: QtCore.QPoint):
        # Map the position to the item under the cursor
        item = self.ui.filter_list.itemAt(pos)

        if item:
            # Show context menu only if an item is under the cursor
            self.filter_context_menu.exec(self.ui.filter_list.mapToGlobal(pos))

    def edit_filter(self):
        print("Edit filter clicked")
        index = self.ui.filter_list.currentRow()
        self.controller.adjust_filter_settings(index)

    def delete_filter(self):
        print("Delete filter clicked")

    def populate_filter_results_list(self, filters: list[str]):
        self.ui.filter_list.clear()
        for filter_name in filters:
            self.ui.filter_list.addItem(filter_name)

    def filter_list_item_clicked(self, item: QtWidgets.QListWidgetItem):
        print("Filter list item clicked")
        index = self.ui.filter_list.row(item)
        self.controller.filter_list_item_clicked(item.text(), index)

    """
    Segmentation handling
    
    """

    def populate_segmentation_combobox(self, segmentation_types: list[str]):
        self.ui.segmentation_combo.clear()  # type: ignore
        for segmentation_type in segmentation_types:
            self.ui.segmentation_combo.addItem(segmentation_type)  # type: ignore

    def segmentation_combobox_changed(self):
        # get text from combobox
        algorithm = self.ui.segmentation_combo.currentText()
        self.controller.segmentation_combobox_changed(algorithm)  # type: ignore

    """
    Recoginition handling
    
    """

    def show_results_clicked(self):
        self.controller.show_results_clicked()

    def populate_results_list(self, recognitions: list[str]):
        self.ui.results_list.clear()
        for recognition_name in recognitions:
            self.ui.results_list.addItem(recognition_name)

    def populate_recognition_combobox(self, recognition_types: list[str]):
        self.ui.recognition_combo.clear()  # type: ignore
        for recognition_type in recognition_types:
            self.ui.recognition_combo.addItem(recognition_type)  # type: ignore

    def results_list_item_clicked(self, item: QtWidgets.QListWidgetItem):
        print("Results list item clicked")
        index = self.ui.results_list.row(item)
        self.controller.results_list_item_clicked(item.text(), index)

    def update_result_text_preview(self, text: str):
        self.ui.text_preview.setText(text)

    def recognition_combobox_changed(self):
        # get text from combobox
        algorithm = self.ui.recognition_combo.currentText()
        self.controller.recognition_combobox_changed(algorithm)  # type: ignore

    """
    Resize event handling
    """

    def on_resize(self, event: QtGui.QResizeEvent):
        print("Resize event detected, starting debounce timer.")
        self._resize_timer.start(100)  # Wait 100ms before resizing
        self.main_window.resizeEvent(event)  # Call the original resize evet

    def export_text_clicked(self):
        """Handle export text button click."""
        text = self.ui.text_preview.toPlainText()
        if text:
            file_dialog = QtWidgets.QFileDialog()
            file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setNameFilter("Text Files (*.txt)")
            if file_dialog.exec():
                file_path = file_dialog.selectedFiles()[0]
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text)
            print("Text exported to file")
