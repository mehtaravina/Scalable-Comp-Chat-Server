'''

Framework to hold channels

'''
import helper
import random
class ChatApplication:
    def __init__(self):
        #self._channels = {}
        self._channelsRef = {}
        self._port = 22222
        self._channelEntityDict = {}
            # { channelName :
                #{ entityName : refNum }
            #}
        self.leave_string = '/leave'
        self.exit_string = '/exit'
        self._host = "10.62.0.115"

    def newMessage(self, newEntity):
        newEntity.socket.sendall(b'client_name:\n')

    def listChannelsWithRefId(self, entity):
        if len(self._channelsRef) == 0:
            msg = 'No active chat channels. use /join [group] to create a new chat\n'
            entity.socket.sendall(msg.encode())
        else:
            msg = 'list of all the available chatrooms\n'
            for channel in self._channelsRef:
                msg += channel + ": " + str(len(self._channelsRef[channel]._entityWithRef)) + " members\n" #+ str(self._channelsRef[channel]._refId) + " \n"
            entity.socket.sendall(msg.encode())

    def messageHandler(self, entity, msg):
        message = b'Commands : /list , /join [group], /leave, /msg [group] [message]:\n'
        #print(entity._name + " writes: " + msg)
        if "name:" in msg:
            name = msg.split()[1]
            entity._name = name
            print("CLIENT_IP:%s\nPORT:%s\nCLIENT_NAME:%s\n" %("0", self._port, entity._name))
            entity.socket.sendall(message)

        elif "/join" in msg:
            if len(msg.split()) >= 2:
                channel_name = msg.split()[1]
                refId = random.randint(100, 9999)
                joinId = random.randint(10000, 999999)
                # Algo : Check for the channel to join
                #   If it not existing : Create a new channel
                #   If it existing : join the channel or switch the channel
                # Need to work on better approach for switching or identifying the channels
                if not channel_name in self._channelsRef:
                    new_channel = helper.Channels(channel_name)
                    self._channelsRef[channel_name] = new_channel

                if channel_name in self._channelsRef:
                    self._channelsRef[channel_name]._entityWithRef.update({entity:[refId, joinId]})
                    self._channelsRef[channel_name].newMessage(entity, refId)
                    self._channelEntityDict[entity._name] = {channel_name:refId}
                print("JOINED_CHATROOM:%s\nSERVER_IP:%s\nPORT:%s\nROOM_REF:%s\nJOIN_ID:%s\n" % (channel_name, self._host, self._port, str(refId), joinId))
            else:
                entity.socket.sendall(message)

        elif "/list" in msg:
            self.listChannelsWithRefId(entity)

        elif "/leave" in msg:
            if(len(msg.split()) >= 2):
                channel_name = msg.split()[1]
                self.removeEntity(channel_name, entity)

            else:
                msg = 'No valid argument, use /leave [group] command \n'
                entity.socket.sendall(msg.encode())

        elif "/exit" in msg:
            entity.socket.sendall(self.exit_string.encode())
            self.exitEntity(entity)

        elif "/msg" in msg:
            if len(msg.split()) >= 2:
                channel_name = msg.split()[1]
                messageBrod = " ".join(msg.split()[2:])
                messageBrod = messageBrod + '\n'
                if entity._name in self._channelEntityDict:
                    if self._channelsRef[channel_name]:
                        refId = self._channelsRef[channel_name]._entityWithRef[entity][0]
                        joinId = self._channelsRef[channel_name]._entityWithRef[entity][1]
                        print("CHAT:%s\nJOIN_ID:%s\nCLIENT_NAME:%s\nMESSAGE:%s\n" % (refId, joinId, entity._name, messageBrod))
                        self._channelsRef[channel_name].broadcast(entity, messageBrod.encode())
                else:
                    msg = 'No chatrooms available, use /join [group], /msg [group] [message] command \n'
                    entity.socket.sendall(msg.encode())
        else:
            print ("no valid argument, use /list or /join [group] or /msg [group] [message]")

    def removeEntity(self, channel_name , entity):
        if channel_name in self._channelsRef:
            refId = self._channelsRef[channel_name]._entityWithRef[entity][0]
            joinId = self._channelsRef[channel_name]._entityWithRef[entity][1]
            print("LEFT_CHATROOM:%s\nJOIN_ID:%s\nCLIENT_NAME:%s\n" % (refId, joinId, entity._name))
            if entity._name in self._channelEntityDict:
                self._channelsRef[channel_name].removeEntity(entity)

    def exitEntity(self, entity):
        if entity._name in self._channelEntityDict:
            for key in self._channelEntityDict[entity._name].keys():
                self._channelsRef[key].removeEntity(entity)
        del self._channelEntityDict[entity._name]
        print("DISCONNECT:%s\nPORT:%s\nCLIENT_NAME:%s\n" % (self._host, self._port, entity._name))
