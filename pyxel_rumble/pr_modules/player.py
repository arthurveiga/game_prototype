import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))

from . import global_config as config
from . import game


class Player (config.GameObject, game.CircleBody):
    SPEED = 90
    JUMP_SPEED = 120

    def __init__(self, x, y):
        super().__init__(
            radius=4,
            position=(x, y),
            elasticity=0.2,
            collision_type=config.CollisionType.PLAYER,
        )
        self.can_jump = False
        self.remaining_jumps = 3

    def update(self):
        v = self.velocity
        mass = self.mass
        F = mass * 200
        self.force += game.Vec2d(0, -mass * 200)

        # Resetar o jogador
        if game.pyxel.btnp(game.pyxel.KEY_R):
            self.player.body.position = (self.width/2, self.height/2)
            v = game.Vec2d(0,0)
        
        if game.pyxel.btn(game.pyxel.KEY_LEFT):
            if self.can_jump and self.remaining_jumps > 0:
                v = game.Vec2d(-self.SPEED, v.y)
            elif v.x <= 0:
                v = game.Vec2d(-self.SPEED / 2, v.y)
        elif game.pyxel.btn(game.pyxel.KEY_RIGHT):
            if self.can_jump and self.remaining_jumps > 0:
                v = game.Vec2d(+self.SPEED, v.y)
            elif v.x <= 0:
                v = game.Vec2d(+self.SPEED / 2, v.y)
        else:
            r = 0.5 if self.can_jump else 1.0
            v = game.Vec2d(v.x * r, v.y)

        if (game.pyxel.btnp(game.pyxel.KEY_UP)
            and self.can_jump and self.remaining_jumps > 0 ):
            v = game.Vec2d(v.x, self.JUMP_SPEED)

        self.velocity = v

    def draw(self, camera=game.pyxel):
        x, y, _right, _top = self.bb
        sign = 1 if self.velocity.x >= 0 else -1

        idx = int(self.position.x / 2) % 3
        u = 8 * idx
        camera.blt(x, y, 0, u, 0, sign * 8, 8, game.pyxel.COLOR_YELLOW)

    def register(self, space, message):
        space.add(self)

        @space.post_solve_collision(config.CollisionType.PLAYER, ...)
        def _col_start(arb: game.Arbiter):
            n = arb.normal_from(self)
            self.can_jump = n.y <= -0.5
            self.remaining_jumps = 3

        @space.separate_collision(config.CollisionType.PLAYER, ...)
        def _col_end(arb: game.Arbiter):
            self.can_jump = False if self.remaining_jumps == 0 else True
