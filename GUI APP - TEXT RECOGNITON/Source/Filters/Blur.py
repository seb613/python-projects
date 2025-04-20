from ..Filter import Filter
from PIL import ImageFilter
from PIL.Image import Image

class Blur(Filter):
    def __init__(self, image: Image):
        super().__init__(image)     
        self.name = "Blur"
        self.strength: int = 50
        self.settings_view.add_slider('siła', 0,100,self.strength, self.update_str)
        super().execute(image)
        
    def update_str(self, value: int):
        self.strength = value
        self.filter()
        self.settings_view.update_preview()

    def filter(self):
        self.image = self.previous_image.filter(ImageFilter.GaussianBlur(radius= self.strength/10))