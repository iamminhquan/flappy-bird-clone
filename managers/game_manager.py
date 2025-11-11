from __future__ import annotations
from entities.bird import Bird
from managers.pipe_manager import PipeManager
from managers.score_manager import ScoreManager
import pygame


def check_collisions(bird: Bird, pipe_manager: PipeManager) -> bool:
    """Checks if the bird collides with any pipe.

    Args:
        bird (Bird): The bird instance to check for collisions.
        pipe_manager (PipeManager): The manager containing all active pipes.

    Returns:
        bool: True if the bird collides with any pipe, False otherwise.
    """
    pipe_sprites = pipe_manager.get_all_pipe_sprites()
    return (
        pygame.sprite.spritecollideany(bird, pygame.sprite.Group(pipe_sprites))
        is not None
    )


def reset_game(
    bird: Bird, pipe_manager: PipeManager, score_manager: ScoreManager
) -> None:
    """Resets the core game state to its initial configuration.

    This function resets the bird's position and velocity, clears and respawns all
    pipes via the pipe manager, and resets the score.

    Args:
        bird (Bird): The bird instance to reset.
        pipe_manager (PipeManager): The manager to reset all pipe pairs.
        score_manager (ScoreManager): The manager to reset the score.

    Returns:
        None
    """
    bird.reset(70, 90)
    pipe_manager.reset()
    score_manager.reset_score()
