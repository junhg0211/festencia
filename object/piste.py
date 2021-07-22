from pygame import draw
from pygame.transform import rotate

from const import BLACK, RED, GREEN, PRETENDARD_BOLD, lang
from display import Display
from object import Object, Dualcircles
from util import center, Face, linear


class Piste(Object):
    WIDTH = 20
    HEIGHT = 11
    RADIUS = 0.88

    def __init__(self, green_name: str, red_name: str, display: Display, x: int = 0, y: int = 0):
        super().__init__(x, y)
        self.display = display

        self.width = self.display.width // 7 * 6
        self.height = self.width * 0.55

        self.center_x(self.display).set_y(50)

        self.dualcircles = Dualcircles(0, 0, 0, 0, self.height / 100 * 8)
        self.lowergap = self.display.height - (self.y + self.height)

        self.big_face = Face(PRETENDARD_BOLD, 128, BLACK)
        self.small_face = Face(PRETENDARD_BOLD, 64, BLACK)

        self.green_score = 0
        self.green_surface = self.big_face.render(str(self.green_score))
        self.green_score_x = center(self.x, self.green_surface.get_width())
        self.green_name_surface = rotate(self.small_face.render(green_name), 90)
        self.green_name_x = center(self.x, 64) - 5

        self.red_score = 0
        self.red_surface = self.big_face.render(str(self.red_score))
        self.red_score_x = center(self.x, self.red_surface.get_width()) + self.width + self.x
        self.red_name_surface = self.small_face.render(red_name)
        self.red_name_surface = rotate(self.small_face.render(red_name), -90)

        self.announcement = True
        self.announcement_surface = self.big_face.render(lang('piste.engarde'))
        self.announcement_x = center(self.display.width, self.announcement_surface.get_width())
        self.announcement_y = self.y + self.height + center(self.lowergap, self.announcement_surface.get_height())

        self.time_left = 147
        self.timer_surface = self.small_face.render('a')
        self.timer_x = self.display.width * .7

        self.assaut = 2
        self.assaut_surface = self.small_face.render(f'{self.assaut}/3')
        self.assaut_x = self.display.width * .3 - self.assaut_surface.get_width()

        self.extra_y = self.y + self.height + center(self.lowergap, self.timer_surface.get_height())

    def set_red_pos(self, x: float, y: float):
        self.dualcircles.x = linear(x, 0, Piste.WIDTH, self.x, self.x + self.width)
        self.dualcircles.y = linear(y, 0, Piste.HEIGHT, self.y, self.y + self.height)

    def set_green_pos(self, x: float, y: float):
        self.dualcircles.x2 = linear(x, 0, Piste.WIDTH, self.x, self.x + self.width)
        self.dualcircles.y2 = linear(y, 0, Piste.HEIGHT, self.y, self.y + self.height)

    def render_timer(self):
        minute = self.time_left // 60
        second = self.time_left % 60
        self.timer_surface = self.small_face.render(f'{minute}:{second:02d}')

    def set_green_score(self, score: int):
        self.green_score = score
        self.green_surface = self.big_face.render(str(self.green_score))
        self.green_score_x = center(self.x, self.green_surface.get_width())

    def set_red_score(self, score: int):
        self.red_score = score
        self.red_surface = self.big_face.render(str(self.red_score))
        self.red_score_x = center(self.x, self.red_surface.get_width()) + self.width + self.x

    def tick(self):
        self.dualcircles.tick()

        self.render_timer()

    def center_x(self, display: Display) -> 'Piste':
        self.x = center(display.width, self.width)
        return self

    def render(self, display: Display):
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

        if self.announcement:
            display.display.blit(
                self.announcement_surface, (self.announcement_x, self.announcement_y))
        display.display.blit(self.timer_surface, (self.timer_x, self.extra_y))
        display.display.blit(self.assaut_surface, (self.assaut_x, self.extra_y))
