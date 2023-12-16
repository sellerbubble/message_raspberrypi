from get_send_pic import get_pic

if __name__ == '__main__':
    message = get_pic()
    while True:
        message.get_str()
        #message.send_str()
        message.footage_socket.send_string(message.action)
