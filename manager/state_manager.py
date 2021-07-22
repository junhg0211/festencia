from typing import Callable

from display import Display
from manager import MouseManager, KeyboardManager
from object import FPSCalculator
from state import Selection
from state.game import Game


class StateManager:
    def __init__(self, display: Display, fps_calculator: FPSCalculator, mouse_manager: MouseManager,
                 keyboard_manager: KeyboardManager, shutdown: Callable):
        self.state = None

        self.display = display
        self.fps_calculator = fps_calculator
        self.mouse_manager = mouse_manager
        self.keyboard_manager = keyboard_manager
        self.shutdown = shutdown

    def state_to(self, state: str, *args):
        """
        When ``state`` is ..., args is ...

        * ``host_game``, [title: str]
        """

        if state == 'title':
            self.state = Selection('title', self.display, self, self.fps_calculator, self.mouse_manager,
                                   self.keyboard_manager, self.shutdown)
        elif state == 'host':
            self.state = Selection('host', self.display, self, self.fps_calculator, self.mouse_manager,
                                   self.keyboard_manager)
        elif state == 'host_game':
            self.state = Game(args[0], self.display, self.mouse_manager, self)

    def set_state(self, state):
        self.state = state
        return self

    def tick(self):
        if self.state:
            self.state.tick()

    def render(self, display: Display):
        if self.state:
            self.state.render(display)
