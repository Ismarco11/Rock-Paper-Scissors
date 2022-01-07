import socket
from _thread import *
from player import Player
import pickle
from game import Game

server = "192.168.1.104"
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_inter(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    print(str(p))

    reply = ""
    while True:
        data = conn.recv(4096).decode()
        print(data)

        try:
            if gameId in games:
                game = games[gameId]
                print(game)

                if not data:
                    print("nodata")
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print("Lost connention")
    try:
        del games[gameId]
        print("Closing game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game....")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_inter, (conn, p, gameId))
