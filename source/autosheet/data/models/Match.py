class Match:
    """
    A class representing a match between subject and target.
    """

    def __init__(self, target: str, distance: float) -> None:
        """
        Initialize a Match object.
        """
        self.target = target
        self.distance = distance

    def to_dict(self) -> dict:
        """
        Convert the Match object to a dictionary.
        """
        return {"target": self.target, "distance": self.distance}

    @classmethod
    def from_dict(cls, data: dict) -> "Match":
        """
        Construct a Match object from a dictionary.
        """
        return cls(data["target"], data["distance"])
