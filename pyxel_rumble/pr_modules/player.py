import pyxel
from easymunk import Vec2d, CircleBody, Arbiter
from .global_config import GameObject, CollisionType, WIDTH, HEIGHT

class Player (GameObject, CircleBody):
    SPEED = 90
    JUMP_SPEED = 120
    COLOR = pyxel.COLOR_RED
    NUMBER_JUMPS = 2

    def __init__(self, x, y):
        super().__init__(
            radius=4,
            position=(x, y),
            elasticity=0.1,
            collision_type=CollisionType.PLAYER,
        )
        self.can_jump = False
        self.remaining_jumps = self.NUMBER_JUMPS

    def update(self):
        v = self.velocity
        mass = self.mass
        F = mass * 200
        self.force += Vec2d(0, -mass * 200)

        # Resetar o jogador
        if pyxel.btnp(pyxel.KEY_R):
            self.body.position = (WIDTH/2, HEIGHT/2)
            v = Vec2d(0,0)
        
        # Controles
        if pyxel.btn(pyxel.KEY_LEFT):
            if self.can_jump and self.remaining_jumps > 0:
                v = Vec2d(-self.SPEED, v.y)
            elif v.x <= 0:
                v = Vec2d(-self.SPEED / 2, v.y)
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if self.can_jump and self.remaining_jumps > 0:
                v = Vec2d(+self.SPEED, v.y)
            elif v.x <= 0:
                v = Vec2d(+self.SPEED / 2, v.y)
        else:
            r = 0.5 if self.can_jump else 1.0
            v = Vec2d(v.x * r, v.y)

        if (pyxel.btnp(pyxel.KEY_UP)
            and self.can_jump and self.remaining_jumps > 0 ):
            v = Vec2d(v.x, self.JUMP_SPEED)
            self.remaining_jumps-=1
        elif(pyxel.btnp(pyxel.KEY_DOWN)
            and self.remaining_jumps < self.NUMBER_JUMPS):
            v = Vec2d(v.x, -self.JUMP_SPEED)

        self.velocity = v

    def draw(self, camera=pyxel):
        x, y, _right, _top = self.bb
        sign = 1 if self.velocity.x >= 0 else -1

        idx = int(self.position.x / 2) % 6
        u = 16 * idx
        camera.blt(x, y, 0, u, 0, sign * 16, 16, pyxel.COLOR_GREEN)

    def register(self, space, message):
        space.add(self)

        @space.post_solve_collision(CollisionType.PLAYER, ...)
        def _col_start(arb: Arbiter):
            n = arb.normal_from(self)
            self.can_jump = n.y <= -0.5
            self.remaining_jumps = self.NUMBER_JUMPS

        @space.separate_collision(CollisionType.PLAYER, ...)
        def _col_end(arb: Arbiter):
            self.can_jump = False if self.remaining_jumps == 0 else True