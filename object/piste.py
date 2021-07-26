from time import time

from pygame import draw, gfxdraw
from pygame.transform import rotate

from const import BLACK, RED, GREEN, PRETENDARD_BOLD, lang
from display import Display
from object import Object, Dualcircles, Text
from util import center, Face, linear


class Click(Object):
    DURATION = 2

    def __init__(self, x: int, y: int, color: tuple, intersection: list, time_: float, excludes: list):
        super().__init__(x, y)
        self.color = color
        self.intersection = intersection
        self.time = time_
        self.excludes = excludes

    def tick(self):
        if self.time + Click.DURATION < time():
            self.excludes.append(self.time)

    def render(self, display: Display):
        draw.aaline(display.display, self.color, (self.x - 10, self.y - 10), (self.x + 10, self.y + 10))
        draw.aaline(display.display, self.color, (self.x - 10, self.y + 10), (self.x + 10, self.y - 10))
        if self.intersection:
            gfxdraw.polygon(display.display, self.intersection, self.color)


class Piste(Object):
    WIDTH = 20
    HEIGHT = 11
    RADIUS = 1.8

    def __init__(self, green_name: str, red_name: str, title: str, display: Display, x: int = 0, y: int = 0):
        super().__init__(x, y)
        self.display = display

        self.width = self.display.width // 7 * 6
        self.height = self.width * 0.55

        self.center_x(self.display).set_y(50)

        self.dualcircles = Dualcircles(0, 0, 0, 0, linear(Piste.RADIUS, 0, Piste.HEIGHT, 0, self.height))
        self.lowergap = self.display.height - (self.y + self.height)

        self.big_face = Face(PRETENDARD_BOLD, 128, BLACK)
        self.small_face = Face(PRETENDARD_BOLD, 64, BLACK)

        self.green_score = 0
        self.green_surface = self.big_face.render(str(self.green_score))
        self.green_score_x = center(self.x, self.green_surface.get_width())
        self.green_name_surface = None
        self.green_name_x = center(self.x, 64) - 5
        self.set_green_name(green_name)

        self.red_score = 0
        self.red_surface = self.big_face.render(str(self.red_score))
        self.red_score_x = center(self.x, self.red_surface.get_width()) + self.width + self.x
        self.red_name_surface = None
        self.set_red_name(red_name)

        title_face = Face(PRETENDARD_BOLD, 24, BLACK)
        self.title = Text(title, title_face, y=10).center_x(self.display)

        self.announcement = True
        self.announcement_surface = self.big_face.render(lang('piste.engarde'))
        self.announcement_x = center(self.display.width, self.announcement_surface.get_width())
        self.announcement_y = self.y + self.height + center(self.lowergap, self.announcement_surface.get_height())

        self.time_left = 180
        self.timer_surface = self.small_face.render('3:00')
        self.timer_x = self.display.width * .7

        self.assaut = 0
        self.assaut_surface = None
        self.assaut_x = 0
        self.update_assaut(1)

        self.extra_y = self.y + self.height + center(self.lowergap, self.timer_surface.get_height())

        self.clicks = dict()
        self.clicks_excludes = list()

    def click(self, x: int, y: int, color: tuple) -> 'Piste':
        now = time()
        self.clicks[now] = Click(x, y, color, self.dualcircles.arc_vertices.copy(), now, self.clicks_excludes)
        return self

    def render_timer(self) -> 'Piste':
        minute = int(self.time_left) // 60
        second = int(self.time_left) % 60
        self.timer_surface = self.small_face.render(f'{minute}:{second:02d}')
        return self

    def update_assaut(self, assaut) -> 'Piste':
        self.assaut = assaut
        self.assaut_surface = self.small_face.render(f'{self.assaut}/3')
        self.assaut_x = self.display.width * .3 - self.assaut_surface.get_width()
        return self

    def center_x(self, display: Display) -> 'Piste':
        self.x = center(display.width, self.width)
        return self

    def set_announcement(self, sign) -> 'Piste':
        self.announcement_surface = self.big_face.render(lang(f'piste.{sign}'))
        self.announcement_x = center(self.display.width, self.announcement_surface.get_width())
        return self

    def set_time_left(self, time_left) -> 'Piste':
        self.time_left = time_left
        return self.render_timer()

    def set_title(self, title: str) -> 'Piste':
        self.title.set_text(title).center_x(self.display)
        return self

    def set_green_name(self, green_name: str) -> 'Piste':
        self.green_name_surface = rotate(self.small_face.render(green_name), 90)
        return self

    def set_red_name(self, red_name: str) -> 'Piste':
        self.red_name_surface = rotate(self.small_face.render(red_name), -90)
        return self

    def set_red_pos(self, x: float, y: float) -> 'Piste':
        self.dualcircles.x = linear(x, 0, Piste.WIDTH, self.x, self.x + self.width)
        self.dualcircles.y = linear(y, 0, Piste.HEIGHT, self.y, self.y + self.height)
        return self

    def set_green_pos(self, x: float, y: float) -> 'Piste':
        self.dualcircles.x2 = linear(x, 0, Piste.WIDTH, self.x, self.x + self.width)
        self.dualcircles.y2 = linear(y, 0, Piste.HEIGHT, self.y, self.y + self.height)
        return self

    def set_green_score(self, score: int) -> 'Piste':
        self.green_score = score
        self.green_surface = self.big_face.render(str(self.green_score))
        self.green_score_x = center(self.x, self.green_surface.get_width())
        return self

    def set_red_score(self, score: int) -> 'Piste':
        self.red_score = score
        self.red_surface = self.big_face.render(str(self.red_score))
        self.red_score_x = center(self.x, self.red_surface.get_width()) + self.width + self.x
        return self

    def tick(self):
        for click in set(self.clicks.values()):
            click.tick()

        for exclude in self.clicks_excludes:
            del self.clicks[exclude]
        self.clicks_excludes.clear()

        self.dualcircles.tick()
        self.render_timer()

    def render(self, display: Display):
        try:
            for click in self.clicks.values():
                click.render(display)
        except RuntimeError:
            pass

        self.dualcircles.render(display)
        draw.lines(display.display, BLACK, True, (
            (self.x, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height),
            (self.x + self.width, self.y)))

        draw.rect(display.display, GREEN, ((0, 0), (self.x, 30)))
        display.display.blit(self.green_surface, (self.green_score_x, 30))
        display.display.blit(self.green_name_surface, (self.green_name_x, 190))

        draw.rect(display.display, RED, ((self.x + self.width, 0), (self.x, 30)))
        display.display.blit(self.red_surface, (self.red_score_x, 30))
        display.display.blit(self.red_name_surface, (self.green_name_x + self.x + self.width, 190))

        self.title.render(display)

        if self.announcement:
            display.display.blit(
                self.announcement_surface, (self.announcement_x, self.announcement_y))
        display.display.blit(self.timer_surface, (self.timer_x, self.extra_y))
        display.display.blit(self.assaut_surface, (self.assaut_x, self.extra_y))
