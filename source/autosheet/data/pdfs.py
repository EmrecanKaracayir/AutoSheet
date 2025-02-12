from autosheet.utils import paths

_PDF_NAMES: list[str] | None = None


def get_pdf_names() -> list[str]:
    """
    Get the names of the PDFs in the PDFs folder.
    """
    global _PDF_NAMES

    # Return the cached PDFs if they exist
    if _PDF_NAMES is not None:
        return _PDF_NAMES

    # Load the PDFs from the file system
    _PDF_NAMES = [file.stem for file in paths.PDFS_FOLDER.iterdir() if file.is_file()]
    return _PDF_NAMES
