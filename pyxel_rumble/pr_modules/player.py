import pyxel
import random
from easymunk import Vec2d, CircleBody, Arbiter
from .global_config import GameObject, CollisionType, WIDTH, HEIGHT, FPS

class Player (GameObject, CircleBody):
    SPEED = 80
    JUMP_SPEED = 120
    COLOR = pyxel.COLOR_RED
    NUMBER_JUMPS = 2

    def __init__(self, x, y):
        super().__init__(
            radius=4,
            position=(x, y),
            elasticity=0.0,
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
        # u altera horizontalmente a posição nos assets, v altera verticalmente

        is_moving = False if ((abs(round(self.velocity.x, 3)) == 0) and abs(round(self.velocity.y, 3) == 0)) else True

        rise_threshold = 0.5
        fall_threshold = -0.01
        is_jumping = True if (round(self.velocity.y, 3) >= rise_threshold)  else False
        
        is_in_the_air = True if (round(self.velocity.y, 3) < rise_threshold and
                                 round(self.velocity.y, 3) >= fall_threshold)  else False
        is_falling = True if (round(self.velocity.y, 3) < fall_threshold)  else False

        is_walking = True if (abs(round(self.velocity.x, 3)) > 0 and 
                             (abs(round(self.velocity.y, 3)) == 0) and 
                             (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_RIGHT))) else False
        
        # ficar parado (idle)

        if (is_moving == False):
            # numero de frames contados de todas as animações de idle
            abana = [0 for _ in range(0, 10, 1)]
            abana_pisca = [1 for _ in range(0, 10, 1)]
            pisca = [2 for _ in range(0, 9, 1)]
            parado = [-1 for _ in range(0, 20, 1)]
            # sequência pré-definida
            anim = abana + parado + pisca + parado + abana + abana_pisca
            anim_counter = int(pyxel.frame_count) % len(anim)

            #animação
            idle_anim_selected = anim[anim_counter]
            if (idle_anim_selected in [0, 1]):
                # abana rabo (0), abana rabo e pisca (1)
                idx = int(pyxel.frame_count//2) % 6
                u = 16 * idx
                v = 16 * idle_anim_selected
                camera.blt(x, y, 0, u, v, sign * 16, 16, pyxel.COLOR_GREEN)
            elif (idle_anim_selected == 2):
                # só pisca o olho (2)
                idx = int(pyxel.frame_count//3) % 3
                u = 16 * idx
                v = 16 * idle_anim_selected
                camera.blt(x, y, 0, u, v, sign * 16, 16, pyxel.COLOR_GREEN)
            elif (idle_anim_selected == -1):
                # parado (-1)
                camera.blt(x, y, 0, 0, 0, sign * 16, 16, pyxel.COLOR_GREEN)
            else:
                pass
                
        else:
            if(is_walking):
                # numero de frames contados de todas as animações de andar
                anda = [3 for _ in range(0, 8, 1)]
                # sequência pré-definida
                anim = anda
                anim_counter = int(pyxel.frame_count) % len(anim)
                
                # andando (3)
                walk_anim_selected = anim[anim_counter]
                idx = int(pyxel.frame_count//2) % 5
                u = 16 * idx
                v = 16 * walk_anim_selected
                camera.blt(x, y, 0, u, v, sign * 16, 16, pyxel.COLOR_GREEN)

            elif(is_jumping):
                jump_anim_selected = 4
                idx = 0
                u = 16 * idx
                v = 16 * jump_anim_selected
                camera.blt(x, y, 0, u, v, sign * 16, 16, pyxel.COLOR_GREEN)
                
            elif(is_in_the_air):
                jump_anim_selected = 4
                idx = 1
                u = 16 * idx
                v = 16 * jump_anim_selected
                camera.blt(x, y, 0, u, v, sign * 16, 16, pyxel.COLOR_GREEN)

            elif(is_falling):
                jump_anim_selected = 4
                idx = 2
                u = 16 * idx
                v = 16 * jump_anim_selected
                camera.blt(x, y, 0, u, v, sign * 16, 16, pyxel.COLOR_GREEN)

            else:
                pass

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