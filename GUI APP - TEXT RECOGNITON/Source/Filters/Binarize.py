# type: ignore

from ..Filter import Filter
from PIL import ImageFilter, ImageOps
from PIL.Image import Image

class Binarize(Filter):
    def __init__(self, image: Image):
        super().__init__(image)     
        self.name = "Binarize"
        self.thresh: int = 50
        self.settings_view.add_slider('thresh', 0, 255, self.thresh, self.update_thresh)
        super().execute(image)
        
    def update_thresh(self, value: int):
        self.thresh = value
        self.filter()
        self.settings_view.update_preview()

    def filter(self):
        # Convert image to grayscale
        gray_image = self.previous_image.convert("L")
        # Apply binarization using the threshold
        self.image = gray_image.point(lambda p: 255 if int(p) > self.thresh else 0, '1')
