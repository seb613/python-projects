from ..Filter import Filter
from PIL import ImageFilter
from PIL.Image import Image

class UnsharpMask(Filter):
    def __init__(self, image: Image):
        super().__init__(image)
        self.name = "UnsharpMask"
        super().execute(image)

    def filter(self):
        self.image = self.image.filter(ImageFilter.UnsharpMask)