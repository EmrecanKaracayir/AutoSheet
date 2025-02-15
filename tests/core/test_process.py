from PIL import Image

from autosheet.core import process


def test_get_processed():
    test_image = Image.open("data/images/1.png")
    process.get_processed("1", test_image)
    assert True
