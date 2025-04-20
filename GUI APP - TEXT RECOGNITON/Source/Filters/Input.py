from ..Filter import Filter
from PIL import ImageFilter
from PIL.Image import Image

class Input(Filter):
    def __init__(self, image: Image):
        super().__init__(image)
        self.name = 'Input'
        self.execute(image)