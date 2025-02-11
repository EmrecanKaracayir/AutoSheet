from autosheet.core import distance, glyph


def test_get_distance():
    test_glyph = "A"
    test_mask = glyph.get_glyph_mask(test_glyph)

    # Compute the distance between the mask and itself
    assert distance.get_distance(test_glyph, test_mask, test_glyph, test_mask) == 0

    # Compute the difference between two largely different masks
    test_glyph1 = "A"
    test_mask1 = glyph.get_glyph_mask(test_glyph1)
    test_glyph2 = "B"
    test_mask2 = glyph.get_glyph_mask(test_glyph2)

    large_distance = distance.get_distance(test_glyph1, test_mask1, test_glyph2, test_mask2)

    # Reverse the order of the masks
    reverse_distance = distance.get_distance(test_glyph2, test_mask2, test_glyph1, test_mask1)

    assert large_distance == reverse_distance

    # Compute the difference between two similar masks
    test_glyph3 = "B"
    test_mask3 = glyph.get_glyph_mask(test_glyph3)
    test_glyph4 = "8"
    test_mask4 = glyph.get_glyph_mask(test_glyph4)

    small_distance = distance.get_distance(test_glyph3, test_mask3, test_glyph4, test_mask4)

    assert large_distance > small_distance

    # Compute all glyph differences
    glyphs = list("0123456789") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for i, g1 in enumerate(glyphs):
        for j, g2 in enumerate(glyphs):
            if j < i:
                continue
            mask1 = glyph.get_glyph_mask(g1)
            mask2 = glyph.get_glyph_mask(g2)
            distance.get_distance(g1, mask1, g2, mask2)
