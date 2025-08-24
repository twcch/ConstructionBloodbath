from __future__ import annotations
from abc import ABC, abstractmethod
from pygame.math import Vector2 as vector
from typing import Sequence, Callable


class ShootBehavior(ABC):
    """Interface for different shooting strategies."""
    def __init__(self, shoot_cb: Callable):
        self._shoot_cb = shoot_cb

    @abstractmethod
    def shoot(self, owner, direction: vector):
        ...


class SingleShot(ShootBehavior):
    def shoot(self, owner, direction: vector):
        pos = owner.rect.center + direction * 80
        y_offset = vector(0, -16) if not getattr(owner, 'duck', False) else vector(0, 10)
        self._shoot_cb(pos + y_offset, direction, owner)


class SpreadShot(ShootBehavior):
    def __init__(self, shoot_cb: Callable, angles: Sequence[float]):
        super().__init__(shoot_cb)
        self.angles = angles

    def shoot(self, owner, direction: vector):
        base_angle = 0 if direction.x >= 0 else 180
        # naive spread adjusting x direction only (placeholder)
        for delta in self.angles:
            dir_vec = vector(1, 0)
            if direction.x < 0:
                dir_vec.x = -1
            self._shoot_cb(owner.rect.center + dir_vec * 80, dir_vec, owner)
