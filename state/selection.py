from const import PRETENDARD_BOLD, BLACK, lang
from display import Display
from manager import MouseManager, ObjectManager, KeyboardManager
from object import Dualcircles, FPSCalculator, Text, TextButton, TextInserter
from state import State
from util import Face, Spacer, center


class Selection(State):
    GAP = 150
    PADDING = 50

    def __init__(self, mode: str, display: Display, state_manager, fps_calculator: FPSCalculator,
                 mouse_manager: MouseManager, keyboard_manager: KeyboardManager, *args):
        """
        args: when mode is

        * ``title``, [shutdown: Callable]
        """

        super().__init__()

        self.display = display
        self.state_manager = state_manager
        self.fps_calculator = fps_calculator
        self.mouse_manager = mouse_manager
        self.keyboard_manager = keyboard_manager

        self.dualcircles = Dualcircles(0, 0, 0, 0, self.display, self.fps_calculator).random_pos(self.display)
        self.object_manager.add(self.dualcircles)

        title_face = Face(PRETENDARD_BOLD, 128, BLACK)

        button_face = Face(PRETENDARD_BOLD, 32, BLACK)
        self.reactables = ObjectManager()
        self.spacer = None
        title = lang('title')
        if mode == 'title':
            host = TextButton(lang('state.title.host'), button_face, lambda: self.state_manager.state_to('host'),
                              self.mouse_manager) \
                .center_y(self.display).add_y(Selection.PADDING)
            join = TextButton(lang('state.title.join'), button_face, lambda: None, self.mouse_manager) \
                .center_y(self.display).add_y(Selection.PADDING)
            spectate = TextButton(lang('state.title.spectate'), button_face, lambda: None, self.mouse_manager) \
                .center_y(self.display).add_y(Selection.PADDING)
            quit_ = TextButton(lang('state.title.quit'), button_face, args[0], self.mouse_manager) \
                .center_y(self.display).add_y(Selection.PADDING)

            self.reactables.add(host)
            self.reactables.add(join)
            self.reactables.add(spectate)
            self.reactables.add(quit_)
            self.spacer = Spacer(Selection.GAP, *self.reactables.objects)
        elif mode == 'host':
            title = lang('state.host.title')

            port = TextInserter(f'{lang("state.host.port")}: {{}}', button_face,
                                self.mouse_manager, self.keyboard_manager, '31872') \
                .center_y(self.display).add_y(Selection.PADDING)
            game_title = TextInserter(f'{lang("state.host.title")}: {{}}', button_face,
                                      self.mouse_manager, self.keyboard_manager, lang('state.host.default_name')) \
                .center_y(self.display).add_y(Selection.PADDING)
            back = TextButton(lang('state.host.back'), button_face, lambda: self.state_manager.state_to('title'),
                              self.mouse_manager) \
                .center_y(self.display).add_y(Selection.PADDING)
            start = TextButton(lang('state.host.start'), button_face,
                               lambda: self.state_manager.state_to('host_game', game_title.string),
                               self.mouse_manager) \
                .center_y(self.display).add_y(Selection.PADDING)

            self.reactables.add(port)
            self.reactables.add(game_title)
            self.reactables.add(back)
            self.reactables.add(start)

            self.spacer = Spacer(Selection.GAP, *self.reactables.objects)

        self.title = Text(title, title_face).center(self.display).add_y(-75)
        self.object_manager.add(self.title)

    def tick(self):
        super().tick()

        if self.mouse_manager.left_start:
            self.dualcircles.random_pos(self.display)

        self.spacer.objects[0].set_x(center(self.display.width, self.spacer.get_width()))
        self.reactables.tick()
        self.spacer.tick()

    def render(self, display: Display):
        super().render(display)
        self.reactables.render(display)
