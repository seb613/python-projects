from icecream import ic
from PIL import Image

from Source.Filter import Filter
from typing import Any

from .segmentation import Segmentation
from .recognition.recognition import Recognition

import threading


class File:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.image: Image.Image


class Result:
    def __init__(self, image: Image.Image):
        self.name: str = "segment"
        self.image: Image.Image = image
        self.text: str = ""


class Model:
    def __init__(self):
        self.__file: File = File(name="None", path="None")
        # Create a white image to prevent errors
        self.__file.image = Image.new("RGB", (1, 1), "white")  # type: ignore
        self.controller: Any

        self.recognition_algorithm: Recognition 
        self.segmentation_algorithm: Segmentation

        self.filter_items: list[Filter] = []
        self.results_items: list[Result] = []

    def attach_controller(self, controller: Any):
        self.controller = controller

    @property
    def loaded_file(self) -> File:
        return self.__file

    @loaded_file.setter
    def loaded_file(self, path: str):
        filename = path.split("/")[-1]
        try:
            self.clean_workspace()
            self.__file = File(filename, path)
            self.__file.image = Image.open(path)  # type: ignore
            ic(f"Loaded file {filename}")
            self.add_filter("Input")

        except FileNotFoundError:
            ic(f"File {filename} not found")

    @loaded_file.deleter
    def loaded_files(self):
        self.clean_workspace()
        del self.__file

    def clean_workspace(self) -> None:
        self._clean_filters()
        self._clean_results()

    def _clean_filters(self) -> None:
        self.filter_items = []

    def _clean_results(self) -> None:
        self.results_items = []

    def show_original_image(self) -> None:
        """Show the original image in a separate window."""
        try:
            ic(f"Requested original image for {self.__file.name}")
            self.__file.image.show()
        except KeyError:
            ic("File not found")

    def _get_last_image(self) -> Image.Image:
        try:
            return self.filter_items[-1].image
        except IndexError:
            return self.__file.image

    def add_filter(self, filter_name: str) -> None:
        from .Filters import class_map as filter_map  # Deferred import

        try:
            ic(f"Adding filter {filter_name}")
            filter_class = filter_map[filter_name]

            self.filter_items.append(filter_class(self._get_last_image()))
        except KeyError:
            ic(f"Filter {filter_name} not found")

    def get_filters_results(self) -> list[str]:
        return [filter.name for filter in self.filter_items]

    def get_filter_preview(self, index: int) -> Image.Image:
        return self.filter_items[index].image

    def get_filter_types(self) -> list[str]:
        from .Filters import __all__ as filter_classes

        print(filter_classes)
        return filter_classes

    def adjust_filter_settings(self, filter_index: int) -> None:
        self.filter_items[filter_index].settings_view.show()

    ##OCR

    def perform_segmentation(self) -> None:
        print("Performing segmentation")
        results: list[Result] = []

        for result in self.segmentation_algorithm.segment(self._get_last_image()):
            results.append(Result(result))

        self.results_items = results

    def perform_recognition(self) -> None:
        print("Performing recognition")
            
        def recognize(result: Result) -> None:
            print(f"Recognizing {result.name}")
            result.text = self.recognition_algorithm.recognize(result.image)

        threads = []
        semaphore = threading.Semaphore(8)

        for result in self.results_items:
            semaphore.acquire()
            thread = threading.Thread(target=lambda r=result: (recognize(r), semaphore.release()))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
            
    def concatenate_results(self) -> None:
        print("Concatenating results")
        all_results = self.results_items[1:]
        image = self._get_last_image()
        results = ""
        for result in all_results:
            try:
                results = results + result.text + " "
            except Exception as e:
                print(e)
        print(results)
        result = Result(image)
        result.text = results
        result.name = "concatenated"
        
        self.results_items = [result] + self.results_items

    def get_results_names(self) -> list[str]:
        return [result.name for result in self.results_items]

    def get_result(self, index: int) -> Result:
        return self.results_items[index]

    ###
