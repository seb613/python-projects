from ..Filter import Filter
from PIL import ImageFilter
from PIL.Image import Image

class Detail(Filter):
    def __init__(self, image: Image):
        super().__init__(image)
        self.name = "Detail"
        super().execute(image)

    def filter(self):
        self.image = self.image.filter(ImageFilter.DETAIL)