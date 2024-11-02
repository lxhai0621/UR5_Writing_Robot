import numpy as np
import socket
import time
import struct
import util
import rtde
import os
import re
import pickle
HOST = "192.168.1.108"
PORT = 30003
#home = [-0.32860, 0.64458, -0.31890, 4.508, 0.781, -0.706]
home = [-0.12131, -0.42322, 0.14700, 1.085, 2.718, -2.490]
count = 0
class UR5:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.connect((HOST, PORT))
    def get_current_tcp(self):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((HOST, PORT))
        data = tcp_socket.recv(1108)
        position = struct.unpack('!6d', data[444:492])
        #tcp_socket.close()
        return np.asarray(position)

    def move_to_tcp(self, target_tcp):
        tool_acc = 2
        tool_vel = 4
        tool_pos_tolerance = [0.001, 0.001, 0.001, 0.05, 0.05, 0.05]
        tcp_command = "movel(p[%f,%f,%f,%f,%f,%f],a=1,v=1,t=0,r=0)\n" % (
            target_tcp[0], target_tcp[1], target_tcp[2], target_tcp[3], target_tcp[4],
            target_tcp[5])
        self.tcp_socket.send(str.encode(tcp_command))

        actual_pos = self.get_current_tcp()
        target_rpy = util.rv2rpy(target_tcp[3], target_tcp[4], target_tcp[5])
        rpy = util.rv2rpy(actual_pos[3], actual_pos[4], actual_pos[5])
        while not (all([np.abs(actual_pos[j] - target_tcp[j]) < tool_pos_tolerance[j] for j in range(3)])
                   and all([np.abs(rpy[j] - target_rpy[j]) < tool_pos_tolerance[j + 3] for j in range(3)])):
            actual_pos = self.get_current_tcp()
            rpy = util.rv2rpy(actual_pos[3], actual_pos[4], actual_pos[5])


    def move_down(self):
        tcp = self.get_current_tcp()
        tcp[2] = -0.05371
        self.move_to_tcp(tcp)

    def move_up(self):
        tcp = self.get_current_tcp()
        tcp[2] = 0.14700
        self.move_to_tcp(tcp)

    def go_home(self):
        self.move_to_tcp(home)


#pos = [335.70,-144.43]
#pos = [300.14,-65.30]
pos = [280.14,-90.23]
#pos = [370.43,-110.43]
if __name__ == "__main__":
    with open('Chinese_strokes','rb') as f:
        data = pickle.load(f)

    ur = UR5()
    ur.go_home()
    #ur.move_to_tcp([0.33570, -0.14443, 0.14700, 1.085, 2.718, -2.490])

    ur.move_down()
    ur.move_up()
    ur.move_to_tcp([0.33570,-0.14443,0.14700,1.085,2.718,-2.490])

    sentense = "宁知一水不可渡"
    num = len(sentense)
    width = 85


    for i,word in enumerate(sentense):
        x_pos = pos[0]
        y_pose = width * (i - num / 2 + 1) + pos[1]
        strokes = data[word]
        for st in strokes:
            for po in st:
                x = x_pos + po['y']/10+width
                y = y_pose +po['x']/10 - width+10
                print(x,y)
                ur.move_to_tcp([x/1000,y/1000,-0.05371,1.085,2.718,-2.490])
            ur.move_up()
        ur.go_home()
        ur.move_down()
        ur.move_up()
        #ur.move_down()
        #ur.move_up()
        ur.move_to_tcp([0.33570, -0.14443, 0.14700, 1.085, 2.718, -2.490])
    ur.go_home()

"""
    pos = [444.43,-165.43]
    sentense = "况复万山修且阻"
    num = len(sentense)
    width = 70

    for i, word in enumerate(sentense):
        x_pos = pos[0]
        y_pose = width * (i - num / 2 + 1) + pos[1]
        strokes = data[word]
        for st in strokes:
            for po in st:
                x = x_pos + po['y'] / 10 + width
                y = y_pose + po['x'] / 10 - width + 10
                print(x, y)
                ur.move_to_tcp([x / 1000, y / 1000, -0.05371, 1.085, 2.718, -2.490])
            ur.move_up()
        ur.go_home()
        ur.move_down()
        ur.move_up()
        # ur.move_down()
        # ur.move_up()
        ur.move_to_tcp([0.33570, -0.14443, 0.14700, 1.085, 2.718, -2.490])
"""



