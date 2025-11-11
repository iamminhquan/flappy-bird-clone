from __future__ import annotations


class ScoreManager:
    """Tracks and manages the player's current score and high score."""

    def __init__(self: ScoreManager) -> None:
        """Initializes the score manager with scores set to zero."""
        self.__score = 0
        self.__high_score = 0

    def increment_score(self: ScoreManager) -> None:
        """Increments the current score by one.

        Returns:
            None
        """
        self.__score += 1

    def reset_score(self) -> None:
        """Resets the current score to zero.

        Returns:
            None
        """
        self.__score = 0

    def update_high_score(self: ScoreManager) -> None:
        """Updates the high score if the current score is greater.

        Returns:
            None
        """
        if self.__score > self.__high_score:
            self.__high_score = self.__score

    @property
    def score(self: ScoreManager) -> int:
        """Gets the current score.

        Returns:
            int: The current score value.
        """
        return self.__score

    @property
    def high_score(self: ScoreManager) -> int:
        """Gets the highest score achieved.

        Returns:
            int: The high score value.
        """
        return self.__high_score
