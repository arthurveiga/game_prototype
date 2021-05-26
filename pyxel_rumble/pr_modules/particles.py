import random
from random import random
import pyxel
from .anim_dog_moveset import *
from .anim_rabbit_moveset import *

class Particles:
    def __init__ (self, space):
        self.particles = []
        self.space = space
        self.duration = 0

    def draw (self, camera=pyxel, color=pyxel.COLOR_RED):
        for p in self.particles:
            x, y = p.position
            camera.pset(x, y, pyxel.COLOR_RED)

    def update(self):
        for p in self.particles.copy():
            p. velocity = p.velocity.rotated(random.uniform(-5,5))
            p.duration -= 1
            if p.duration <= 0:
                self.particles.remove(p)

    def emmit(self, position, velocity):
        p= self.space.create_body(
            mass = 0.1, 
            moment= float('inf'), 
            position = position, 
            velocity = velocity,
            duration = 0
        )
        p.duration = random.uniform(75, 111)
        self.particles.append(p)

    # def get_color(self, t):
    #     if t > 95:
    #         return pyxel.COLOR_GRAY
    #     elif t > 40:
    #         return pyxel.COLOR_BLACK
