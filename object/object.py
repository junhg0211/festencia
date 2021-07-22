from display import Display


class Object:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def set_x(self, x: int):
        self.x = x
        return self

    def set_y(self, y: int):
        self.y = y
        return self

    def add_x(self, dx: int):
        self.x += dx
        return self

    def add_y(self, dy: int):
        self.y += dy
        return self

    def tick(self):
        pass

    def render(self, display: Display):
        pass
