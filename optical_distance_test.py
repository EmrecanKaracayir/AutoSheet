import argparse
import csv
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial.distance import directed_hausdorff
from skimage.metrics import structural_similarity as ssim
from skimage.morphology import skeletonize

# Configure paths and parameters
GLYPH_CACHE = Path("resource/glyphs")
PRECOMPUTED_PATH = Path("resource/precomputed.json")
FONT_PATH = Path("resource/font.ttf")
TARGET_SIZE = 200  # Standard image size after processing

# Ensure directories exist
GLYPH_CACHE.mkdir(parents=True, exist_ok=True)



def extract_edge_contour(img):
    """
    Extract the edge contour from the processed image using Canny.
    Returns the largest contour (Nx2 array of points) and the full edge image.
    """
    edges = cv2.Canny(img, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        contour = largest.reshape(-1, 2)
        return contour, edges
    else:
        return np.empty((0, 2)), edges


def compute_hausdorff_distance(contour1, contour2):
    """
    Compute symmetric Hausdorff distance between two contours.
    """
    if contour1.shape[0] == 0 or contour2.shape[0] == 0:
        return np.inf
    d1 = directed_hausdorff(contour1, contour2)[0]
    d2 = directed_hausdorff(contour2, contour1)[0]
    return max(d1, d2)


def compute_chamfer_distance(edges1, edges2):
    """
    Compute chamfer distance by calculating the Euclidean distance transform.
    """
    dt = cv2.distanceTransform(255 - edges1, cv2.DIST_L2, 3)
    pts = np.where(edges2 != 0)
    if len(pts[0]) == 0:
        return np.inf
    return np.mean(dt[pts])


def compute_geometric_distance(img1, img2):
    """
    Compute geometric distance from edges using a fusion of Hausdorff
    and Chamfer distances.
    """
    proc1 = preprocess_glyph(img1)
    proc2 = preprocess_glyph(img2)
    contour1, edges1 = extract_edge_contour(proc1)
    contour2, edges2 = extract_edge_contour(proc2)
    hausdorff = compute_hausdorff_distance(contour1, contour2)
    chamfer = compute_chamfer_distance(edges1, edges2)
    # Weighting: 60% for Hausdorff and 40% for Chamfer.
    return 0.6 * hausdorff + 0.4 * chamfer


def compute_shape_match(img1, img2):
    """
    Compute a global shape match using OpenCV's matchShapes.
    This method compares two contours (computed from the processed images).
    """
    proc1 = preprocess_glyph(img1)
    proc2 = preprocess_glyph(img2)
    c1, _ = extract_edge_contour(proc1)
    c2, _ = extract_edge_contour(proc2)
    if c1.shape[0] == 0 or c2.shape[0] == 0:
        return np.inf
    # Use method I1 (which is robust across rotations/scales)
    match = cv2.matchShapes(c1, c2, cv2.CONTOURS_MATCH_I1, 0)
    return match


def compute_skeleton_distance(img1, img2, scale_factor=50):
    """
    Compute a skeleton-based distance:
      - Use skeletonization on the processed binary image.
      - Calculate SSIM between the resulting skeleton images.
      - Convert similarity to a "difference" (1 - SSIM) and scale.
    """
    proc1 = preprocess_glyph(img1)
    proc2 = preprocess_glyph(img2)
    # Normalize to [0,1]
    bin1 = (proc1 / 255).astype(np.uint8)
    bin2 = (proc2 / 255).astype(np.uint8)
    skel1 = skeletonize(bin1.astype(bool)).astype(np.float32)
    skel2 = skeletonize(bin2.astype(bool)).astype(np.float32)
    try:
        sim = ssim(skel1, skel2, data_range=1)
    except ValueError:
        sim = 0
    diff = 1 - sim
    return diff * scale_factor


def get_complexity(img):
    """
    Compute a simple complexity measure for the given glyph image.
    Here we use the ratio of edge pixels (using Canny) to the total number of pixels.
    """
    proc = preprocess_glyph(img)
    edges = cv2.Canny(proc, 50, 150)
    edge_count = np.count_nonzero(edges)
    return edge_count / (TARGET_SIZE * TARGET_SIZE)


def compute_optical_distance(img1, img2):
    """
    Compute the fused optical distance between two glyph images,
    incorporating the difference in their complexities.

    The optical distance is computed as a weighted fusion of:
      - Geometric distance (edge-based)
      - Global shape match (Hu-based matchShapes)
      - Skeleton-based difference (via skeleton SSIM)

    Then we compute each glyph's complexity (ratio of edge pixels) and
    augment the optical distance by adding a term proportional to the
    absolute difference in complexities.
    """
    geo = compute_geometric_distance(img1, img2)
    shape = compute_shape_match(img1, img2)
    skel = compute_skeleton_distance(img1, img2, scale_factor=50)

    # More balanced weights for each metric:
    alpha = 0  # geometric distance
    beta = 0  # shape match
    gamma = 1  # skeleton-based difference

    base_distance = alpha * geo + beta * shape + gamma * skel

    # Compute complexities of the two glyphs
    complexity1 = get_complexity(img1)
    complexity2 = get_complexity(img2)

    # Compute the difference in complexity
    complexity_diff = abs(complexity1 - complexity2)

    # Adjust the optical distance by a term proportional to the complexity difference.
    # The weight factor k controls how strongly differences in complexity affect our score.
    k = 0
    final_distance = base_distance + k * complexity_diff

    return final_distance


def get_cached_distance(char1, char2, precomputed):
    """
    Retrieve a cached optical distance for a given glyph pair,
    or compute and cache it if not present.
    """
    key = f"{min(char1, char2)}_{max(char1, char2)}"
    if key in precomputed:
        return precomputed[key]
    glyph1 = get_glyph(char1)
    glyph2 = get_glyph(char2)
    distance = compute_optical_distance(glyph1, glyph2)
    precomputed[key] = float(distance)
    with open(PRECOMPUTED_PATH, "w") as f:
        json.dump(precomputed, f, indent=2)
    return distance


def generate_sorted_distance_list(precomputed):
    """
    Generate a sorted list of unique glyph pairs by optical distance.
    Each item is a tuple: (pair, distance), where pair is "X_Y".
    """
    characters = list("0123456789") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    pairs = []
    for i, ch1 in enumerate(characters):
        for j, ch2 in enumerate(characters):
            if j <= i:
                continue
            distance = get_cached_distance(ch1, ch2, precomputed)
            pairs.append((f"{ch1}_{ch2}", distance))
    pairs.sort(key=lambda x: x[1])
    return pairs


def export_sorted_distance_csv(precomputed, filename="glyph_distances.csv"):
    """
    Export sorted glyph pair distances to a CSV file.
    """
    characters = list("0123456789") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    pairs = []
    for ch1 in characters:
        for ch2 in characters:
            if ch1 == ch2:
                continue  # skip identical characters
            distance = get_cached_distance(ch1, ch2, precomputed)
            pairs.append((ch1, ch2, distance))
    pairs.sort(key=lambda x: x[2])
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["char1", "char2", "distance"])
        for char1, char2, distance in pairs:
            writer.writerow([char1, char2, f"{distance:.4f}"])
    print(f"Exported sorted distances to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Compute improved optical glyph distance and output tables."
    )
    parser.add_argument("--str1", help="First string for pairwise comparison")
    parser.add_argument("--str2", help="Second string for pairwise comparison")
    parser.add_argument("--table", action="store_true", help="Generate a full table of distances")
    parser.add_argument(
        "--export", action="store_true", help="Export sorted glyph pair distances to CSV"
    )
    args = parser.parse_args()

    if args.table:
        try:
            with open(PRECOMPUTED_PATH) as f:
                precomputed = json.load(f)
        except FileNotFoundError:
            precomputed = {}
        pairs = generate_sorted_distance_list(precomputed)
        if args.export:
            export_sorted_distance_csv(precomputed)
        else:
            print("\nSorted Glyph Pair Distances:")
            for pair, distance in pairs:
                print(f"{pair}: {distance:.4f}")
    elif args.str1 and args.str2:
        if len(args.str1) != len(args.str2):
            raise ValueError("Strings must have equal length.")
        try:
            with open(PRECOMPUTED_PATH) as f:
                precomputed = json.load(f)
        except FileNotFoundError:
            precomputed = {}
        total_distance = 0
        for c1, c2 in zip(args.str1, args.str2):
            if c1 == c2:
                continue
            total_distance += get_cached_distance(c1, c2, precomputed)
        print(f"Optical distance for the string pair: {total_distance:.4f}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
