import cv2
import numpy as np
from PIL import Image

from autosheet.utils import constants, paths


def get_processed(name: str, image: Image.Image) -> np.ndarray:
    """ """
    # 1. Resize image
    resized_image = _resize_image(image)
    _debug_image(resized_image, name, 1)

    # 2. Convert to grayscale
    grayscaled_image = _grayscale_image(resized_image)
    _debug_image(grayscaled_image, name, 2)

    # 3. Brightness correction using gamma adjustment
    gamma_adjusted_image = _gamma_adjust_image(grayscaled_image)
    _debug_image(gamma_adjusted_image, name, 3)

    # 4. Enhance contrast using CLAHE
    clahe_enhanced_image = _clahe_enhance_image(gamma_adjusted_image)
    _debug_image(clahe_enhanced_image, name, 4)

    # 5. Denoise
    denoised_image = _denoise_image(clahe_enhanced_image)
    _debug_image(denoised_image, name, 5)

    # 6. Invert image
    inverted_image = _invert_image(denoised_image)
    _debug_image(inverted_image, name, 6)

    # 7. Binarize image
    binary_image = _binarize_image(inverted_image)
    _debug_image(binary_image, name, 7)

    # 8. Clean image
    cleaned_image = _clean_image(binary_image)
    _debug_image(cleaned_image, name, 8)

    # 9. Deskew image
    deskewed_image = _deskew_image(cleaned_image)
    _debug_image(deskewed_image, name, 9)

    return deskewed_image


def _resize_image(image: Image.Image) -> Image.Image:
    """
    Resize the input image to a maximum width of 1024 pixels.
    """
    width, height = image.size

    # Resize only if the image is wider than 1024 pixels.
    if width > 1024:
        factor = 1024.0 / width
        new_size = (int(width * factor), int(height * factor))
        resized_image = image.resize(new_size, resample=Image.Resampling.LANCZOS)
    else:
        resized_image = image

    return resized_image


def _grayscale_image(image: Image.Image) -> np.ndarray:
    """
    Convert the image from BGR to grayscale.
    """
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)


def _gamma_adjust_image(image: np.ndarray) -> np.ndarray:
    """
    Apply gamma correction to adjust image brightness.
    """
    invGamma = 1.0 / 0.8
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.linspace(0, 255, 256)]).astype(
        "uint8"
    )
    return cv2.LUT(image, table)


def _clahe_enhance_image(gray_image: np.ndarray) -> np.ndarray:
    """
    Enhance contrast of a grayscale image using CLAHE.
    """
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    return clahe.apply(gray_image)


def _denoise_image(image: np.ndarray) -> np.ndarray:
    """
    Remove noise from a grayscale image using fast non-local means denoising.
    """
    return cv2.fastNlMeansDenoising(image, None, h=10, templateWindowSize=7, searchWindowSize=15)


def _invert_image(image: np.ndarray) -> np.ndarray:
    """
    Invert a grayscale image.
    """
    return cv2.bitwise_not(image)


def _binarize_image(image: np.ndarray) -> np.ndarray:
    """
    Convert an image to a binary image using adaptive thresholding.
    """
    return cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        15,
        2,
    )


def _clean_image(image: np.ndarray) -> np.ndarray:
    """
    Perform morphological closing to connect text segments and reduce noise.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=1)
    return closed


def _deskew_image(image: np.ndarray) -> np.ndarray:
    """
    Deskew a rotated image using Hough line transform.
    """
    # Edge detection
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    if lines is None:
        return image

    # Calculate the angle of rotation
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2((y2 - y1), (x2 - x1)))
        angles.append(angle)

    # Rotate the image
    median_angle = np.median(angles)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
    rotated_image = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated_image


def _debug_image(image: np.ndarray, name: str, step: int) -> None:
    """
    Save the image to the debug folder.
    """
    # Get the step text
    match step:
        case 1:
            step_text = "resized"
        case 2:
            step_text = "grayscaled"
        case 3:
            step_text = "gamma-corrected"
        case 4:
            step_text = "clahe-enhanced"
        case 5:
            step_text = "denoised"
        case 6:
            step_text = "inverted"
        case 7:
            step_text = "binarized"
        case 8:
            step_text = "cleaned"
        case 9:
            step_text = "deskewed"
        case _:
            step_text = "unknown"

    # Save the image
    cv2.imwrite(
        paths.get_path(
            paths.DEBUG_PROCESSED_FOLDER / f"{name}_{step}_{step_text}.{constants.IMAGE_FORMAT}"
        ),
        image,
    )
