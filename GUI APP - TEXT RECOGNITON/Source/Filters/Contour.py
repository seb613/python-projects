from ..Filter import Filter
from PIL import ImageFilter
from PIL.Image import Image

class Contour(Filter):
    def __init__(self, image: Image):
        super().__init__(image)
        self.name = "Contour"
        super().execute(image)

    def filter(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)