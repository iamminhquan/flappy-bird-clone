from __future__ import annotations
from typing import List
from pygame import sprite

import pygame
import constants


class Pipe(sprite.Sprite):
    """Represents a single pipe (top or bottom) for collision detection.

    Inherits from `pygame.sprite.Sprite`.
    """

    def __init__(
        self: Pipe,
        x: int,
        y: int,
        width: float,
        height: float,
        speed: float,
        color: List[int] = constants.GREEN,
    ) -> None:
        """Initializes a new pipe.

        Args:
            x (int): Initial horizontal position in pixels.
            y (int): Initial vertical position in pixels.
            width (float): Width of the pipe in pixels.
            height (float): Height of the pipe in pixels.
            speed (float): Leftward movement speed in pixels per frame.
            color (List[int], optional): RGB color of the pipe. Defaults to constants.GREEN.
        """
        super().__init__()
        self.__x = x
        self.__speed = speed
        self.__color = color

        self.rect = pygame.Rect(x, y, width, height)

    def update(self: Pipe) -> None:
        """Moves the pipe leftward based on its speed and updates its rectangle.

        Returns:
            None
        """
        self.__x -= self.__speed
        self.rect.x = self.__x

    def draw(self: Pipe, screen: pygame.Surface) -> None:
        """Draws the pipe on the given screen.

        Args:
            screen (pygame.Surface): The main display surface.

        Returns:
            None
        """
        pygame.draw.rect(screen, self.__color, self.rect)

    @property
    def speed(self: Pipe) -> float:
        """Gets the current leftward speed of the pipe.

        Returns:
            float: Speed in pixels per frame.
        """
        return self.__speed
