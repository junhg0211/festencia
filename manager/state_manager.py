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

        * ``host_game``, [title: str, host: str, port: int, name: str]
        * ``error``, [content: str]
        * ``join_game``, [host: str, port: int, name: str]
        """

        if state == 'title':
            self.state = Selection(Selection.TITLE, self.display, self, self.fps_calculator, self.mouse_manager,
                                   self.keyboard_manager, self.shutdown)
        elif state == 'host':
            self.state = Selection(Selection.HOST, self.display, self, self.fps_calculator, self.mouse_manager,
                                   self.keyboard_manager)
        elif state == 'host_game':
            self.state = Game(Game.HOST, self.display, self.mouse_manager, self,
                              title=args[0], host=args[1], port=args[2], name=args[3])
        elif state == 'error':
            self.state = Selection(Selection.ERROR, self.display, self, self.fps_calculator, self.mouse_manager,
                                   self.keyboard_manager, args[0])
        elif state == 'join':
            self.state = Selection(Selection.JOIN, self.display, self, self.fps_calculator, self.mouse_manager,
                                   self.keyboard_manager)
        elif state == 'join_game':
            state = Game(Game.JOIN, self.display, self.mouse_manager, self, host=args[0], port=args[1], name=args[2])
            if not (isinstance(self.state, Selection) and self.state.mode == Selection.ERROR):
                # Handling the joining exceptions.
                # When connection error occured while trying to connect to the server, this will not be held.
                self.state = state

    def set_state(self, state):
        self.state = state
        return self

    def tick(self):
        if self.state:
            self.state.tick()

    def render(self, display: Display):
        if self.state:
            self.state.render(display)
