# type: ignore
from transformers import MgpstrProcessor, MgpstrForSceneTextRecognition
from .recognition import Recognition
from PIL import Image

class MGPSTR(Recognition):
    def __init__(self):
        self.type = "MGPSTR"

        self.processor = MgpstrProcessor.from_pretrained('alibaba-damo/mgp-str-base')
        self.model = MgpstrForSceneTextRecognition.from_pretrained('alibaba-damo/mgp-str-base')

    def recognize(self, img: Image.Image) -> str:
        # Perform recognition
        image = img.convert("RGB")
        pixel_values = self.processor(images = image, return_tensors="pt").pixel_values

        outputs = self.model(pixel_values)
        
        generated_text = self.processor.batch_decode(outputs.logits)['generated_text']
        print(generated_text)
        
        return str(generated_text)