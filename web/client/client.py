from socket import socket
from threading import Thread
from time import time

import globals
from const import GREEN, RED, lang
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
        self.halted = False  # when socket is not connected to server and need to stop all the operations in this object

        self.thread = Thread(target=self.run)
        self.thread.setDaemon(True)

    def send_host(self, name: str):
        self.send(f'HOST {name}')

    def send_set_title(self, title: str):
        self.send(f'SETTITLE {title}')

    def send_join(self, name: str):
        self.send(f'JOIN {name}')

    def send_host_name(self):
        self.send('HOSTNAME')

    def send_join_name(self):
        self.send('JOINNAME')

    def send_click(self):
        self.send('CLICK')

    def send_pos(self, x: float, y: float):
        self.send(f'POS {x} {y}')

    def send_start(self):
        self.send('START')

    def connect(self):
        Log.client(f'Connecting to {self.host}:{self.port}')
        try:
            self.s.connect((self.host, self.port))
        except TimeoutError:
            Log.client('Connection timed out, closing the Client socket.')
            self.halted = True
            self.quit()
            globals.data['state_manager'].state_to('error', lang('error.join_timeout'))
        except ConnectionRefusedError:
            Log.client('Connection refused, closing the Client socket.')
            self.halted = True
            self.quit()
            globals.data['state_manager'].state_to('error', lang('error.connection_refused'))
        else:
            Log.client(f'Connected to {self.host}:{self.port}')

    def handle(self):
        if not self.halted:
            self.running = True
            self.thread.start()
        else:
            Log.client('Handle signed but client halted, ignore the sign.')

    def recv(self) -> list:
        if not self.halted:
            try:
                value = self.s.recv(1024).decode().split('\n')
            except OSError:
                Log.client('Connection destroyed, closing the Client socket.')
                self.halted = True
                self.quit()
                globals.data['state_manager'].state_to('error', lang('error.connection_destroyed'))
                return list()
            else:
                while '' in value:
                    value.remove('')
                for line in value:
                    if 'POS' not in line:
                        Log.client(f'<- {line}')
                return value
        else:
            return list()

    def send(self, value: str):
        if not self.halted:
            try:
                self.s.send(f'{value}\n'.encode())
            except OSError:
                self.quit()
                globals.data['state_manager'].state_to('error', lang('error.disconnected'))
                return
            if 'POS' not in value:
                Log.client(f'-> {value}')

    def start(self):
        Log.client('Start operated.')
        self.connect()
        self.handle()

    def run(self):
        Log.client(f'{self.thread.name} started.')
        while self.running:
            recv = self.recv()
            if not recv:
                break

            for line in recv:
                tokens = line.split(' ')

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
                    x, y = self.interpolate_pos(tokens[1], tokens[2])
                    self.piste.dualcircles.set_x2(x).set_y2(y)
                elif tokens[0] == 'JPOS':
                    x, y = self.interpolate_pos(tokens[1], tokens[2])
                    self.piste.dualcircles.set_x(x).set_y(y)
                elif tokens[0] == 'CLICK':
                    host = tokens[1] == 'True'
                    x, y = self.interpolate_pos(tokens[2], tokens[3])
                    self.piste.click(x, y, GREEN if host else RED)
                elif tokens[0] == 'HOSTOK':
                    name = ' '.join(tokens[1:])
                    self.piste.set_green_name(name)
                elif tokens[0] == 'TITLE':
                    title = ' '.join(tokens[1:])
                    self.piste.set_title(title)
                elif tokens[0] == 'JOINOK':
                    title = ' '.join(tokens[1:])
                    self.piste.set_title(title)
                elif tokens[0] == 'HSCORE':
                    score = int(tokens[1])
                    self.piste.set_green_score(score)
                elif tokens[0] == 'JSCORE':
                    score = int(tokens[1])
                    self.piste.set_red_score(score)
        self.quit()

    def interpolate_pos(self, x: str, y: str):
        x = linear(float(x), 0, Piste.WIDTH, self.piste.x, self.piste.x + self.piste.width)
        y = linear(float(y), 0, Piste.HEIGHT, self.piste.y, self.piste.y + self.piste.height)
        return x, y

    def quit(self):
        if self.running and not self.halted:
            Log.client('Quit')
            self.send('QUIT')
            self.running = False
        self.s.close()
        Log.client('Socket closed.')
