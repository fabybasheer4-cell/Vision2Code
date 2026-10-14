import torch
import numpy as np
from ultralytics import YOLO

# Load pre-trained model (you'll need to train this)
MODEL_PATH = 'models/ui_component_detector.pt'


def detect_components(image):
    """
    Detect UI components using YOLO model
    """
    try:
        # Load YOLO model
        model = YOLO(MODEL_PATH)

        # Perform detection
        results = model(image)

        components = []

        # UI component classes
        component_types = {
            0: 'button',
            1: 'text_field',
            2: 'image',
            3: 'card',
            4: 'navbar',
            5: 'footer',
            6: 'heading',
            7: 'paragraph',
            8: 'checkbox',
            9: 'radio_button',
            10: 'dropdown',
            11: 'icon',
            12: 'container'
        }

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())

                component = {
                    'type': component_types.get(cls, 'unknown'),
                    'bbox': [x1, y1, x2, y2],
                    'confidence': conf,
                    'position': {
                        'x': x1,
                        'y': y1,
                        'width': x2 - x1,
                        'height': y2 - y1
                    }
                }
                components.append(component)

        return components

    except Exception as e:
        print(f"Component detection error: {e}")
        return []