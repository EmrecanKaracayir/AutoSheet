import os
import platform
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

from autosheet.core import match, process, recognition
from autosheet.data import image
from autosheet.utils import paths


def load_image(image_path: Path) -> tuple[str, Image.Image]:
    """
    Copy and load the image from the given path.
    """
    return image.copy_image(image_path)


def process_image(name: str, image: Image.Image) -> np.ndarray:
    """
    Process the image and return the processed image.
    """
    return process.get_processed(name, image)


def recognize_text(raw_image: Image.Image, processed_image: np.ndarray) -> tuple[str, str]:
    """
    Recognize text from the raw and processed images.
    """
    return recognition.get_recognition(np.array(raw_image), processed_image)


def find_datasheet(raw_image_text: str, processed_image_text: str) -> Path:
    """
    Find the datasheet path from the recognized text.
    """
    raw_matched_name, raw_distance = match.get_match(raw_image_text)
    processed_matched_name, processed_distance = match.get_match(processed_image_text)

    # Select the best match
    if raw_distance < processed_distance:
        pdf_name = raw_matched_name
    else:
        pdf_name = processed_matched_name

    # Return the datasheet path
    return paths.get_path(paths.PDFS_FOLDER / f"{pdf_name}.pdf")


def open_datasheet(pdf_path: Path) -> None:
    """
    Open the datasheet using the default application.
    """
    if platform.system() == "Darwin":
        subprocess.call(("open", pdf_path))
    elif platform.system() == "Windows":
        os.startfile(pdf_path)
    else:
        subprocess.call(("xdg-open", pdf_path))
