from ..Filter import Filter
from PIL import ImageFilter
from PIL.Image import Image

class Sepia(Filter):
    def __init__(self, image: Image):
        super().__init__(image)
        self.name = "Sepia"
        super().execute(image)

    def filter(self):
        self.image = self.image.convert("RGB")
        width, height = self.image.size
        pixels = self.image.load()  # create the pixel map

        for py in range(height):
            for px in range(width):
                r, g, b = self.image.getpixel((px, py))

                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                if tr > 255:
                    tr = 255

                if tg > 255:
                    tg = 255

                if tb > 255:
                    tb = 255

                pixels[px, py] = (tr, tg, tb)