
class tcp_message():
    def __init__(self):
        self.open_tcp()
        self.IP = '172.20.10.5'

    def open_camera(self):
        self.pi = Picamera2()
        config = self.pi.create_preview_configuration()
        self.pi.configure(config)
        self.pi.start_preview(Preview.QTGL)
        self.pi.start()
    def open_tcp(self):
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PAIR)
        self.footage_socket.bind('tcp://*:4000')
        self.footage_socket.connect('tcp://%s:5555' % self.IP)

    def open_window(self):
        cv2.namedWindow('Stream', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)

    def send_pic(self):
        self.pi.capture_file('pic.jpg')

        with open('pic.jpg', 'rb') as file:
            data = file.read()

        jpg_as_test = base64.b64encode(data)  # 把内存中的图像流数据进行base64编码

        # 发送数据
        footage_socket.send(jpg_as_test)

    def show_pic(self):
        cv2.imshow("Stream", self.source)  # 把图像显示在窗口中
        cv2.waitKey(5)

    def get_str(self):
        action = self.footage_socket.recv_string()
        print(action)