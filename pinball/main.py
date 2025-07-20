"""Simple pinball game using pygame.

This module defines a minimal pinball implementation with a ball,
flippers and basic scoring. The physics are intentionally simplified so
that the logic can be tested without a display.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from typing import Tuple

try:
    import pygame
except ModuleNotFoundError:  # pragma: no cover - pygame might not be installed during tests
    pygame = None

# Game constants
WIDTH, HEIGHT = 640, 480
GRAVITY = 400  # pixels per second squared
FPS = 60
BALL_RADIUS = 8


@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float


def update_ball(ball: Ball, dt: float) -> Ball:
    """Update ball position applying gravity.

    Parameters
    ----------
    ball:
        The ball instance to update. Modified in place.
    dt:
        Delta time in seconds.
    Returns
    -------
    Ball
        The updated ball for convenience.
    """
    ball.vy += GRAVITY * dt
    ball.x += ball.vx * dt
    ball.y += ball.vy * dt
    return ball


def reset_ball() -> Ball:
    """Return a ball positioned in the middle of the screen."""
    return Ball(WIDTH / 2, HEIGHT / 4, 0, 0)


class Flipper:
    """Simple vertical flipper controlled by a keyboard key."""

    def __init__(self, x: int, key: int) -> None:
        self.rect = pygame.Rect(x, HEIGHT - 40, 60, 10)
        self.key = key
        self.speed = 350
        self.default_y = self.rect.y

    def update(self, dt: float, keys: Tuple[bool, ...]) -> None:
        if keys[self.key]:
            self.rect.y = max(self.default_y - 20, self.rect.y - self.speed * dt)
        else:
            self.rect.y = min(self.default_y, self.rect.y + self.speed * dt)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (200, 0, 0), self.rect)


class Game:
    def __init__(self) -> None:
        if pygame is None:
            raise RuntimeError("pygame is required to run the game")
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pinball")
        self.clock = pygame.time.Clock()

        self.ball = reset_ball()
        self.left_flipper = Flipper(80, pygame.K_LEFT)
        self.right_flipper = Flipper(WIDTH - 140, pygame.K_RIGHT)
        self.score = 0

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.restart()
        return True

    def restart(self) -> None:
        self.ball = reset_ball()
        self.score = 0

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.left_flipper.update(dt, keys)
        self.right_flipper.update(dt, keys)
        update_ball(self.ball, dt)

        # Simple wall collisions
        if self.ball.x - BALL_RADIUS < 0 or self.ball.x + BALL_RADIUS > WIDTH:
            self.ball.vx *= -1
        if self.ball.y - BALL_RADIUS < 0:
            self.ball.vy *= -1
            self.score += 10
        if self.ball.y > HEIGHT:
            self.restart()

        # Flipper collisions
        for flipper in (self.left_flipper, self.right_flipper):
            if flipper.rect.collidepoint(self.ball.x, self.ball.y + BALL_RADIUS):
                self.ball.vy = -abs(self.ball.vy)
                self.score += 1

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, (255, 255, 255), (int(self.ball.x), int(self.ball.y)), BALL_RADIUS)
        self.left_flipper.draw(self.screen)
        self.right_flipper.draw(self.screen)
        font = pygame.font.SysFont(None, 24)
        score_surf = font.render(f"Score: {self.score}", True, (255, 255, 0))
        self.screen.blit(score_surf, (10, 10))
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()


def main() -> None:
    if pygame is None:
        sys.stderr.write("pygame is not available.\n")
        return
    Game().run()


if __name__ == "__main__":
    main()
