from .recognition import Recognition
import easyocr
import numpy as np


class EasyOCR(Recognition):
    def __init__(self):
        self.type = "EasyOSR"
        self.reader = easyocr.Reader(['pl', 'en'], gpu=True)
        
    def recognize(self, img):
        image = np.array(img)
        results = self.reader.readtext(image)

        print("Wykryty tekst:")
        result = []
        for (bbox, text, prob) in results:
            result.append(TextProbability(text, prob))
        return find_max_probability(result)
    


class TextProbability:
    def __init__(self, text: str, prob: float):
        self.text = text
        self.prob = prob

def find_max_probability(results):
    if not results:
        return None

    max_prob_object = max(results, key=lambda x: x.prob)
    return max_prob_object.text
