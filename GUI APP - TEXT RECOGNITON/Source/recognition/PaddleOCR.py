from paddleocr import PaddleOCR
from .recognition import Recognition
from PIL import Image
from PIL import ImageOps
import numpy as np
from PIL import Image

class PaddleOCRRecognition_CRNN(Recognition):
    def __init__(self):
        super().__init__()
        self.type = "PaddleOCR"
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', rec_model_dir='./models/rec/crnn', det=False)

    def recognize(self, img: Image.Image) -> str:
        # add white border to the image
        border_size = 20  # Width of the border in pixels
        img = ImageOps.expand(img, border=border_size, fill='white')  # Add white padding

        
        image = np.array(img)
        #scale up the image
        
        result = self.ocr.ocr(image, cls=True)
        
        print("Wynik rozpoznawania:", result)

        if result is None or len(result) == 0 or result[0] is None:
            return "Brak wykrytego tekstu"  
        
        recognized_text = ""
        for segment in result:  
            for line in segment:
                text = line[1][0]
                recognized_text += text + "\n"

        if not recognized_text:
            return "Brak rozpoznanego tekstu w obrazie"
        
        return recognized_text.strip()

class PaddleOCRRecognition_SAR(Recognition):
    def __init__(self):
        super().__init__()
        self.type = "PaddleOCR"
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', rec_model_dir='./models/rec/rec_sar_resnet31')

    def recognize(self, img: Image.Image) -> str:
        # add white border to the image
        border_size = 20  # Width of the border in pixels
        img = ImageOps.expand(img, border=border_size, fill='white')  # Add white padding

        
        image = np.array(img)
        #scale up the image
        
        result = self.ocr.ocr(image, cls=True)
        
        print("Wynik rozpoznawania:", result)

        if result is None or len(result) == 0 or result[0] is None:
            return "Brak wykrytego tekstu"  
        
        recognized_text = ""
        for segment in result:  
            for line in segment:
                text = line[1][0]
                recognized_text += text + "\n"

        if not recognized_text:
            return "Brak rozpoznanego tekstu w obrazie"
        
        return recognized_text.strip()
    
class PaddleOCRRecognition_NRTR(Recognition):
    def __init__(self):
        super().__init__()
        self.type = "PaddleOCR"
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', rec_model_dir='./models/rec/rec_nrtr')

    def recognize(self, img: Image.Image) -> str:
        # add white border to the image
        border_size = 20  # Width of the border in pixels
        img = ImageOps.expand(img, border=border_size, fill='white')  # Add white padding

        
        image = np.array(img)
        #scale up the image
        
        result = self.ocr.ocr(image, cls=True)
        
        print("Wynik rozpoznawania:", result)

        if result is None or len(result) == 0 or result[0] is None:
            return "Brak wykrytego tekstu"  
        
        recognized_text = ""
        for segment in result:  
            for line in segment:
                text = line[1][0]
                recognized_text += text + "\n"

        if not recognized_text:
            return "Brak rozpoznanego tekstu w obrazie"
        
        return recognized_text.strip()
    
    
class PaddleOCRRecognition_QANET(Recognition):
    def __init__(self):
        super().__init__()
        self.type = "PaddleOCR"
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', rec_model_dir='./models/rec/rec_qanet')

    def recognize(self, img: Image.Image) -> str:
        # add white border to the image
        border_size = 20  # Width of the border in pixels
        img = ImageOps.expand(img, border=border_size, fill='white')  # Add white padding

        
        image = np.array(img)
        #scale up the image
        
        result = self.ocr.ocr(image, cls=True)
        
        print("Wynik rozpoznawania:", result)

        if result is None or len(result) == 0 or result[0] is None:
            return "Brak wykrytego tekstu"  
        
        recognized_text = ""
        for segment in result:  
            for line in segment:
                text = line[1][0]
                recognized_text += text + "\n"

        if not recognized_text:
            return "Brak rozpoznanego tekstu w obrazie"
        
        return recognized_text