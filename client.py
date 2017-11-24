import select, socket, sys
import helper

class Client:
    def __init__(self):
        self._utils = helper.ChatUtils()
        self._readBuffer = 4096
        self._host = "10.62.0.115"    # Need to change this

    def run(self):
        serverConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverConn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serverConn.connect((self._host, self._utils.getPort()))
        print("HELO text\n")
        message = ''
        listOfSocket = [sys.stdin, serverConn]
        while True:
            readSockets, writeSockets, errorSockets = select.select(listOfSocket, [], [])
            for s in readSockets:
                if s is serverConn:
                    msg = s.recv(self._readBuffer)
                    if not msg:
                        print("Failed: Server down!")
                        sys.exit(2)
                    else:
                        if msg == self._utils.getExitString():
                            sys.stdout.write('Exit\n')
                            sys.exit(2)
                        elif msg == self._utils.getJoinString():
                            sys.stdout.write('Join: %s', msg)
                        else:
                            sys.stdout.write(msg.decode())
                            if 'name' in msg.decode():
                                message = 'name: '
                            else:
                                message = ''

                else:
                    msg = message + sys.stdin.readline()
                    serverConn.sendall(msg.encode())


prg = Client()
prg.run()
