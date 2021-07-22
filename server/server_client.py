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

    def recv(self):
        value = self.connection.recv(1024).decode()
        Log.server(f'{self} -> {value}')
        return value

    def send(self, value: str):
        self.connection.send(value.encode())
        Log.server(f'{self} <- {value}')
        return value

    def run(self):
        while self.connected:
            recv = self.recv()
            if not recv:
                self.quit()
                break

            tokens = recv.split(' ')

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
                    self.send('HOSTOK')
                else:
                    self.send('HOSTNO')
            elif tokens[0] == 'SETTITLE':
                if self.server.host == self:
                    self.server.title = ' '.join(tokens[1:])
            elif tokens[0] == 'JOIN':
                if self.server.joiner is None:
                    self.server.joiner = self
                    self.name = ' '.join(tokens[1:])
                    self.send('JOINOK')
                else:
                    self.send('JOINNO')
            elif tokens[0] == 'QUIT':
                self.quit()
            elif tokens[0] == 'MESSAGE':
                self.server.announce(recv)
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
                    self.server.host_x = x
                    self.server.host_y = y
                    self.server.announce(f'HPOS {x} {y}')
                elif self == self.server.joiner:
                    self.server.joiner_x = x
                    self.server.joiner_y = y
                    self.server.announce(f'JPOS {x} {y}')
            elif tokens[0] == 'CLICK':
                if self == self.server.host:
                    self.server.game.host_click()
                elif self == self.server.joiner:
                    self.server.game.joiner_click()

    def quit(self):
        self.connected = False
        halt = False
        if self in self.server.host:
            self.server.host = None
            halt = True
        elif self in self.server.joiner:
            self.server.joiner = None
            halt = True
        else:
            if self in self.server.spectators:
                self.server.spectators.remove(self)

        if halt:
            self.server.announce('ANNOUNCE halte')
