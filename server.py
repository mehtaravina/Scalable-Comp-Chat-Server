import select, socket
import helper

class Server:
    def __init__(self):
        self._utils = helper.ChatUtils()
        self._chatApp = helper.ChatApplication()
        self._listOfConnection = []
        self._readBuffer = 4096
        self._host = "10.62.0.115"    # Need to change this

    def run(self):
        listen_sock = self._utils.create_socket((self._host, self._utils.getPort()))
        self._listOfConnection.append(listen_sock)
        while True:
            readSockets, writeSockets, errorSockets = select.select(self._listOfConnection, [], [])
            for entity in readSockets:
                if entity is listen_sock:
                    new_socket, add = entity.accept()
                    new_entity = helper.SingleEntity(new_socket)
                    self._listOfConnection.append(new_entity)
                    self._chatApp.newMessage(new_entity)

                else:
                    msg = entity.socket.recv(self._readBuffer)
                    if msg:
                        msg = msg.decode().lower()
                        self._chatApp.messageHandler(entity, msg)
                    else:
                        entity.socket.close()
                        self._listOfConnection.remove(entity)

            for sock in errorSockets: # close error sockets
                sock.close()
                self._listOfConnection.remove(sock)


prg = Server()
prg.run()
