from __future__ import annotations
from entities.pipe_pair import PipePair
from entities.pipe import Pipe

import constants
import pygame


class PipeManager:
    """Manages the lifecycle of multiple pipe pairs, including spawning, updating, drawing, and removal.

    Responsible for keeping pipe spacing consistent, respawning new pipes when needed,
    and providing all individual pipe sprites for collision detection.
    """

    def __init__(
        self: PipeManager, gap: int, pipe_width: int, speed: int, spawn_distance: int
    ) -> None:
        """Initializes the PipeManager with initial pipe pairs.

        Args:
            gap (int): Vertical gap between top and bottom pipes in pixels.
            pipe_width (int): Width of each pipe in pixels.
            speed (int): Leftward movement speed in pixels per frame.
            spawn_distance (int): Horizontal distance between consecutive pipe pairs in pixels.
        """
        self.__pipes: list[PipePair] = []
        self.__gap: int = gap
        self.__pipe_width: int = pipe_width
        self.__speed: int = speed
        self.__spawn_distance: int = spawn_distance
        self.__spawn_interval_frames: int = (
            int(self.__spawn_distance / self.__speed) if self.__speed > 0 else 60
        )
        self.__frames_since_last_spawn: int = 0

        start_x: int = constants.SCREEN_WIDTH + 100
        initial_count: int = 3
        for i in range(initial_count):
            self.__pipes.append(
                PipePair(
                    start_x + i * self.__spawn_distance,
                    self.__pipe_width,
                    self.__gap,
                    self.__speed,
                )
            )

    def update(self: PipeManager) -> None:
        """Updates all active pipe pairs, handles spawning new pipes, and removes off-screen pipes.

        Moves each pipe pair leftward, spawns new pairs at fixed intervals,
        and removes any pipes that have completely exited the screen.

        Returns:
            None
        """
        for pipe in self.__pipes:
            pipe.update()

        self.__frames_since_last_spawn += 1
        if (
            self.__frames_since_last_spawn >= self.__spawn_interval_frames
            and self.__pipes
        ):
            last_x: int = self.__pipes[-1].top_pipe.rect.x
            new_x: int = max(
                last_x + self.__spawn_distance, constants.SCREEN_WIDTH + 100
            )
            self.__pipes.append(
                PipePair(new_x, self.__pipe_width, self.__gap, self.__speed)
            )
            self.__frames_since_last_spawn = 0

        while self.__pipes and self.__pipes[0].top_pipe.rect.right < 0:
            self.__pipes.pop(0)

    def draw(self: PipeManager, screen: pygame.Surface) -> None:
        """Draws all active pipe pairs onto the given screen surface.

        Args:
            screen (pygame.Surface): The main display surface.

        Returns:
            None
        """
        for pipe in self.__pipes:
            pipe.draw(screen)

    def get_all_pipe_sprites(self: PipeManager) -> list[Pipe]:
        """Returns a list of all individual pipe sprites for collision detection.

        Returns:
            list[Pipe]: A list containing all top and bottom pipe sprites.
        """
        all_sprites: list[Pipe] = []

        for pipe_pair in self.__pipes:
            top_pipe, bottom_pipe = pipe_pair.get_pipes()
            all_sprites.append(top_pipe)
            all_sprites.append(bottom_pipe)

        return all_sprites

    def reset(self: PipeManager) -> None:
        """Resets the pipe manager to its initial state.

        Clears all current pipes, resets frame counters, and spawns initial pipe pairs.

        Returns:
            None
        """
        self.__pipes.clear()
        self.__frames_since_last_spawn = 0

        start_x: int = constants.SCREEN_WIDTH + 100
        initial_count: int = 3

        for i in range(initial_count):
            self.__pipes.append(
                PipePair(
                    start_x + i * self.__spawn_distance,
                    self.__pipe_width,
                    self.__gap,
                    self.__speed,
                )
            )
