from __future__ import annotations

from typing import TYPE_CHECKING

import pygame  # type: ignore[import]

import constants

if TYPE_CHECKING:
    from entities.bird import Bird
    from managers.pipe_manager import PipeManager
    from managers.score_manager import ScoreManager

__all__ = [
    "draw_score",
    "draw_main_menu",
    "draw_game_over_menu",
    "draw_confirm_exit",
    "draw_window",
]


def draw_score(screen: pygame.Surface, score_manager: ScoreManager) -> None:
    """
    Draw the current score in the top left corner.
    """
    if not pygame.font.get_init():
        pygame.font.init()

    font = _get_font("arial", 36)

    if font:
        score_text = font.render(f"Score: {score_manager.score}", True, constants.BLACK)
        screen.blit(score_text, (20, 20))
    else:
        # Draw simple score indicator if font fails
        pygame.draw.rect(screen, constants.BLACK, (20, 20, 100, 30))


def draw_main_menu(screen: pygame.Surface) -> None:
    """
    Draw the main menu UI with 'Start' and 'Exit' buttons.
    """
    if not pygame.font.get_init():
        pygame.font.init()

    title_font = _get_font("arial", 64)

    if title_font:
        title_text = title_font.render("Flappy Bird", True, constants.BLACK)
        title_rect = title_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 140)
        )
        screen.blit(title_text, title_rect)

    buttons = _get_menu_button_rects()
    mouse_pos = pygame.mouse.get_pos()

    for name, rect in buttons.items():
        is_hover = rect.collidepoint(mouse_pos)
        base_color = (70, 130, 180)  # steel blue
        hover_color = (100, 149, 237)  # cornflower blue
        color = hover_color if is_hover else base_color
        pygame.draw.rect(screen, color, rect, border_radius=8)

        button_font = _get_font("arial", 36)

        if button_font:
            label = "Start" if name == "start" else "Exit"
            text_surf = button_font.render(label, True, constants.WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)


def draw_game_over_menu(
    screen: pygame.Surface, score_manager: ScoreManager
) -> None:
    """
    Draw the game over menu with restart and exit options.
    """
    _draw_game_over_overlay(screen)
    _draw_game_over_texts(screen, score_manager)
    _draw_game_over_buttons(screen)


def draw_confirm_exit(screen: pygame.Surface) -> None:
    # modal overlay
    modal = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    modal.set_alpha(180)
    modal.fill((0, 0, 0))
    screen.blit(modal, (0, 0))

    if not pygame.font.get_init():
        pygame.font.init()

    title_font = _get_font("arial", 48)

    if title_font:
        msg = "Are you sure you want to exit?"
        title_text = title_font.render(msg, True, constants.WHITE)
        title_rect = title_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 40)
        )
        screen.blit(title_text, title_rect)

    buttons = _get_confirm_exit_button_rects()
    mouse_pos = pygame.mouse.get_pos()
    for name, rect in buttons.items():
        is_hover = rect.collidepoint(mouse_pos)
        base_color = (178, 34, 34) if name == "yes" else (70, 130, 180)
        hover_color = (220, 20, 60) if name == "yes" else (100, 149, 237)
        color = hover_color if is_hover else base_color
        pygame.draw.rect(screen, color, rect, border_radius=8)

        button_font = _get_font("arial", 36)
        if button_font:
            label = "Yes" if name == "yes" else "No"
            text_surf = button_font.render(label, True, constants.WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)


def draw_window(
    screen: pygame.Surface,
    pipe_manager: PipeManager,
    player_bird: Bird,
    game_state: str,
    score_manager: ScoreManager | None = None,
) -> None:
    """Render the current frame based on game state."""
    screen.fill(constants.WHITE)

    if game_state == "menu":
        draw_main_menu(screen)
    elif game_state == "confirm_exit_menu":
        draw_main_menu(screen)
        draw_confirm_exit(screen)
    else:
        pipe_manager.draw(screen)
        player_bird.draw(screen)

        if game_state == "playing" and score_manager:
            draw_score(screen, score_manager)

        if game_state == "game_over" and score_manager:
            draw_game_over_menu(screen, score_manager)
        elif game_state == "confirm_exit_game_over" and score_manager:
            draw_game_over_menu(screen, score_manager)
            draw_confirm_exit(screen)

    pygame.display.flip()


# Private helpers


def _get_font(font_name: str, size: int) -> pygame.font.Font | None:
    """
    Get a font object with fallback options.
    """
    if not pygame.font.get_init():
        pygame.font.init()

    try:
        return pygame.font.SysFont(font_name, size)
    except Exception:
        pass

    try:
        return pygame.font.Font(None, size)
    except Exception:
        return None


def _draw_game_over_overlay(screen: pygame.Surface) -> None:
    overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(constants.BLACK)
    screen.blit(overlay, (0, 0))


