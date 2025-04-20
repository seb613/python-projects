from PIL import Image


class Recognition():
    def __init__(self):
        self.type = "algorytm"

    def recognize(self, img: Image.Image) -> str:
        # Perform recognition
        self.image = img
        return "Recognized text"
    
    