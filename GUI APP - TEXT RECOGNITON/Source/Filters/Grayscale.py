from ..Filter import Filter
from PIL import ImageFilter
from PIL.Image import Image


class Grayscale(Filter):
    def __init__(self, image: Image):
        super().__init__(image)
        self.name = "Grayscale"
        super().execute(image)

    def filter(self):
        self.image = self.image.convert("L")
        
# other filters to implement

class Invert(Filter):
    def __init__(self, image: Image):
        super().__init__(image)
        self.name = "Invert"
        super().execute(image)

    def filter(self):
        self.image = self.image.convert("RGB")
        self.image = self.image.point(lambda p: 255 - p) # type: ignore
        
    