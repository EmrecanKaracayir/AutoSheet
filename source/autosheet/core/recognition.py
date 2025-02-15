import easyocr
import numpy as np


def get_recognition(raw_image: np.ndarray, processed_image: np.ndarray) -> tuple[str, str]:
    """
    Get text recognition from raw and processed images.
    """
    raw_image_texts = easyocr.Reader(["en"]).readtext(raw_image)
    processed_image_texts = easyocr.Reader(["en"]).readtext(processed_image)
    raw_image_text = " ".join([text[1] for text in raw_image_texts])
    processed_image_text = " ".join([text[1] for text in processed_image_texts])
    return raw_image_text, processed_image_text
