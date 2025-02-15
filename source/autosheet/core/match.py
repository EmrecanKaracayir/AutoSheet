from autosheet.core import distance
from autosheet.data import matches, pdfs
from autosheet.data.models.Match import Match


def get_match(subject: str) -> tuple[str, float]:
    """
    Match the subject string to the closest targe string.
    """
    cache = matches.get_matches()

    # Get the list of target strings
    targets = pdfs.get_pdf_names()
    matching_results = {}

    # If the subject is not in the cache, add it
    if subject not in cache:
        cache[subject] = []

    # Compute the distance between the subject and each target
    for target in targets:
        # Lookup the match in the cache
        found_in_cache = False
        for match in cache[subject]:
            if match.target == target:
                matching_results[target] = match.distance
                found_in_cache = True
                break

        # Skip the target if it is already in the cache
        if found_in_cache:
            continue

        # Compute the distance between the subject and the target
        distance = _compute_min_distance(subject, target)
        matching_results[target] = distance

        # Add the match to the cache
        cache[subject].append(Match(target, distance))

    # Save the updated cache
    matches.save_matches()

    # Find the target with the minimum distance
    best_target = min(matching_results, key=matching_results.get)
    return best_target, matching_results[best_target]


def _compute_min_distance(subject: str, target: str) -> float:
    """
    Compute the minimum distance between the subject and the target.
    """
    # Subject and target are the same length, compute the distance
    if len(subject) == len(target):
        return _compute_levenshtein_distance(subject, target)
    best_score = float("inf")

    # Subject is longer, window the target
    if len(subject) > len(target):
        window_size = len(target)

        # Slide the window over the subject
        for i in range(len(subject) - len(target) + 1):
            sub_subject = subject[i : i + window_size]

            # Compute the distance between the windowed subject and the target
            score = _compute_levenshtein_distance(sub_subject, target)
            best_score = min(best_score, score)

    # Target is longer, window the subject
    else:
        window_size = len(subject)

        # Slide the window over the target
        for i in range(len(target) - len(subject) + 1):
            sub_target = target[i : i + window_size]

            # Compute the distance between the subject and the windowed target
            score = _compute_levenshtein_distance(subject, sub_target)
            best_score = min(best_score, score)

    return best_score


def _compute_levenshtein_distance(subject: str, target: str) -> float:
    """
    Compute the Levenshtein distance between subject and target using custom costs.
    Insertion and deletion costs are determined by comparing a character with an empty string.
    Substitution cost is given by distance.get_distance for the two characters.
    """
    m = len(subject)
    n = len(target)

    # Initialize a (m+1) x (n+1) DP matrix.
    dp = [[0.0 for _ in range(n + 1)] for _ in range(m + 1)]

    # Base cases using custom cost functions
    for i in range(1, m + 1):
        # Deletion: cost to delete subject[i-1] is cost of comparing it to an empty string.
        dp[i][0] = dp[i - 1][0] + distance.get_distance(subject[i - 1], "")

    for j in range(1, n + 1):
        # Insertion: cost to insert target[j-1] is cost of comparing an empty string to it.
        dp[0][j] = dp[0][j - 1] + distance.get_distance("", target[j - 1])

    # Fill the DP matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            deletion_cost = dp[i - 1][j] + distance.get_distance(subject[i - 1], "")
            insertion_cost = dp[i][j - 1] + distance.get_distance("", target[j - 1])
            substitution_cost = dp[i - 1][j - 1] + distance.get_distance(
                subject[i - 1], target[j - 1]
            )
            dp[i][j] = min(deletion_cost, insertion_cost, substitution_cost)

    return dp[m][n]
