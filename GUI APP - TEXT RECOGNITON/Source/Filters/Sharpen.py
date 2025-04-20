from ..Filter import Filter
from PIL import ImageFilter
from PIL.Image import Image
from PIL import ImageEnhance

class Sharpen(Filter):
    def __init__(self, image: Image):
        super().__init__(image)
        self.name = "Sharpen"
        super().execute(image)

    def filter(self):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(2.0)  