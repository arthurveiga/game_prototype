import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.path.pardir))

from . import global_config as config
from . import player
import pyxel
from easymunk import Vec2d, Arbiter, CircleBody, Space, march_string
from easymunk import pyxel as phys

class Game:
    # Cores
    
    # Outras propriedades
    CAMERA_TOL = Vec2d(config.WIDTH / 2 - 64, config.HEIGHT / 2 - 48)
    N_ENEMIES = 20

    def __init__(self, scenario=config.SCENARIO):
        self.paused = False
        self.camera = phys.Camera(flip_y=True)
        self.space = phys.space(
            gravity=(0, -25),
            wireframe=True,
            camera=self.camera,
            elasticity=1.0,
        )

        # Inicializa o jogo
        self.state = config.GameState.GAMEPLAY
        pyxel.load("assets.pyxres")

        pyxel.cls(pyxel.COLOR_LIGHTBLUE)

        # Cria jogador
        self.player = player.Player(50, 50)
        self.player.register(self.space, self.message)

        # Cria chão
        f = phys.rect(0, 0, 1000, 48, body_type="static")

        # Cria margens
        phys.margin(0, 0, 1000, config.HEIGHT)

    def message(self, msg, sender):
        fn = getattr(self, f'handle_{msg}', None)
        if fn is None:
            print(f'Mensagem desconhecida: "{msg} ({sender})')
        else:
            fn(sender)

    def draw(self):
        pyxel.cls(0)
        for body in self.space.bodies:
            if isinstance(body, (player.Player)):
                body.draw(self.camera)
            else:
                self.camera.draw(body)

         # Desenha texto informativo
        pyxel.text(5, 5, "Setas para controlar a bola (bola tem 3 pulos)\nR para resetar", pyxel.COLOR_BLACK)
        info_text = "Posicao: (" + str(round(self.player.body.position[0], 3)) + ", " + str(round(self.player.body.position[1], 3)) + ")\n" +                    "Velocidade: (" + str(round(self.player.body.velocity[0], 3)) + ", " + str(round(self.player.body.velocity[1], 3)) + ")\n" + "Pulos Restantes: " + str(self.remaining_jumps)
        pyxel.text(5, 30, info_text, pyxel.COLOR_BLACK)

    def update(self):

        if (pyxel.btnp(pyxel.KEY_P)):
            self.paused = False if self.paused else True

        self.space.step(1 / 30, 2)
        if not self.paused:
            self.player.update()
        self.camera.follow(self.player.position, tol=self.CAMERA_TOL)


pyxel.init(config.WIDTH, config.HEIGHT)
pyxel.mouse(True)
game = Game()
pyxel.run(game.update, game.draw)
