import pyxel
from .anim_dog_moveset import *
from .anim_rabbit_moveset import *

class Particles:
    def __init__ (self, space):
        self.particles = []
        self.space = space

    def draw (self, camera=pyxel):
        for p in self.particles:
            x, y = p.position
            camera.pset(x, y, pyxel.COLOR_WHITE)

    def update(self):
        ...

    def emmit(self, position, velocity):
        p= self.space.create_body(
            mass = 0.1, moment= float('inf'), position = position, velocity = velocity
        )
        self.particles.append(p)
