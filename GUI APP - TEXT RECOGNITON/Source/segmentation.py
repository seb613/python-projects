# type: ignore
from PIL.Image import Image
from PIL import Image as Image_cls
from PIL import ImageDraw
from typing import List
import cv2
import numpy as np
import torch
from Source.craft_text_detector import Craft
from paddleocr import PaddleOCR
from copy import deepcopy
    

class Segmentation():
    def __init__(self):
        self.type = "algorytm"

    def segment(self, img: Image) -> list[Image]:
        # Perform segmentation
        segmented_image: Image = img # Placeholder
        # segment
        segments: List[Image] = [segmented_image] # + all segments [orginal_image with BB overlaid + segments]
        return segments
    
class EAST_Segmentation(Segmentation):
    """EAST segmentation algorithm using OpenCV"""
    def __init__(self):
        self.type = "EAST"

    def segment(self, img: Image) -> list[Image]:
        # Convert PIL image to NumPy array
        image = np.array(img)
        
        # Convert RGB to BGR (OpenCV uses BGR by default)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        orig = image.copy()
        (H, W) = image.shape[:2]
        (newW, newH) = (1280, 1280) ###############################
        rW = W / float(newW)
        rH = H / float(newH)

        image = cv2.resize(image, (newW, newH))
        blob = cv2.dnn.blobFromImage(image, 1.0, (newW, newH), (123.68, 116.78, 103.94), swapRB=True, crop=False)

        return self.segment_with_blob(orig, blob, rW, rH)
    
    def segment_with_blob(self, orig, blob, rW, rH):
        # Update the path to the frozen_east_text_detection.pb file
        net = cv2.dnn.readNet('Source/frozen_east_text_detection.pb')

        net.setInput(blob)
        output_layers = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]
        (scores, geometry) = net.forward(output_layers)

        (rects, confidences) = self.decode_predictions(scores, geometry)
        boxes = cv2.dnn.NMSBoxes(rects, confidences, 0.5, 0.5)  ######################### PEWNOŚĆ

        # Handle the case where boxes might be empty
        if len(boxes) == 0:
            return [Image_cls.fromarray(cv2.cvtColor(orig, cv2.COLOR_BGR2RGB))]  # Return only the original image if no boxes

        # Flatten the numpy array returned by NMSBoxes
        boxes = boxes.flatten()

        segments: List[Image] = []

        # Loop over all detected boxes (blobs)
        for i in boxes:
            (startX, startY, endX, endY) = rects[i]
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)

            # Extract each blob (region of interest) as a separate image
            blob_image = orig[startY:endY, startX:endX]
            blob_pil = Image_cls.fromarray(cv2.cvtColor(blob_image, cv2.COLOR_BGR2RGB))
            segments.append(blob_pil)

            # Draw bounding box on the original image
            cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

        # Convert the result back to PIL image
        result_image = Image_cls.fromarray(cv2.cvtColor(orig, cv2.COLOR_BGR2RGB))
        segments.insert(0, result_image)  # Insert the original image with boxes as the first element

        return segments

    def decode_predictions(self, scores, geometry):
        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []

        for y in range(numRows):
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            for x in range(numCols):
                if scoresData[x] < 0.5:
                    continue

                offsetX = x * 4.0
                offsetY = y * 4.0
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])

        return (rects, confidences)


