from autosheet.core import process
from autosheet.utils import constants
from PIL import Image


def test_get_processed():
    # Set debug mode to True
    constants.DEBUG = True

    # Start testing
    test_image = Image.open("data/images/1.png")
    process.get_processed("1", test_image)
    assert True
