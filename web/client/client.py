from socket import socket
from threading import Thread
from time import time

from const import GREEN, RED
from object.piste import Piste
from util import Log, linear


class Client:
    def __init__(self, host: str, port: int, state_manager, piste: Piste):
        self.host = host
        self.port = port
        self.state_manager = state_manager
        self.piste = piste

        self.s = socket()

        self.running = False

        self.thread = Thread(target=self.run)
        self.thread.setDaemon(True)

    def send_host(self, name: str):
        self.send(f'HOST {name}')

    def send_set_title(self, title: str):
        self.send(f'SETTITLE {title}')

    def connect(self):
        self.s.connect((self.host, self.port))
        Log.client(f'Connected to {self.host}:{self.port}')

    def handle(self):
        self.running = True
        self.thread.start()

    def recv(self) -> str:
        value = self.s.recv(1024).decode()
        Log.client(f'<- {value}')
        return value

    def send(self, value: str):
        self.s.send(value.encode())
        Log.client(f'-> {value}')

    def start(self):
        self.connect()
        self.handle()

    def run(self):
        Log.client(f'{self.thread.name} started.')
        while self.running:
            recv = self.recv()
            if not recv:
                self.quit()
                break

            tokens = recv.split(' ')

            if tokens[0] == 'PING':
                a_time = tokens[1]
                self.send(f'PONG {a_time} {time()}')
            elif tokens[0] == 'PONG':
                message = ' '.join(tokens[1:])
                Log.client(f'PONG {message}')
            elif tokens[0] == 'HOSTNAME':
                name = ' '.join(tokens[1:])
                self.piste.set_green_name(name)
            elif tokens[0] == 'JOINNAME':
                name = ' '.join(tokens[1:])
                self.piste.set_red_name(name)
            elif tokens[0] == 'ASSA':
                assaut = int(tokens[1])
                self.piste.update_assaut(assaut)
            elif tokens[0] == 'TIME':
                anchor = float(tokens[1])
                time_ = float(tokens[2])
                self.piste.set_time_left(time_ + (time() - anchor))
            elif tokens[0] == 'ANNOUNCE':
                sign = tokens[1]
                self.piste.set_announcement(sign)
            elif tokens[0] == 'HPOS':
                x = float(tokens[1])
                y = float(tokens[2])
                self.piste.dualcircles.set_x(x).set_y(y)
            elif tokens[0] == 'JPOS':
                x = float(tokens[1])
                y = float(tokens[2])
                self.piste.dualcircles.set_x2(x).set_y2(y)
            elif tokens[0] == 'CLICK':
                host = tokens[0] == 'True'
                x = linear(float(tokens[1]), 0, Piste.WIDTH, self.piste.x, self.piste.x + self.piste.width)
                y = linear(float(tokens[2]), 0, Piste.HEIGHT, self.piste.y, self.piste.y + self.piste.height)
                self.piste.click(x, y, GREEN if host else RED)
            elif tokens[0] == 'HOSTOK':
                name = ' '.join(tokens[1:])
                self.piste.set_green_name(name)
            elif tokens[0] == 'TITLE':
                title = ' '.join(tokens[1:])
                self.piste.set_title(title)

    def quit(self):
        # todo things when server closed
        if self.running:
            Log.client('Quit')
            self.send('QUIT')
            self.s.close()
            self.running = False
