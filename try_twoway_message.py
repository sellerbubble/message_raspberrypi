import multiprocessing

import zmq
import time


class node1():
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.bind('tcp://*:5555')

    def send(self):
        msg = f"Message from Node 1, iteration"
        self.socket.send_string(msg)
        time.sleep(1)


class node2():
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.connect('tcp://127.0.0.1:5555')

    def rev(self):
        msg = self.socket.recv_string()
        print(f"Node 2 received: {msg}")
        time.sleep(1)


if __name__ == "__main__":
    # 启动两个节点
    node1 = node1()
    node2 = node2()
    node1.send()
    time.sleep(1)

    node2.rev()
