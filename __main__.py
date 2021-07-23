from pygame import init as pygame_init
from pygame.event import get as event_get

from const import CAPTION, WHITE
from display import Display
from handler import Quit
from manager import ObjectManager, HandlerManager, MouseManager, KeyboardManager, StateManager
from object import FPSCalculator
from state import Selection

pygame_init()


class Main:
    def __init__(self):
        self.display = Display(1920, 1080, CAPTION)

        self.running = True

        self.mouse_manager = MouseManager()
        keyboard_manager = KeyboardManager()
        self.handler_manager = HandlerManager() \
            .add(Quit(self.shutdown)) \
            .add(self.mouse_manager) \
            .add(keyboard_manager)
        fps_calculator = FPSCalculator()
        self.object_manager = ObjectManager() \
            .add(fps_calculator)
        self.state_manager = StateManager(self.display, fps_calculator, self.mouse_manager, keyboard_manager,
                                          self.shutdown)
        self.state_manager.set_state(
            Selection(Selection.TITLE, self.display, self.state_manager, fps_calculator, self.mouse_manager,
                      keyboard_manager, self.shutdown))

    def shutdown(self):
        self.running = False

    def handle(self):
        for event in event_get():
            self.handler_manager.handle(event)

    def tick(self):
        self.state_manager.tick()
        self.object_manager.tick()

        self.mouse_manager.tick()

    def render(self, display: Display):
        self.display.display.fill(WHITE)
        self.state_manager.render(display)
        self.object_manager.render(display)
        self.display.flip()

    def run(self):
        while self.running:
            self.handle()
            self.tick()
            self.render(self.display)


if __name__ == '__main__':
    game = Main()
    game.run()
