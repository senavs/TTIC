class SubjectSettings:
    MIN_AGE: int = 5
    MAX_AGE: int = 90


class PathologySettings:
    PROB_INFECTION: float = 0.15
    PROB_DEATH: float = 0.03
    EXPOSED_MAX_DAY: int = 7
    INFECTIOUS_MAX_DAY: int = 14
