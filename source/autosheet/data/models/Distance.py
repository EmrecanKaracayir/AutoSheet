class Distance:
    """
    A class representing a distance between subject and target.
    """

    def __init__(self, target: str, distance: float) -> None:
        """
        Initialize a Distance object.
        """
        self.target = target
        self.distance = distance

    def to_dict(self) -> dict:
        """
        Convert the Distance object to a dictionary.
        """
        return {"target": self.target, "distance": self.distance}

    @classmethod
    def from_dict(cls, data: dict) -> "Distance":
        """
        Construct a Distance object from a dictionary.
        """
        return cls(data["target"], data["distance"])
