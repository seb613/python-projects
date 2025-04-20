from ..Filter import Filter
from PIL import ImageFilter
from PIL.Image import Image

class Emboss(Filter):
    def __init__(self, image: Image):
        super().__init__(image)
        self.name = "Emboss"
        super().execute(image)

    def filter(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)