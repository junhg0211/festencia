import re
from socket import gethostbyname, getfqdn

from const import PRETENDARD_BOLD, BLACK, lang
from display import Display
from manager import MouseManager, ObjectManager, KeyboardManager
from object import Dualcircles, FPSCalculator, Text, TextButton, TextInserter
from settings import settings, update
from state import State
from util import Face, Spacer, center


class Selection(State):
    """ The state where the user can select an action. """

    GAP = 150
    PADDING = 50

    TITLE = 'title'
    HOST = 'host'
    ERROR = 'error'
    JOIN = 'join'

    def __init__(self, mode: str, display: Display, state_manager, fps_calculator: FPSCalculator,
                 mouse_manager: MouseManager, keyboard_manager: KeyboardManager, *args):
        """
        args: when mode is
        * ``title``, [shutdown: Callable]
        """

        super().__init__()

        self.mode = mode
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
        if mode == Selection.TITLE:
            host = TextButton(lang('state.title.host'), button_face, lambda: self.state_manager.state_to('host'),
                              self.mouse_manager)
            join = TextButton(lang('state.title.join'), button_face,
                              lambda: self.state_manager.state_to('join'), self.mouse_manager)
            spectate = TextButton(lang('state.title.spectate'), button_face, lambda: None, self.mouse_manager)
            quit_ = TextButton(lang('state.title.quit'), button_face, args[0], self.mouse_manager)

            self.reactables.add(host)
            self.reactables.add(join)
            self.reactables.add(spectate)
            self.reactables.add(quit_)
            self.spacer = Spacer(Selection.GAP, *self.reactables.objects)

        elif mode == Selection.HOST:
            title = lang('state.title.host')

            port = TextInserter(lang("state.host.port_template"), button_face,
                                self.mouse_manager, self.keyboard_manager, settings['port'])
            game_title = TextInserter(lang('state.host.room_title_template'), button_face,
                                      self.mouse_manager, self.keyboard_manager, settings['room_title'])
            game_title.ender = lambda: update('room_title', game_title.inserted)
            back = TextButton(lang('state.host.back'), button_face, lambda: self.state_manager.state_to('title'),
                              self.mouse_manager)
            start = TextButton(lang('state.host.start'), button_face,
                               lambda: self.state_manager.state_to('host_game',
                                                                   game_title.inserted, gethostbyname(getfqdn()),
                                                                   int(port.inserted), settings['name']),
                               self.mouse_manager)

            self.reactables.add(port)
            self.reactables.add(game_title)
            self.reactables.add(back)
            self.reactables.add(start)
            self.spacer = Spacer(Selection.GAP, *self.reactables.objects)

        elif mode == Selection.ERROR:
            title = lang('state.error.title')

            content = Text(args[0], button_face)
            back = TextButton(lang('state.error.back'), button_face, lambda: self.state_manager.state_to('title'),
                              self.mouse_manager)

            self.reactables.add(content)
            self.reactables.add(back)
            self.spacer = Spacer(Selection.GAP, *self.reactables.objects)

        elif mode == Selection.JOIN:
            title = lang('state.title.join')

            host = TextInserter(lang('state.join.host_template'), button_face, self.mouse_manager,
                                self.keyboard_manager, settings['host'])
            host.ender = lambda: update('host', host.inserted)
            port = TextInserter(lang('state.join.port_template'), button_face, self.mouse_manager,
                                self.keyboard_manager, settings['port'])
            port.ender = lambda: update('port', port.inserted)
            name = TextInserter(lang('state.join.name_template'), button_face, self.mouse_manager,
                                self.keyboard_manager, settings['name'])

            def ender():
                update('name', name.inserted)
                if re.compile(r'[\dA-Z\- ]+').fullmatch(name.inserted) is None or \
                        button_face.render(name.inserted).get_width() > button_face.render('W' * 12).get_width():
                    name.set_inserted('UNNAMED')
            name.ender = ender
            back = TextButton(lang('state.join.back'), button_face, lambda: self.state_manager.state_to('title'),
                              self.mouse_manager)
            join = TextButton(lang('state.join.join'), button_face,
                              lambda: self.state_manager.state_to('join_game', host.inserted, int(port.inserted),
                                                                  settings['name']),
                              self.mouse_manager)

            self.reactables.add(host)
            self.reactables.add(port)
            self.reactables.add(name)
            self.reactables.add(back)
            self.reactables.add(join)
            self.spacer = Spacer(Selection.GAP, *self.reactables.objects)

        for object_ in self.reactables.objects:
            # noinspection PyUnresolvedReferences
            object_.center_y(self.display).add_y(Selection.PADDING)

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
