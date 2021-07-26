from socket import socket
from threading import Thread
from time import time

from util import Log


class ServerClient:
    def __init__(self, server, connection: socket, host: str, port: int):
        self.server = server
        self.connection = connection
        self.host = host
        self.port = port

        self.name = ''

        self.connected = True

        self.thread = Thread(target=self.run)

    def __str__(self):
        return f'{self.host}:{self.port}'

    def __eq__(self, other):
        return str(self) == str(other)

    def handle(self):
        self.thread.setDaemon(True)
        self.thread.start()

    def recv(self) -> list:
        try:
            value = self.connection.recv(1024).decode().split('\n')
        except ConnectionResetError:
            self.quit()
            Log.server(f'{self.host}:{self.port} ConnectionReset, quitted.')
        else:
            while '' in value:
                value.remove('')
            for line in value:
                if 'POS' not in line:
                    Log.server(f'{self} -> {line}')
            return value

    def send(self, value: str):
        self.connection.send(f'{value}\n'.encode())
        if 'POS' not in value:
            Log.server(f'{self} <- {value}')
        return value

    def run(self):
        while self.connected:
            recv = self.recv()
            if not recv:
                break

            for line in recv:
                tokens = line.split(' ')

                if tokens[0] == 'PING':
                    message = ' '.join(tokens[1:])
                    self.send(f'PONG {message}')
                elif tokens[0] == 'PONG':
                    a_time = float(tokens[1])
                    b_time = float(tokens[2])
                    c_time = time()
                    Log.server(f'{self}. SEND {(b_time - a_time) * 1000:.1f}ms, '
                               f'RECV {(c_time - b_time) * 1000:.1f}ms, '
                               f'PING {(c_time - a_time) * 1000:.1f} ms')
                elif tokens[0] == 'HOST':
                    if self.server.host is None:
                        self.server.host = self
                        self.name = ' '.join(tokens[1:])
                        self.send(f'HOSTOK {self.name}')
                    else:
                        self.send('HOSTNO')
                elif tokens[0] == 'SETTITLE':
                    if self.server.host == self:
                        self.server.title = ' '.join(tokens[1:])
                    self.server.announce(f'TITLE {self.server.title}')
                elif tokens[0] == 'JOIN':
                    if self.server.joiner is None:
                        self.server.joiner = self
                        self.name = ' '.join(tokens[1:])
                        self.send(f'JOINOK {self.server.title}')
                        self.server.announce(f'JOINNAME {self.name}')
                    else:
                        self.send('JOINNO')
                elif tokens[0] == 'QUIT':
                    self.quit()
                elif tokens[0] == 'MESSAGE':
                    self.server.announce(line)
                elif tokens[0] == 'SPEC':
                    self.server.spectators.append(self)
                    self.send('SPECOK')
                elif tokens[0] == 'HOSTNAME':
                    if self.server.host:
                        self.send(f'HOSTNAME {self.server.host.name}')
                    else:
                        self.send('NOHOST')
                elif tokens[0] == 'JOINNAME':
                    if self.server.joiner:
                        self.send(f'JOINNAME {self.server.joiner.name}')
                    else:
                        self.send('NOJOIN')
                elif tokens[0] == 'SPECNAME':
                    names = list()
                    for spectator in self.server.spectators:
                        names.append(spectator.name)
                    names = ','.join(names)
                    self.send(f'SPECNAME {names}')
                elif tokens[0] == 'ASSA':
                    self.send(f'ASSA {self.server.assaut}')
                elif tokens[0] == 'TIME':
                    anchor, time_ = self.server.get_anchor_time()
                    self.send(f'TIME {anchor} {time_}')
                elif tokens[0] == 'POS':
                    x = float(tokens[1])
                    y = float(tokens[2])
                    if self == self.server.host:
                        self.server.game.host_x = x
                        self.server.game.host_y = y
                        self.server.announce(f'HPOS {x} {y}')
                    elif self == self.server.joiner:
                        self.server.game.joiner_x = x
                        self.server.game.joiner_y = y
                        self.server.announce(f'JPOS {x} {y}')
                elif tokens[0] == 'CLICK':
                    if self == self.server.host:
                        self.server.game.host_click()
                    elif self == self.server.joiner:
                        self.server.game.joiner_click()
                elif tokens[0] == 'START':
                    if self == self.server.host:
                        if not self.server.game.running:
                            self.server.game.start()
        self.quit()

    def quit(self):
        if self.connected:
            self.connected = False
            if self == self.server.host:
                self.server.host = None
                self.server.announce('ANNOUNCE halte')
            elif self == self.server.joiner:
                self.server.joiner = None
                self.server.announce('ANNOUNCE halte')
            elif self in self.server.spectators:
                self.server.spectators.remove(self)
