from const import PRETENDARD_BOLD, BLACK
from display import Display
from manager import MouseManager
from object import Text
from object.piste import Piste
from state import State
from util import Face


class Game(State):
    def __init__(self, title: str, display: Display, mouse_manager: MouseManager, state_manager):
        super().__init__()

        self.display = display
        self.mouse_manager = mouse_manager
        self.state_manager = state_manager

        self.piste = Piste('SCH JEON', 'NEO S.E.H. MINIC IV', display)
        self.object_manager.add(self.piste)

        title_face = Face(PRETENDARD_BOLD, 24, BLACK)
        self.title = Text(title, title_face, y=10).center_x(self.display)
        self.object_manager.add(self.title)

    def tick(self):
        super().tick()

        if self.mouse_manager.left_start:
            self.piste.dualcircles.random_pos(self.display)

    def render(self, display: Display):
        super().render(display)
