from threading import Thread


class ServerGame:
    WIDTH = 20
    HEIGHT = 11
    RADIUS = 0.88

    def __init__(self, server):
        self.server = server

        self.title = ''

        self.host_x = 0
        self.host_y = 0
        self.joiner_x = ServerGame.WIDTH
        self.joiner_y = ServerGame.HEIGHT

        self.assaut = 1
        self.time = 180.0
        self.state = 0
        """
        0 - not started waiting for participant
        1 - en garde
        2 - prêt (waiting for a second)
        3 - prêt (waiting for less than a second)
        4 - allez
        5 - halte (coup)
        6 - halte (8 score resting (30s))
        7 - end (result)
        9 - halte (participants left)
        """

        self.running = False
        self.thread = Thread(target=self.start)

    def host_click(self):
        pass  # todo when host clicked

    def joiner_click(self):
        pass  # todo when joiner clicked

    def start(self):
        self.running = True

    def run(self):
        while self.running:
            pass

    def tick(self):
        pass
