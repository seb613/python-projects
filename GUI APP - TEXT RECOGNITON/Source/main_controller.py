from Source.main_view import View
from .main_model import Model
from Source.mainwindow import Ui_MainWindow
from PIL.Image import Image
from .filters_view import FiltersView

from typing import Any
from .segmentation import (
    Segmentation,
    EAST_Segmentation,
    YOLO_Segmentation,
    MORPHOLOGY_CLUSTERING_Segmentation,
    CRAFT_Segmentation,
    SAST_SEGMENTATION_PADDLE,
    DB_SEGMENTATION_PADDLE,
    CTPN_SEGMENTATION_PADDLE,
    PSENET_SEGMENTATION_PADDLE,
)
from .recognition.recognition import Recognition
from .recognition.EasyOCR import EasyOCR
from .recognition.PaddleOCR import (
    PaddleOCRRecognition_CRNN,
    PaddleOCRRecognition_SAR,
    PaddleOCRRecognition_NRTR,
    PaddleOCRRecognition_QANET,
)
from .recognition.TrOCR import TrOCR_handwritten, TrOCR_printed
from .recognition.MGPSTR import MGPSTR


segmentation_algorithms_dict: dict[str, Any] = {
    "None": Segmentation,
    "EAST(text sceniczny)": EAST_Segmentation,
    "YOLO": YOLO_Segmentation,
    "MORPH": MORPHOLOGY_CLUSTERING_Segmentation,
    "CRAFT": CRAFT_Segmentation,
    "SAST Paddle": SAST_SEGMENTATION_PADDLE,
    "DB Paddle": DB_SEGMENTATION_PADDLE,
    "CTPN Paddle": CTPN_SEGMENTATION_PADDLE,
    "PSENET Paddle": PSENET_SEGMENTATION_PADDLE,
}
recognition_algorithms_dict: dict[str, Any] = {
    "None": Recognition,
    "EasyOCR": EasyOCR,
    "PaddleOCR_CRNN": PaddleOCRRecognition_CRNN,
    "PaddleOCR_SAR": PaddleOCRRecognition_SAR,
    "PaddleOCR_NRTR": PaddleOCRRecognition_NRTR,
    "PaddleOCR_QANET": PaddleOCRRecognition_QANET,
    "TrOCR handwritten": TrOCR_handwritten,
    "TrOCR printed": TrOCR_printed,
    "MGP-STR": MGPSTR,
}


class Controller:
    def __init__(self):
        self.model: Model = Model()
        self.view: View = View(Ui_MainWindow())
        self.filters_View: FiltersView = FiltersView()

        # attach the controller to the view
        self.view.attach_controller(self)
        self.filters_View.attach_controller(self)
        self.model.attach_controller(self)

        # run setup
        self.__setup()

        # preview image
        self.current_image: Image

    def __setup(self):
        self.view.populate_recognition_combobox(
            list(recognition_algorithms_dict.keys())
        )
        self.view.populate_segmentation_combobox(
            list(segmentation_algorithms_dict.keys())
        )
        self.filters_View.populate_filters_list(self.model.get_filter_types())

        self.model.segmentation_algorithm = Segmentation()  # default
        self.model.recognition_algorithm = Recognition()  # default

    def update_filters_list(self):
        self.filters_View.populate_filters_list(self.model.get_filters_results())

    def _update_filter_results_list(self):
        self.view.populate_filter_results_list(self.model.get_filters_results())

    def _update_results_list(self):
        self.view.populate_results_list(self.model.get_results_names())

    def update_image_preview(self):
        self.view.perform_preview_update(self.current_image)

    def load_file(self, path: str):
        try:
            self.model.loaded_file = path
            self.view.ui.file_label.setText(
                "Otwarty plik: " + self.model.loaded_file.name
            )  # type: ignore
            self.current_image = self.model.loaded_file.image
            self.update_image_preview()
            self._update_filter_results_list()
        except Exception as e:
            print(e)

    def display_full_image(self):
        self.current_image.show()

    def filter_list_item_clicked(self, item: str, index: int):
        print(f"Filter list item clicked: {item} with index {index}")
        self.current_image = self.model.get_filter_preview(index)  # type: ignore
        print(self.current_image)
        self.update_image_preview()

    def adjust_filter_settings(self, filter_index: int):
        self.model.adjust_filter_settings(filter_index)

    def results_list_item_clicked(self, item: str, index: int):
        print(f"Results list item clicked: {item} with index {index}")
        result = self.model.get_result(index)
        self.current_image = result.image
        self.update_image_preview()
        self.view.update_result_text_preview(result.text)

    def add_filter_clicked(self):
        self.filters_View.show()

    def filter_added(self, filter_name: str):
        self.filters_View.hide()
        self.model.add_filter(filter_name)
        self._update_filter_results_list()

    def show_results_clicked(self):
        print("Show results clicked")
        print(self.model.results_items)
        self.model.perform_segmentation()
        self.model.perform_recognition()
        self.model.concatenate_results()
        print(self.model.results_items)
        self._update_results_list()

    def segmentation_combobox_changed(self, algorithm: str):
        print(f"Segmentation combobox changed to {algorithm}")
        self.model.segmentation_algorithm = segmentation_algorithms_dict[algorithm]()

    def recognition_combobox_changed(self, algorithm: str):
        print(f"Recognition combobox changed to {algorithm}")
        self.model.recognition_algorithm = recognition_algorithms_dict[algorithm]()
