import numpy as np
from autosheet.core import process, recognition
from autosheet.utils import constants
from PIL import Image


def test_get_recognition():
    # Set debug mode to True
    constants.DEBUG = True

    # Start testing
    test_raw_image = Image.open("data/images/1.png")
    test_processed_image = process.get_processed("1", test_raw_image)
    raw_result, processed_result = recognition.get_recognition(
        np.array(test_raw_image), test_processed_image
    )
    assert len(raw_result) > 0 and len(processed_result) > 0
