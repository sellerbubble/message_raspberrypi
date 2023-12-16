import cv2
import zmq
import base64
import numpy as np


class get_pic():
    def __init__(self,flag=0):
        if flag == 0:
            self.open_tcp()
            self.open_tcp_local()
        else:
            self.open_tcp_action()
    def open_tcp(self):
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PAIR)
        self.footage_socket.bind('tcp://*:5555')
    def open_tcp_local(self):
        context_2 = zmq.Context()
        self.footage_socket_2 = context_2.socket(zmq.PAIR)
        self.footage_socket_2.connect('tcp://localhost:5000')

    def open_tcp_action(self):
        context_2 = zmq.Context()
        self.footage_socket_2 = context_2.socket(zmq.PAIR)
        self.footage_socket_2.connect('tcp://localhost:4000')
    def open_window(self):
        cv2.namedWindow('Stream', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)

    def get_pic(self):
        print("监听中")
        self.frame = self.footage_socket.recv()  # 接收TCP传输过来的一帧视频图像数据
        # print(type(self.frame))
        img = base64.b64decode(self.frame)  # 把数据进行base64解码后储存到内存img变量中
        # print(type(img))
        npimg = np.frombuffer(img, dtype=np.uint8)  # 把这段缓存解码成一维数组
        # print(type(npimg))
        self.source = cv2.imdecode(npimg, 1)  # 将一维数组解码为图像source
        # print(type(self.source))


    def show_pic(self):
        cv2.imshow("Stream", self.source)  # 把图像显示在窗口中
        cv2.waitKey(5)

    # 注意是从本地接受str
    def get_str(self):
        self.action = self.footage_socket_2.recv_string()
        print(self.action)

    # def send_str(self, action):
    #     print(1)
    #     self.footage_socket.send_string(self.action)

    def send_str(self):
        try:
            self.footage_socket.send_string('1')
        except Exception as e:
            print(f"Error sending string: {e}")

    def open_tcp_local(self):
        context_2 = zmq.Context()
        self.footage_socket_2 = context_2.socket(zmq.PAIR)
        self.footage_socket_2.connect('tcp://localhost:5000')

    def send_pic(self):
        self.footage_socket_2.send(self.frame)


if __name__ == '__main__':
    pic = get_pic()
    get_action = get_pic(1)
    pic.open_window()
    while True:
        pic.get_pic()
        pic.show_pic()
        pic.send_pic()
        get_action.footage_socket_2.setsockopt(zmq.RCVTIMEO,10)
        try:
            get_action.get_str()
            get_action.footage_socket.send_string(get_action.action)
            print(get_action.action)
        except:
            pass
        #pic.footage_socket.send_string('1')