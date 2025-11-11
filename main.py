from __future__ import annotations

import sys
import pygame

import constants
from entities import bird
from managers.game_manager import check_collisions, reset_game
from managers.pipe_manager import PipeManager
from managers.score_manager import ScoreManager


# Game states
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    CONFIRM_EXIT_MENU = "confirm_exit_menu"
    CONFIRM_EXIT_GAME_OVER = "confirm_exit_game_over"


def draw_score(screen: pygame.Surface, score_manager: ScoreManager) -> None:
    """
    Draw the current score in the top left corner.

    Args:
        screen (pygame.Surface): The main display surface.
        score_manager (ScoreManager): The score manager containing current score.
    """
    # Initialize font module if not already done
    if not pygame.font.get_init():
        pygame.font.init()

    try:
        font = pygame.font.SysFont("arial", 36)
    except:
        try:
            font = pygame.font.Font(None, 36)
        except:
            font = None

    if font:
        score_text = font.render(f"Score: {score_manager.score}", True, constants.BLACK)
        screen.blit(score_text, (20, 20))
    else:
        # Draw simple score indicator if font fails
        pygame.draw.rect(screen, constants.BLACK, (20, 20, 100, 30))


def draw_game_over_menu(screen: pygame.Surface, score_manager: ScoreManager) -> None:
    """
    Draw the game over menu with restart and exit options.

    Args:
        screen (pygame.Surface): The main display surface.
        score_manager (ScoreManager): The score manager containing final score.
    """
    # Semi-transparent overlay to dim the background but keep consistency in button style
    overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(constants.BLACK)
    screen.blit(overlay, (0, 0))

    # Initialize font module if not already done
    if not pygame.font.get_init():
        pygame.font.init()

    # Game over text
    try:
        font = pygame.font.SysFont("arial", 55)
    except:
        try:
            font = pygame.font.Font(None, 55)
        except:
            # Fallback: create a simple text surface without custom font
            font = None

    if font:
        game_over_text = font.render("GAME OVER", True, constants.RED)
        text_rect = game_over_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 150)
        )
        screen.blit(game_over_text, text_rect)

        # Final score text
        score_text = font.render(
            f"Final Score: {score_manager.score}", True, constants.WHITE
        )
        score_rect = score_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 80)
        )
        screen.blit(score_text, score_rect)

        # High score text
        high_score_text = font.render(
            f"High Score: {score_manager.high_score}", True, constants.WHITE
        )
        high_score_rect = high_score_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 20)
        )
        screen.blit(high_score_text, high_score_rect)
    else:
        # Draw simple text using basic shapes if font fails
        pygame.draw.rect(
            screen,
            constants.RED,
            (
                constants.SCREEN_WIDTH // 2 - 150,
                constants.SCREEN_HEIGHT // 2 - 200,
                300,
                50,
            ),
        )
        pygame.draw.rect(
            screen,
            constants.WHITE,
            (
                constants.SCREEN_WIDTH // 2 - 150,
                constants.SCREEN_HEIGHT // 2 - 130,
                300,
                50,
            ),
        )
        pygame.draw.rect(
            screen,
            constants.WHITE,
            (
                constants.SCREEN_WIDTH // 2 - 150,
                constants.SCREEN_HEIGHT // 2 - 70,
                300,
                50,
            ),
        )

    # Buttons (consistent with main menu style)
    buttons = _get_game_over_button_rects()
    mouse_pos = pygame.mouse.get_pos()

    for name, rect in buttons.items():
        is_hover = rect.collidepoint(mouse_pos)
        base_color = (70, 130, 180)  # steel blue
        hover_color = (100, 149, 237)  # cornflower blue
        color = hover_color if is_hover else base_color
        pygame.draw.rect(screen, color, rect, border_radius=8)

        # Button text
        try:
            btn_font = pygame.font.SysFont("arial", 36)
        except:
            try:
                btn_font = pygame.font.Font(None, 36)
            except:
                btn_font = None

        if btn_font:
            label = "Restart" if name == "restart" else "Exit"
            text_surf = btn_font.render(label, True, constants.WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)


def handle_game_over_input(keys_pressed: pygame.key.ScancodeWrapper) -> str:
    """
    Handle input during game over menu.

    Args:
        keys_pressed (pygame.key.ScancodeWrapper): Pressed state of all keys.

    Returns:
        str: Action to take - "restart", "exit", or "none"
    """
    if keys_pressed[pygame.K_r]:
        return "restart"
    elif keys_pressed[pygame.K_RETURN] or keys_pressed[pygame.K_SPACE]:
        return "restart"
    elif keys_pressed[pygame.K_ESCAPE]:
        return "exit"
    return "none"


