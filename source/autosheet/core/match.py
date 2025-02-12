from autosheet.core import distance
from autosheet.data import matches, pdfs
from autosheet.data.models.Match import Match


def get_match(subject: str) -> str:
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
        for match in cache[subject]:
            if match.target == target:
                matching_results[target] = match.distance
                break

        # Compute the distance between the subject and the target
        distance = _compute_min_distance(subject, target)
        matching_results[target] = distance

        # Add the match to the cache
        cache[subject].append(Match(target, distance))

    # Save the updated cache
    matches.save_matches()

    # Return the target with the minimum distance
    return min(matching_results, key=matching_results.get)


def _compute_min_distance(subject: str, target: str) -> float:
    """
    Compute the minimum distance between the subject and the target.
    """
    # Subject and target are the same length, compute the distance
    if len(subject) == len(target):
        return sum(distance.get_distance(g1, g2) for g1, g2 in zip(subject, target))
    best_score = float("inf")

    # Subject is longer, window the target
    if len(subject) > len(target):
        window_size = len(target)

        # Slide the window over the subject
        for i in range(len(subject) - len(target) + 1):
            sub_subject = subject[i : i + window_size]

            # Compute the distance between the windowed subject and the target
            score = sum(distance.get_distance(c, t) for c, t in zip(sub_subject, target))
            best_score = min(best_score, score)

    # Target is longer, window the subject
    else:
        window_size = len(subject)

        # Slide the window over the target
        for i in range(len(target) - len(subject) + 1):
            sub_target = target[i : i + window_size]

            # Compute the distance between the subject and the windowed target
            score = sum(distance.get_distance(c, t) for c, t in zip(subject, sub_target))
            best_score = min(best_score, score)

    return best_score
