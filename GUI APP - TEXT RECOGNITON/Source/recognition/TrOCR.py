# type: ignore
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from .recognition import Recognition
from PIL import Image

class TrOCR_handwritten(Recognition):
    def __init__(self):
        self.type = "TrOCR"

        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

    def recognize(self, img: Image.Image) -> str:
        # Perform recognition
        pixel_values = self.processor(img, return_tensors="pt").pixel_values

        generated_ids = self.model.generate(pixel_values)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return generated_text
        
        
class TrOCR_printed(Recognition):
    def __init__(self):
        self.type = "TrOCR"

        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")

    def recognize(self, img: Image.Image) -> str:
        # Perform recognition
        pixel_values = self.processor(img, return_tensors="pt").pixel_values

        generated_ids = self.model.generate(pixel_values)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return generated_text