def _get_menu_button_rects() -> dict[str, pygame.Rect]:
    """
    Compute rectangles for main menu buttons.

    Returns:
        dict[str, pygame.Rect]: Mapping of button name to its rectangle.
    """
    center_x: int = constants.SCREEN_WIDTH // 2
    start_y: int = constants.SCREEN_HEIGHT // 2 - constants.BUTTON_HEIGHT // 2
    total_height: int = constants.BUTTON_HEIGHT * 2 + constants.BUTTON_SPACING
    origin_y: int = constants.SCREEN_HEIGHT // 2 - total_height // 2
    start_button_rect = pygame.Rect(
        center_x - constants.BUTTON_WIDTH // 2,
        origin_y,
        constants.BUTTON_WIDTH,
        constants.BUTTON_HEIGHT,
    )
    exit_button_rect = pygame.Rect(
        center_x - constants.BUTTON_WIDTH // 2,
        origin_y + constants.BUTTON_HEIGHT + constants.BUTTON_SPACING,
        constants.BUTTON_WIDTH,
        constants.BUTTON_HEIGHT,
    )
    return {"start": start_button_rect, "exit": exit_button_rect}


def draw_main_menu(screen: pygame.Surface) -> None:
    """
    Draw the main menu UI with 'Start' and 'Exit' buttons.
    """
    # Title
    if not pygame.font.get_init():
        pygame.font.init()

    try:
        title_font = pygame.font.SysFont("arial", 64)
    except:
        try:
            title_font = pygame.font.Font(None, 64)
        except:
            title_font = None

    if title_font:
        title_text = title_font.render("Flappy Bird", True, constants.BLACK)
        title_rect = title_text.get_rect(
            center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2 - 140)
        )
        screen.blit(title_text, title_rect)

    # Buttons
    buttons = _get_menu_button_rects()
    mouse_pos = pygame.mouse.get_pos()

    for name, rect in buttons.items():
        is_hover = rect.collidepoint(mouse_pos)
        base_color = (70, 130, 180)  # steel blue
        hover_color = (100, 149, 237)  # cornflower blue
        color = hover_color if is_hover else base_color
        pygame.draw.rect(screen, color, rect, border_radius=8)

        # Button text
        try:
            btn_font = pygame.font.SysFont("arial", 36)
        except:
            try:
                btn_font = pygame.font.Font(None, 36)
            except:
                btn_font = None

        if btn_font:
            label = "Start" if name == "start" else "Exit"
            text_surf = btn_font.render(label, True, constants.WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)


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
        center_x + constants.BUTTON_SPACING // 2, origin_y, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT
    )
    return {"yes": yes_rect, "no": no_rect}


def draw_confirm_exit(screen: pygame.Surface) -> None:
    # modal overlay
    modal = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    modal.set_alpha(180)
    modal.fill((0, 0, 0))
    screen.blit(modal, (0, 0))

    if not pygame.font.get_init():
        pygame.font.init()

    try:
        title_font = pygame.font.SysFont("arial", 48)
    except:
        try:
            title_font = pygame.font.Font(None, 48)
        except:
            title_font = None

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

        try:
            btn_font = pygame.font.SysFont("arial", 36)
        except:
            try:
                btn_font = pygame.font.Font(None, 36)
            except:
                btn_font = None
        if btn_font:
            label = "Yes" if name == "yes" else "No"
            text_surf = btn_font.render(label, True, constants.WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)


def handle_main_menu_input(events: list[pygame.event.Event]) -> str:
    """
    Handle input for the main menu.

    Returns:
        str: "start", "exit", or "none"
    """
    buttons = _get_menu_button_rects()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttons["start"].collidepoint(event.pos):
                return "start"
            if buttons["exit"].collidepoint(event.pos):
                return "exit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return "start"
            if event.key == pygame.K_ESCAPE:
                return "exit"
    return "none"


def _get_game_over_button_rects() -> dict[str, pygame.Rect]:
    """
    Compute rectangles for Game Over buttons (Restart, Exit) with same style as main menu.
    """
    center_x: int = constants.SCREEN_WIDTH // 2
    # Place buttons below the score block
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


def handle_game_over_input_events(events: list[pygame.event.Event]) -> str:
    """
    Handle mouse/keyboard events for Game Over menu (clickable buttons).
    """
    buttons = _get_game_over_button_rects()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttons["restart"].collidepoint(event.pos):
                return "restart"
            if buttons["exit"].collidepoint(event.pos):
                return "exit"
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_r):
                return "restart"
            if event.key == pygame.K_ESCAPE:
                return "exit"
    return "none"


def handle_confirm_exit_input(events: list[pygame.event.Event]) -> str:
    """
    Handle input for the confirm-exit modal.
    Returns: "yes", "no", or "none"
    """
    buttons = _get_confirm_exit_button_rects()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if buttons["yes"].collidepoint(event.pos):
                return "yes"
            if buttons["no"].collidepoint(event.pos):
                return "no"
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_y, pygame.K_RETURN):
                return "yes"
            if event.key in (pygame.K_n, pygame.K_ESCAPE):
                return "no"
    return "none"


