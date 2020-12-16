from gameServer import Server

server = Server()
server.init()
server.loop()
server.loop()
print(server.getHistory())