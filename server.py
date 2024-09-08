import os.path
import socket
import sys
import time
from _thread import *
import pickle
import random

from objects.entities.buff import InvisibilityBuff, SpeedBuff, JumpBuff
from objects.entities.bullets import Bullet, BlowingBullet
from objects.map.map import Map
import tkinter as tk
from tkinter import filedialog
from os.path import join

from objects.entities.player import Player
from other.wrapper import Wrap
from other.constants import ROOT
from physics.vec2 import Vec2


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = False
        self.free_id = 0

        self.map_lines = None
        self.map = Map()

        self.players = dict()
        self.entities_to_send = dict()  # key - to whom player
        self.socket = None
        self.clock = None
        self.current_team = -1
        self.mode = 0

    def run(self):
        if self.map_lines is None:
            return
        self.clock = time.time()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.ip, self.port))
        except socket.error as e:
            str(e)
        self.socket.listen(2)
        print("Waiting for a connection, Server Started")

        self.running = True
        start_new_thread(self.spawn_buffs, ())
        start_new_thread(self.start_event, ())
        server_status.config(text="Server is running")
        while self.running:
            try:
                conn, addr = self.socket.accept()
                print("Connected to:", addr)
                start_new_thread(self.client, (conn,))
            except socket.error:
                pass
        print("Server stopped")
        server_status.config(text="Server is not running")
        self.free_id = 0
        self.players = dict()
        self.entities_to_send = dict()

    def stop(self):
        self.running = False
        if self.socket is not None:
            self.socket.close()

    def client(self, conn):
        print(self.current_team)
        identifier = self.free_id
        conn.send(pickle.dumps((identifier, self.map_lines, self.current_team)))
        if self.current_team != -1:
            self.current_team = (self.current_team + 1) % 2

        self.entities_to_send[identifier] = []
        self.free_id += 1
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                type = getattr(sys.modules[__name__], data.type)
                if issubclass(type, Player):
                    data.id = identifier
                    self.players[identifier] = data
                elif issubclass(type, Bullet):
                    for player_key in self.entities_to_send.keys():
                        if player_key != identifier:
                            self.entities_to_send[player_key].append(data)
                if not data:
                    print("Disconnected")
                    break

                reply = []
                for key, item in self.players.items():
                    if key != identifier:
                        reply.append(item)
                reply += self.entities_to_send[identifier]
                self.entities_to_send[identifier].clear()
                conn.sendall(pickle.dumps(reply))
            except Exception:
                break

        print("Lost connection")
        conn.close()
        self.players.pop(identifier)

    def select_map(self):
        file_path = filedialog.askopenfilename(
            initialdir=join("assets", "maps"), filetypes=(("TXT files", "*.txt"),)
        )
        with open(file_path, "r") as f:
            self.map_lines = f.readlines()
        map_name.config(text=f"Map: {os.path.basename(file_path)}")
        self.map.load_from_list(self.map_lines, w_sprites=False)

    def spawn_buffs(self):
        while self.running:
            all_blocks = self.map.blocks.keys()
            random_blocks = random.sample(sorted(all_blocks), len(all_blocks) // 30 + 1)
            for block in random_blocks:
                block_above = (
                    block[0],
                    block[1] - self.map.tile_size,
                )
                if block_above not in all_blocks:
                    type = random.choice([InvisibilityBuff, SpeedBuff, JumpBuff])
                    sprite = None
                    if type == InvisibilityBuff:
                        sprite = join(
                            "assets",
                            "buffs",
                            "invisibility_buff.png",
                        )
                    elif type == SpeedBuff:
                        sprite = join("assets", "buffs", "speed_buff.png")
                    elif type == JumpBuff:
                        sprite = join("assets", "buffs", "jump_buff.png")
                    buff = type(
                        block_above[0],
                        block_above[1],
                        self.map.tile_size,
                        self.map.tile_size,
                        300,
                        sprite_path=sprite,
                    )
                    for arr in self.entities_to_send.values():
                        arr.append(Wrap(buff))
                    break
            time.sleep(4)

    def start_event(self):
        while True:
            time.sleep(random.random() * 10 + 50)
            for i in range(10):
                x = (random.random()) * 5000
                y = -500
                size = random.random() * 150
                meteor = BlowingBullet(
                    x, y, size, size, 150, join(ROOT, "assets", "bullets", "meteor.png")
                )
                meteor.radius = 350
                meteor.velocity = Vec2(-20, 20)
                time.sleep(0.1)
                for arr in self.entities_to_send.values():
                    arr.append(Wrap(meteor))

    def change_mode(self):
        self.mode = (self.mode + 1) % 2
        if self.mode == 0:
            mode.config(text="Single mode")
            self.current_team = -1
        else:
            mode.config(text="Team mode")
            self.current_team = 0


server = Server("localhost", 8686)

root = tk.Tk()
root.geometry("500x500")
root.title("Server")  # заголовок


tk.Label(root, text=f"ip: {server.ip}").pack(anchor="n")
tk.Label(root, text=f"port: {server.port}").pack(anchor="n")
map_name = tk.Label(root, text="Map: ")
map_name.pack(anchor="n")


def start():
    if not server.running:
        start_new_thread(server.run, ())


start_server_button = tk.Button(
    root, text="Start server", command=lambda: start_new_thread(server.run, ())
)
start_server_button.pack(anchor="n")

stop_server_button = tk.Button(root, text="Stop server", command=server.stop)
stop_server_button.pack(anchor="n")

select_map_button = tk.Button(root, text="Select map", command=server.select_map)
select_map_button.pack(anchor="n")

select_map_button = tk.Button(root, text="Change mode", command=server.change_mode)
select_map_button.pack(anchor="n")

server_status = tk.Label(root, text="Server is not running")
server_status.pack(anchor="n")

mode = tk.Label(root, text="Single mode")
mode.pack(anchor="n")

path = join("assets", "maps")
for i in os.listdir(path):
    print(i)
    if os.path.isfile(f"{path}/{i}"):
        map_name.config(text=f"Map: {os.path.basename(i)}")
        with open(f"{path}/{i}", "r") as f:
            server.map_lines = f.readlines()
            print(server.map_lines, i)
        break
server.map.load_from_list(server.map_lines, w_sprites=False)


root.mainloop()  # отображение окна
