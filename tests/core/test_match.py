from autosheet.core import match


def test_get_match() -> None:
    test_subject = "74LS0O"
    assert match.get_match(test_subject) == "74LS00"

    # Longer subject
    test_subject = "74L5IAXXXXXX"
    assert match.get_match(test_subject) == "74LS14"

    # Shorter subject
    test_subject = "7AXX151"
    assert match.get_match(test_subject) == "74LS151"

    # Exact length
    test_subject = "XXLSB64"
    assert match.get_match(test_subject) == "74LS86A"