class MORPHOLOGY_CLUSTERING_Segmentation(Segmentation):
    """Refined segmentation algorithm for text detection."""
    def __init__(self):
        self.type = "KNN_CLUSTERING"
        self.image: Image_cls = Image_cls.new("RGB", (0, 0))

    def segment(self, img: Image_cls) -> List[Image_cls]:
        """
        Segments the input image to isolate text regions.
        Args:
            img (Image_cls): The input image in PIL format.

        Returns:
            List[Image_cls]: A list containing the original image and segmented parts.
        """
        # Convert the PIL image to a NumPy array for OpenCV processing
        original = np.array(img)
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        
        #automatic thresholding
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # Debug Step 1: Save thresholded image
        Image_cls.fromarray(thresh).show()
        
        # Perform morphological operations to clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned_mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # Debug Step 2: Save cleaned mask
        Image_cls.fromarray(cleaned_mask).show()
        
        # Find contours to extract text regions
        contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        segments = []
        h, w = original.shape[:2]  # Dimensions of the image

        # Iterate over contours and extract bounding boxes
        for contour in contours:
            x, y, w_box, h_box = cv2.boundingRect(contour)
            
            # Filter out invalid segments
            if w_box > 5 and h_box > 5:  # Exclude tiny contours
                # Extract the region of interest (ROI)
                segment = original[y:y+h_box, x:x+w_box]
                segments.append(Image_cls.fromarray(segment))
        
        # Overlay bounding boxes on the original image for visualization
        annotated_image = original.copy()
        for contour in contours:
            x, y, w_box, h_box = cv2.boundingRect(contour)
            if w_box > 5 and h_box > 5:  # Only valid segments
                cv2.rectangle(annotated_image, (x, y), (x+w_box, y+h_box), (0, 255, 0), 2)
        
        # Convert annotated original image back to PIL format
        annotated_image_pil = Image_cls.fromarray(annotated_image)
        
        # Return the list of images: [annotated image, each segment]
        return [annotated_image_pil] + segments
    
    

class YOLO_Segmentation(Segmentation):
    """YOLO segmentation algorithm"""
    def __init__(self):
        self.type = "YOLO"
        self.image: Image = Image_cls.new("RGB", (0, 0))
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # 'yolov5s', 'yolov5m', 'yolov5l', 'yolov5x'

        
    def segment(self, img: Image) -> list[Image]:
        # Perform segmentation
        results = self.model(img)
        
        print(results.pandas().xyxy[0]) 
        #convert to pil image
        print(results.render())
        results.show()
        results = results.render()
        
        #make it pil
        results = Image_cls.fromarray(results[0])
        
        
        # segment
        segments: List[Image] = [results]
        return segments
    
    
class CRAFT_Segmentation(Segmentation): 
    """CRAFT segmentation algorithm"""
    def __init__(self):
        self.type = "CRAFT"
        self.craft = Craft(crop_type="box", cuda=False)

    def segment(self, img: Image_cls) -> List[Image_cls]:
        # Ensure the input image is converted to a format compatible with the tokenizer
        image_array = np.array(img)
        
        prediction_result = self.craft.detect_text(image=image_array)
        polys = prediction_result["boxes"]
        
        # Convert the PIL image to a NumPy array for OpenCV processing
        original = np.array(img)
        
        # Overlay bounding boxes on the original image for visualization
        annotated_image = original.copy()
        for poly in polys:
            poly = poly.reshape(-1, 2).astype(int)
            cv2.polylines(annotated_image, [poly], isClosed=True, color=(0, 255, 0), thickness=2)
            
        # Convert annotated original image back to PIL format
        annotated_image_pil = Image_cls.fromarray(annotated_image)
        
        # crop all segments
        segments = []
        for poly in polys:
            poly = poly.reshape(-1, 2).astype(int)
            x, y, w, h = cv2.boundingRect(poly)
            segment = original[y:y+h, x:x+w]
            segments.append(Image_cls.fromarray(segment))
            
        # Return the list of images: [annotated image, each segment]
        return [annotated_image_pil] + segments




# DB segmentation algorithm
class DB_SEGMENTATION_PADDLE(Segmentation):
    def __init__(self):
        self.type = "DB"
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', det_model_dir='./models/det/det_mv3_db', rec=False)

    def segment(self, img: Image) -> list[Image]:
        # Convert PIL image to NumPy array
        result = self.ocr.ocr(np.array(img), cls=False)
        
        img2 = deepcopy(img)
        draw = ImageDraw.Draw(img2)
        

        # Extract the bounding boxes from the OCR result
        text_boxes = []
        for line in result[0]:
            # Each line contains: [box coordinates, (text, confidence)]
            points = line[0]
            # Points are in the form of (x1, y1), (x2, y2), (x3, y3), (x4, y4)
            # We can extract the box coordinates for cropping
            min_x = min([p[0] for p in points])
            max_x = max([p[0] for p in points])
            min_y = min([p[1] for p in points])
            max_y = max([p[1] for p in points])

            # Crop the text region based on bounding box coordinates
            text_box = img.crop((min_x, min_y, max_x, max_y))
            text_boxes.append(text_box)
            
            # Draw bounding box on the original image
            draw.polygon([tuple(p) for p in points], outline='red')
            

        return [img2] + text_boxes
    
