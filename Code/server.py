from collections import deque
from collections.abc import Callable, Sequence
from select import select
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, socket

Address = tuple[str, int]
Handler = Callable[[socket, Address], None]


tasks: Sequence[Handler] = deque()
recv_wait = {}
send_wait = {}


def run():
    while any([tasks, recv_wait, send_wait]):
        while not tasks:
            can_recv, can_send, _ = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))
        task = tasks.popleft()
        try:
            reason, resource = task.send(None)
            if reason == 'recv':
                recv_wait[resource] = task
            elif reason == 'send':
                send_wait[resource] = task
            else:
                raise RuntimeError(f'Unknown reason {reason!r}')
        except StopIteration:
            print('Task done')


class GenSocket:
    def __init__(self, sock):
        self.sock = sock

    def accept(self):
        yield 'recv', self.sock
        client, addr = self.sock.accept()
        return GenSocket(client), addr

    def recv(self, n):
        yield 'recv', self.sock
        return self.sock.recv(n)

    def send(self, data):
        yield 'send', self.sock
        return self.sock.send(data)

    def __getattr__(self, name):
        return getattr(self.sock, name)


def tcp_server(
    address: Address,
    handler: Handler,
):
    sock = GenSocket(socket(AF_INET, SOCK_STREAM))
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)

    while True:
        client, addr = yield from sock.accept()
        tasks.append(handler(client, addr))


def echo_handler(client: socket, address: Address):
    print(f'Connection from {address}')
    while True:
        data = yield from client.recv(1000)
        if not data:
            break
        yield from client.send(b'GOT:' + data)
    print('Connection closed')


if __name__ == '__main__':
    tasks.append(tcp_server(('', 25000), echo_handler))
    run()
