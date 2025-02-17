from autosheet.core import match
from autosheet.utils import constants


def test_get_match() -> None:
    # Set debug mode to True
    constants.DEBUG = True

    # Start testing
    test_subject = "74LS0O"
    assert match.get_match(test_subject)[0] == "74LS00"

    # Longer subject
    test_subject = "74L5IAXXXXXX"
    assert match.get_match(test_subject)[0] == "74LS14"

    # Shorter subject
    test_subject = "7AXX151"
    assert match.get_match(test_subject)[0] == "74LS151"

    # Exact length
    test_subject = "XXLSB64"
    assert match.get_match(test_subject)[0] == "74LS86A"
