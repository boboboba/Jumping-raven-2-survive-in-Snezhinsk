import socket
from _thread import *
import pickle
from player import Player
from bullets import Bullet
from wrapper import Wrap
from map import Map

server = 'localhost'
port = 8686

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
s.listen(2)
print("Waiting for a connection, Server Started")
map = Map()

players = dict()
entities_to_send = dict() #key - to whom player
c = 0

def client(conn):

    global c
    identifier = c
    with open('map.txt') as f:
        conn.send(pickle.dumps((identifier, f.readlines())))
    # players[identifier] = Wrap(Player(0,0,0,0))
    # players[identifier].id = identifier
    entities_to_send[identifier] = []
    c += 1
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            if data.type == 'player':
                data.id = identifier
                players[identifier] = data
            elif data.type == 'bullet' or data.type == 'bbullet':
                for player_key in entities_to_send.keys():
                        if player_key != identifier:
                            entities_to_send[player_key].append(data)
            # _id, _type, x, y, velx, vely = data.split(';')
            # if _type == 'p':
            #     players[identifier] = data
            # elif _type == 'b':
            #     for player_key in entities_to_send.keys():
            #         if player_key != identifier:
            #             entities_to_send[player_key].append(';'.join([identifier, _type, x, y, velx, vely]))


            # if isinstance(data, Player):
            #     players[identifier] = data
            # elif isinstance(data, Bullet):
            #     for key in entities_to_send.keys():
            #         if key != identifier:
            #             entities_to_send[key].append(data)
            #     print(len(entities_to_send))
            if not data:
                print("Disconnected")
                break

            reply = []
            for key, item in players.items():
                if key != identifier:
                    reply.append(item)
            reply += entities_to_send[identifier]
            entities_to_send[identifier].clear()
            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    conn.close()
    players.pop(identifier)


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    # client(conn)
    start_new_thread(client, (conn,))