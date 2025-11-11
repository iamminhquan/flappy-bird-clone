from __future__ import annotations
from pygame import sprite
import pygame
import constants


class Bird(sprite.Sprite):
    """Represents the bird character in the game.

    Handles movement, jumping, resetting position, and rendering.
    Inherits from `pygame.sprite.Sprite` to enable collision detection.
    """

    def __init__(self: Bird, x: int, y: int, surface: pygame.Surface) -> None:
        """Initializes a new bird instance.

        Args:
            x (int): Initial horizontal position in pixels.
            y (int): Initial vertical position in pixels.
            surface (pygame.Surface): The image surface used to represent the bird.
        """
        super().__init__()
        self.__x = x
        self.__y = y
        self.__velocity = 0.0
        self.__gravity = 0.5
        self.__jump_force = -7.0
        self.__surface = surface

        # Set up the sprite's rect for collision detection
        self.rect = self.__surface.get_rect()
        self.rect.x = x
        self.rect.y = y

    def movement(self: Bird) -> None:
        """Updates the bird's movement for the current frame.

        Applies gravity, updates vertical position based on velocity,
        clamps the bird within screen bounds, and updates the sprite's rectangle.

        Returns:
            None
        """
        self.__velocity += self.__gravity
        self.__y += self.__velocity

        if self.__y + self.__surface.get_height() >= constants.SCREEN_HEIGHT:
            self.__y = constants.SCREEN_HEIGHT - self.__surface.get_height()
            self.__velocity = 0.0

        if self.__y <= 0:
            self.__y = 0

        self.rect.x = self.__x
        self.rect.y = self.__y

    def jump(self: Bird) -> None:
        """Makes the bird jump by applying an upward impulse.

        Sets the bird's vertical velocity to a negative value,
        temporarily countering gravity and causing upward movement.

        Returns:
            None
        """
        self.__velocity = self.__jump_force

    def reset(self: Bird, x: int, y: int) -> None:
        """Resets the bird's position and vertical velocity.

        Args:
            x (int): New horizontal position in pixels.
            y (int): New vertical position in pixels.

        Returns:
            None
        """
        self.__x = x
        self.__y = y
        self.__velocity = 0.0
        self.rect.x = x
        self.rect.y = y

    def draw(self: Bird, screen: pygame.Surface) -> None:
        """Renders the bird on the specified screen surface.

        Args:
            screen (pygame.Surface): The main display surface to render the bird on.

        Returns:
            None
        """
        screen.blit(self.__surface, [self.__x, self.__y])

    @property
    def x(self: Bird) -> float:
        """Gets the current horizontal position of the bird.

        Returns:
            float: The x-coordinate in pixels.
        """
        return self.__x

    @property
    def y(self: Bird) -> float:
        """Gets the current vertical position of the bird.

        Returns:
            float: The y-coordinate in pixels.
        """
        return self.__y

    @property
    def velocity(self: Bird) -> float:
        """Gets the bird's current vertical velocity.

        Returns:
            float: The velocity in pixels per frame.
        """
        return self.__velocity