def _draw_game_over_texts(
    screen: pygame.Surface, score_manager: ScoreManager
) -> None:
    font = _get_font("arial", 55)

    if font:
        center_x = constants.SCREEN_WIDTH // 2
        center_y = constants.SCREEN_HEIGHT // 2

        game_over_text: pygame.Surface = font.render("GAME OVER", True, constants.RED)
        text_rect: pygame.Rect = game_over_text.get_rect(
            center=(center_x, center_y - 150)
        )
        screen.blit(game_over_text, text_rect)

        score_text: pygame.Surface = font.render(
            f"Final Score: {score_manager.score}", True, constants.WHITE
        )
        score_rect: pygame.Surface = score_text.get_rect(
            center=(center_x, center_y - 80)
        )
        screen.blit(score_text, score_rect)

        high_score_text: pygame.Surface = font.render(
            f"High Score: {score_manager.high_score}", True, constants.WHITE
        )
        high_score_rect: pygame.Rect = high_score_text.get_rect(
            center=(center_x, center_y - 20)
        )
        screen.blit(high_score_text, high_score_rect)
    else:
        center_x: int = constants.SCREEN_WIDTH // 2
        center_y: int = constants.SCREEN_HEIGHT // 2
        rect_width: int = 300
        rect_height: int = 50

        pygame.draw.rect(
            screen,
            constants.RED,
            (center_x - rect_width // 2, center_y - 200, rect_width, rect_height),
        )
        pygame.draw.rect(
            screen,
            constants.WHITE,
            (center_x - rect_width // 2, center_y - 130, rect_width, rect_height),
        )
        pygame.draw.rect(
            screen,
            constants.WHITE,
            (center_x - rect_width // 2, center_y - 70, rect_width, rect_height),
        )


def _draw_game_over_buttons(screen: pygame.Surface) -> None:
    buttons = _get_game_over_button_rects()
    mouse_position: tuple[int, int] = pygame.mouse.get_pos()

    for name, rect in buttons.items():
        is_hover: bool = rect.collidepoint(mouse_position)
        base_color: tuple[int, int, int] = (70, 130, 180)  # steel blue
        hover_color: tuple[int, int, int] = (100, 149, 237)  # cornflower blue
        color: tuple[int, int, int] = hover_color if is_hover else base_color
        pygame.draw.rect(screen, color, rect, border_radius=8)

        button_font = _get_font("arial", 36)
        if button_font:
            label = "Restart" if name == "restart" else "Exit"
            text_surf = button_font.render(label, True, constants.WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)


def _get_menu_button_rects() -> dict[str, pygame.Rect]:
    """
    Compute rectangles for main menu buttons.
    """
    center_x: int = constants.SCREEN_WIDTH // 2
    total_height: int = constants.BUTTON_HEIGHT * 2 + constants.BUTTON_SPACING
    origin_y: int = constants.SCREEN_HEIGHT // 2 - total_height // 2
    start_button_rect: pygame.Rect = pygame.Rect(
        center_x - constants.BUTTON_WIDTH // 2,
        origin_y,
        constants.BUTTON_WIDTH,
        constants.BUTTON_HEIGHT,
    )
    exit_button_rect: pygame.Rect = pygame.Rect(
        center_x - constants.BUTTON_WIDTH // 2,
        origin_y + constants.BUTTON_HEIGHT + constants.BUTTON_SPACING,
        constants.BUTTON_WIDTH,
        constants.BUTTON_HEIGHT,
    )
    return {"start": start_button_rect, "exit": exit_button_rect}


def _get_game_over_button_rects() -> dict[str, pygame.Rect]:
    """
    Compute rectangles for Game Over buttons (Restart, Exit) with same style as main menu.
    """
    center_x: int = constants.SCREEN_WIDTH // 2
    origin_y: int = constants.SCREEN_HEIGHT // 2 + 30
    restart_rect = pygame.Rect(
        center_x - constants.BUTTON_WIDTH // 2,
        origin_y,
        constants.BUTTON_WIDTH,
        constants.BUTTON_HEIGHT,
    )
    exit_rect = pygame.Rect(
        center_x - constants.BUTTON_WIDTH // 2,
        origin_y + constants.BUTTON_HEIGHT + constants.BUTTON_SPACING,
        constants.BUTTON_WIDTH,
        constants.BUTTON_HEIGHT,
    )
    return {"restart": restart_rect, "exit": exit_rect}


def _get_confirm_exit_button_rects() -> dict[str, pygame.Rect]:
    center_x: int = constants.SCREEN_WIDTH // 2
    origin_y: int = constants.SCREEN_HEIGHT // 2 + 30
    yes_rect = pygame.Rect(
        center_x - constants.BUTTON_WIDTH - constants.BUTTON_SPACING // 2,
        origin_y,
        constants.BUTTON_WIDTH,
        constants.BUTTON_HEIGHT,
    )
    no_rect = pygame.Rect(
        center_x + constants.BUTTON_SPACING // 2,
        origin_y,
        constants.BUTTON_WIDTH,
        constants.BUTTON_HEIGHT,
    )
    return {"yes": yes_rect, "no": no_rect}