def draw_window(
    screen: pygame.Surface,
    pipe_manager: PipeManager,
    game_state: str = GameState.PLAYING,
    score_manager: ScoreManager | None = None,
) -> None:
    """Render the current frame based on game state."""
    screen.fill(constants.WHITE)

    if game_state == GameState.MENU:
        draw_main_menu(screen)
    elif game_state == GameState.CONFIRM_EXIT_MENU:
        draw_main_menu(screen)
        draw_confirm_exit(screen)
    else:
        pipe_manager.draw(screen)
        bird.draw(screen)

        if game_state == GameState.PLAYING and score_manager:
            draw_score(screen, score_manager)

        if game_state == GameState.GAME_OVER and score_manager:
            draw_game_over_menu(screen, score_manager)
        elif game_state == GameState.CONFIRM_EXIT_GAME_OVER and score_manager:
            draw_game_over_menu(screen, score_manager)
            draw_confirm_exit(screen)

    pygame.display.flip()



def handle_events(events: list[pygame.event.Event]) -> bool:
    """Return False if a QUIT event is processed."""
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True



def handle_keys_pressed_events(keys_pressed: pygame.key.ScancodeWrapper) -> None:
    """Handle per-frame keyboard state (escape to quit, space to jump)."""
    if keys_pressed[pygame.K_ESCAPE]:
        sys.exit(1)

    if keys_pressed[pygame.K_SPACE]:
        bird.jump()


def main() -> None:
    """
    Initialize and run the main game loop for a minimal Flappy Bird.

    Sets up the display window and FPS clock, creates the bird and pipe manager,
    then runs the main loop:
    - Cap frame rate to `FPS`.
    - Fetch and handle events (terminate on quit).
    - Update bird motion and pipe positions.
    - Handle key states (ESC to exit, SPACE to jump).
    - Render the current frame.

    The loop continues until exit; then the display module is shut down.
    """
    pygame.display.init()
    pygame.font.init()  # Initialize font module

    running: bool = True

    screen: pygame.Surface = pygame.display.set_mode(
        [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    )
    pygame.display.set_caption("Flappy Bird")

    clock: pygame.time.Clock = pygame.time.Clock()

    BIRD_SIZE: int = 50

    # Bird surface
    bird_surface: pygame.Surface = pygame.Surface([BIRD_SIZE, BIRD_SIZE])
    bird_surface.fill(constants.BLACK)
    pygame.draw.circle(
        bird_surface, constants.GREEN, [BIRD_SIZE // 2, BIRD_SIZE // 2], 20
    )

    pipe_manager: PipeManager = PipeManager(
        gap=200, pipe_width=80, speed=4, spawn_distance=300
    )

    # Initialize ScoreManager
    score_manager: ScoreManager = ScoreManager()

    # Initialize Bird object
    global bird
    bird = bird.Bird(70, 90, bird_surface)

    # Game state
    game_state = GameState.MENU

    # Track last pipe passed for scoring
    last_pipe_passed = None

    # Game loop
    while running:
        # Set the FPS to 60
        clock.tick(constants.FPS)

        # Get events
        events: list[pygame.event.Event] = pygame.event.get()

        # Handle events
        running = handle_events(events)

        # Get keys pressed
        keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        if game_state == GameState.MENU:
            # Handle input in main menu
            action = handle_main_menu_input(events)
            if action == "start":
                reset_game(bird, pipe_manager, score_manager)
                game_state = GameState.PLAYING
                last_pipe_passed = None
            elif action == "exit":
                game_state = GameState.CONFIRM_EXIT_MENU

        elif game_state == GameState.CONFIRM_EXIT_MENU:
            confirm = handle_confirm_exit_input(events)
            if confirm == "yes":
                running = False
            elif confirm == "no":
                game_state = GameState.MENU

        elif game_state == GameState.PLAYING:
            # Movement
            bird.movement()

            pipe_manager.update()

            # Handle keys pressed
            handle_keys_pressed_events(keys_pressed)

            # Check for scoring (when bird passes a pipe)
            for pipe_pair in pipe_manager._PipeManager__pipes:
                if (
                    pipe_pair.top_pipe.rect.right < bird.rect.left
                    and pipe_pair != last_pipe_passed
                ):
                    score_manager.increment_score()
                    last_pipe_passed = pipe_pair

            # Check for collisions
            if check_collisions(bird, pipe_manager):
                score_manager.update_high_score()
                game_state = GameState.GAME_OVER

        elif game_state == GameState.GAME_OVER:
            # Handle input in game over menu (mouse + keyboard)
            action = handle_game_over_input_events(events)
            if action == "none":
                # fallback to continuous key state for convenience
                action = handle_game_over_input(keys_pressed)
            if action == "restart":
                reset_game(bird, pipe_manager, score_manager)
                game_state = GameState.PLAYING
                last_pipe_passed = None
            elif action == "exit":
                game_state = GameState.CONFIRM_EXIT_GAME_OVER

        elif game_state == GameState.CONFIRM_EXIT_GAME_OVER:
            confirm = handle_confirm_exit_input(events)
            if confirm == "yes":
                running = False
            elif confirm == "no":
                game_state = GameState.GAME_OVER

        # Draw window
        draw_window(screen, pipe_manager, game_state, score_manager)

    pygame.display.quit()


if __name__ == "__main__":
    main()
