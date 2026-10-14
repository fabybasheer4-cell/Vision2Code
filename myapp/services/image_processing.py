import cv2
import numpy as np
import base64
from PIL import Image
import io


def process_image(image_data):
    """
    Process uploaded image - preprocess for model input
    """
    try:
        # Decode base64 image
        if isinstance(image_data, str) and ',' in image_data:
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # Convert to numpy array
        img_array = np.array(image)

        # Convert RGB to BGR for OpenCV
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # Preprocessing steps
        # 1. Resize for model input
        img_array = cv2.resize(img_array, (416, 416))

        # 2. Normalize
        img_array = img_array / 255.0

        # 3. Denoise
        img_array = cv2.fastNlMeansDenoisingColored(
            (img_array * 255).astype(np.uint8),
            None, 10, 10, 7, 21
        )

        return img_array

    except Exception as e:
        print(f"Image processing error: {e}")
        return None