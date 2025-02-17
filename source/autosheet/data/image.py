import shutil
from pathlib import Path

from PIL import Image

from autosheet.utils import paths


def get_last_image() -> tuple[Path, Image.Image]:
    """
    Get the last image in the images folder.
    """
    # Generate a list of .png files in the folder
    image_paths = [file for file in paths.get_path(paths.IMAGES_FOLDER).iterdir() if file.is_file()]

    # Sort files by name and select the last one
    last_image_path = sorted(image_paths, key=lambda f: int(f.stem), reverse=True)[0]

    return last_image_path, Image.open(last_image_path)


def copy_image(path: Path) -> tuple[str, Image.Image]:
    """
    Copy the image to the images folder.
    """
    # Generate a list of .png files in the folder
    image_paths = [file for file in paths.get_path(paths.IMAGES_FOLDER).iterdir() if file.is_file()]

    # Sort files by name and select the last one
    last_image_path = sorted(image_paths, key=lambda f: int(f.stem), reverse=True)[0]

    # Add 1 to the last image name
    new_path = paths.get_path(paths.IMAGES_FOLDER / f"{int(last_image_path.stem) + 1}{path.suffix}")

    # Copy the image to the images folder
    shutil.copy(path, new_path)

    # Return the copied image
    return new_path.stem, Image.open(new_path)
