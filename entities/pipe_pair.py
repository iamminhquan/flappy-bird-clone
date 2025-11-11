from __future__ import annotations
from typing import List

import random
import pygame
import constants

from entities.pipe import Pipe


class PipePair:
    """Manages a pair of pipes (top and bottom) separated by a vertical gap."""

    def __init__(
        self: PipePair,
        x: int,
        width: float,
        gap: float,
        speed: float,
        color: List[int] = constants.GREEN,
    ) -> None:
        """Initializes a pipe pair with a top and bottom pipe.

        Args:
            x (int): Initial horizontal position of the pipe pair in pixels.
            width (float): Width of each pipe in pixels.
            gap (float): Vertical gap between top and bottom pipes in pixels.
            speed (float): Leftward movement speed in pixels per frame.
            color (List[int], optional): RGB color of the pipes. Defaults to constants.GREEN.
        """
        self.__x = x
        self.__width = width
        self.__gap = gap
        self.__speed = speed
        self.__color = color

        self.__top_pipe_height = random.randint(
            constants.PIPE_HEIGHT,
            constants.SCREEN_HEIGHT - self.__gap - constants.PIPE_HEIGHT,
        )
        self.__bottom_pipe_height = constants.SCREEN_HEIGHT - self.__gap - self.__top_pipe_height

        self.top_pipe = Pipe(
            self.__x, 0, self.__width, self.__top_pipe_height, self.__speed, self.__color
        )
        self.bottom_pipe = Pipe(
            self.__x,
            self.__top_pipe_height + self.__gap,
            self.__width,
            self.__bottom_pipe_height,
            self.__speed,
            self.__color,
        )

    def update(self: PipePair) -> None:
        """Updates both top and bottom pipes in the pair.

        Returns:
            None
        """
        self.top_pipe.update()
        self.bottom_pipe.update()

    def draw(self: PipePair, screen: pygame.Surface) -> None:
        """Draws both pipes to the given screen.

        Args:
            screen (pygame.Surface): The main display surface.

        Returns:
            None
        """
        self.top_pipe.draw(screen)
        self.bottom_pipe.draw(screen)

    def get_pipes(self: PipePair) -> tuple[Pipe, Pipe]:
        """Gets the top and bottom pipe sprites.

        Returns:
            tuple[Pipe, Pipe]: The top and bottom pipes.
        """
        return self.top_pipe, self.bottom_pipe