# SAST segmentation algorithm

class SAST_SEGMENTATION_PADDLE(Segmentation):
    def __init__(self):
        self.type = "SAST"
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', det_model_dir='./models/det/det_sast')

    def segment(self, img: Image) -> list[Image]:
        # Convert PIL image to NumPy array
        result = self.ocr.ocr(np.array(img), cls=False)
        
        img2 = deepcopy(img)
        draw = ImageDraw.Draw(img2)
        

        # Extract the bounding boxes from the OCR result
        text_boxes = []
        for line in result[0]:
            # Each line contains: [box coordinates, (text, confidence)]
            points = line[0]
            # Points are in the form of (x1, y1), (x2, y2), (x3, y3), (x4, y4)
            # We can extract the box coordinates for cropping
            min_x = min([p[0] for p in points])
            max_x = max([p[0] for p in points])
            min_y = min([p[1] for p in points])
            max_y = max([p[1] for p in points])

            # Crop the text region based on bounding box coordinates
            text_box = img.crop((min_x, min_y, max_x, max_y))
            text_boxes.append(text_box)
            
            # Draw bounding box on the original image
            draw.polygon([tuple(p) for p in points], outline='red')
            

        return [img2] + text_boxes
    
    
#CTPN

class CTPN_SEGMENTATION_PADDLE(Segmentation):
    def __init__(self):
        self.type = "CTPN"
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', det_model_dir='./models/det/det_ctpn')

    def segment(self, img: Image) -> list[Image]:
        # Convert PIL image to NumPy array
        result = self.ocr.ocr(np.array(img), cls=False)
        
        img2 = deepcopy(img)
        draw = ImageDraw.Draw(img2)
        

        # Extract the bounding boxes from the OCR result
        text_boxes = []
        for line in result[0]:
            # Each line contains: [box coordinates, (text, confidence)]
            points = line[0]
            # Points are in the form of (x1, y1), (x2, y2), (x3, y3), (x4, y4)
            # We can extract the box coordinates for cropping
            min_x = min([p[0] for p in points])
            max_x = max([p[0] for p in points])
            min_y = min([p[1] for p in points])
            max_y = max([p[1] for p in points])

            # Crop the text region based on bounding box coordinates
            text_box = img.crop((min_x, min_y, max_x, max_y))
            text_boxes.append(text_box)
            
            # Draw bounding box on the original image
            draw.polygon([tuple(p) for p in points], outline='red')
            

        return [img2] + text_boxes
    
    
# PSENET

class PSENET_SEGMENTATION_PADDLE(Segmentation):
    def __init__(self):
        self.type = "PSENET"
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', det_model_dir='./models/det/det_psnet')

    def segment(self, img: Image) -> list[Image]:
        # Convert PIL image to NumPy array
        result = self.ocr.ocr(np.array(img), cls=False)
        
        img2 = deepcopy(img)
        draw = ImageDraw.Draw(img2)
        

        # Extract the bounding boxes from the OCR result
        text_boxes = []
        for line in result[0]:
            # Each line contains: [box coordinates, (text, confidence)]
            points = line[0]
            # Points are in the form of (x1, y1), (x2, y2), (x3, y3), (x4, y4)
            # We can extract the box coordinates for cropping
            min_x = min([p[0] for p in points])
            max_x = max([p[0] for p in points])
            min_y = min([p[1] for p in points])
            max_y = max([p[1] for p in points])

            # Crop the text region based on bounding box coordinates
            text_box = img.crop((min_x, min_y, max_x, max_y))
            text_boxes.append(text_box)
            
            # Draw bounding box on the original image
            draw.polygon([tuple(p) for p in points], outline='red')
            

        return [img2] + text_boxes