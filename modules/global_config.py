import enum
from typing import Callable
from abc import ABC, abstractmethod

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))

from . import game

#game window
WIDTH, HEIGHT = 256, 196

SCENARIO = """
|
|
|
|
|
|
|
| 
|
|
|X
|X
|===============
"""

class GameState (enum.IntEnum):
    MENU = 1
    CHAR_SELECT = 2
    GAMEPLAY = 3
    RESULTS = 4
    
class CollisionType(enum.IntEnum):
    PLAYER = 1
    PLATFORM = 2

class HitboxType(enum.IntEnum):
    HURTBOX = 0
    ATTACK = 1 # longo e curto alcance
    SHIELD = 2

class GameObject(ABC):
    @abstractmethod
    def update(self):
        ...
    
    @abstractmethod
    def draw(self):
        ...

    @abstractmethod
    def register(self, space: game.Space, message: Callable[[str, "GameObject"], None]):
        ...