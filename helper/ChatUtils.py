import socket


class ChatUtils:
    def __init__(self):
        self._totalClients = 30
        self._port = 22222
        self.leave_string = '/leave'
        self.exit_string = '/exit'
        self.join_string = '/join'

    def totalClients(self):
        return self._totalClients

    def getPort(self):
        return self._port

    def getLeaveString(self):
        return self.leave_string.encode()

    def getExitString(self):
        return self.exit_string.encode()

    def getJoinString(self):
        return self.join_string.encode()

    def create_socket(self, address):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setblocking(0)
        s.bind(address)
        s.listen(self._totalClients)
        #print("listening at ip: ", address)
        print("HELO text\nIP:%s\nPort:%s\nStudentID:%s" % (address[0], self._port, 17307906))
        return s
