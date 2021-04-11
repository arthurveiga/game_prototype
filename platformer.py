import pyxel
from pymunk import Space, Body, Circle, Segment, ShapeFilter


class Game:

    def __init__(self, fps=30, width=256, height=196, speed=50):
        self.fps = fps
        self.width = width
        self.height = height
        self.paused = False
        self.border_color = pyxel.COLOR_RED

        self.space = Space()
        self.space.gravity = (0, 130)
        
        # Adiciona plataforma
        static_platform = self.space.static_body
        self.platform_a = (self.width/5, self.height - 20) 
        self.platform_b = (4*self.width/5, self.height - 20)
        self.platform = Segment(static_platform, self.platform_a, self.platform_b, 5)
        self.platform.elasticity = 0.95
        self.platform.friction = 1.0
        self.space.add(self.platform)

        # Adiciona player
        body = Body(mass=1, moment=1)
        self.player = Circle(body, 5)
        self.player.elasticity = 0.2
        body.position = (self.width/2, self.height/2)
        self.space.add(body, self.player)
        self.remaining_jumps = 3

    def update(self):
        if not self.paused:
            dt = 1 / self.fps
            self.space.step(dt)
            
            # Resetar o jogador
            if pyxel.btnp(pyxel.KEY_R):
                self.player.body.position = (self.width/2, self.height/2)
                self.player.body.velocity = (0, 0)
            # Controles
            if pyxel.btn(pyxel.KEY_LEFT):
                self.player.body.velocity = (-50, self.player.body.velocity.y)
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.player.body.velocity = (50, self.player.body.velocity.y)

            if pyxel.btnp(pyxel.KEY_UP) and self.remaining_jumps > 0:
                self.remaining_jumps -= 1
                self.player.body.velocity = (self.player.body.velocity.x, -50)
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.player.body.velocity = (self.player.body.velocity.x, 80)
            
            # Parar o jogador
            if pyxel.btnr(pyxel.KEY_LEFT):
                self.player.body.velocity = (0, self.player.body.velocity.y)
            if pyxel.btnr(pyxel.KEY_RIGHT):
                self.player.body.velocity = (0, self.player.body.velocity.y)

            # Restaurar pulos
            pos = self.player.body.position
            lst = self.space.point_query(pos, int(self.player.radius+1), ShapeFilter())
            lst.sort(key=lambda i: i.distance)
            if lst and len(lst) > 1:
                if self.player.body.position[1] >= lst[1].shape.body.position[1] and self.remaining_jumps < 2:
                    self.remaining_jumps = 3
    


    def draw(self):
        pyxel.cls(pyxel.COLOR_LIGHTBLUE)

        # Desenha elementos do espaço
        for shape in self.space.shapes:
            ## Todos os círculos (player)
            if isinstance(shape, Circle):
                circle: Circle = shape
                r = circle.radius
                x, y = circle.body.position
                pyxel.circ(x, y, r, pyxel.COLOR_BLACK)
            ## Plataforma
            if isinstance(shape, Segment):
                segment: Segment = shape
                for i in range(-4, 4, 1):
                    pyxel.line(self.platform_a[0], self.platform_a[1] + i, 
                                self.platform_b[0], self.platform_b[1] + i,
                                pyxel.COLOR_BLACK)
        
        # Desenha texto informativo
        pyxel.text(5, 5, "Setas para controlar a bola (bola tem 3 pulos)\nR para resetar", pyxel.COLOR_BLACK)
        info_text = "Posicao: (" + str(round(self.player.body.position[0], 3)) + ", " + str(round(self.player.body.position[1], 3)) + ")\n" +                    "Velocidade: (" + str(round(self.player.body.velocity[0], 3)) + ", " + str(round(self.player.body.velocity[1], 3)) + ")\n" + "Pulos Restantes: " + str(self.remaining_jumps)
        pyxel.text(5, 30, info_text, pyxel.COLOR_BLACK)

    def run(self):
        pyxel.init(self.width, self.height, caption="Platformer", fps=self.fps) 
        pyxel.run(self.update, self.draw)

game = Game()
game.run()