from ..Filter import Filter
from PIL import Image as Imagecls
from PIL.Image import Image
import numpy as np
import cv2

class Erode(Filter):
    def __init__(self, image: Image):
        super().__init__(image)
        self.name = "Erode"
        self.kernel = np.ones((5, 5), np.uint8)
        self.settings_view.add_slider('kernel', 0, 12, 5, self.update_kernel) # type: ignore
        self.execute(image)

    def update_kernel(self, value: int):
        self.kernel = np.ones((value, value), np.uint8)
        self.filter()
        self.settings_view.update_preview()

    def filter(self):
        image = np.array(self.previous_image)
        # Ensure the image is in uint8 format
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)
        # Apply erosion
        image = cv2.erode(image, self.kernel, iterations=1)
        self.image = Imagecls.fromarray(image)
