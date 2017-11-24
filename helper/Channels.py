'''

Channels are basically holds all the connections pertaining to single chat room

'''
class Channels:
    def __init__(self, name):
        self._entityWithRef = {}
        self._name = name

    def newMessage(self, entity, refId):
        msg = entity._name + " joined the chatroom: " + self._name + " refid : " + str(refId) + "\n"
        for ent, ref in self._entityWithRef.items():
            if(ent._name == entity._name and ref == refId):
                ent.socket.sendall(msg.encode())

    def broadcast(self, entity, msg):
        msg = entity._name.encode() + b" : " + msg
        for ent in self._entityWithRef:
            ent.socket.sendall(msg)

    def removeEntity(self, entity):
        if entity in self._entityWithRef:
            del self._entityWithRef[entity]
            self.broadcast(entity, entity._name.encode() + b" is no longer in the chatroom\n")
