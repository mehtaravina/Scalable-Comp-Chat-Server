
class SingleEntity:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self._name = name

    def fileno(self):
        return self.socket.fileno()
