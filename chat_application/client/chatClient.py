from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock

class Client:
    HOST = "192.168.0.21"
    PORT = 5500
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self, name):
        """
        Initialize a Client object.

        Args:
            name (str): The name of the client.
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []  # List to store received messages
        self.lock = Lock()  # Thread lock to ensure thread safety

        # Start a separate thread to continuously run the receive_messages method
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()

        # Send the client's name to the server
        self.send_message(name)

    def receive_messages(self):
        """
        Receive messages from the server.
        """
        while True:
            try:
                # Attempt to receive a message from the server
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                # Acquire the lock, append the message to the list, and release the lock
                with self.lock:
                    self.messages.append(msg)
            except Exception as e:
                # Print an exception message and break out of the loop if an exception occurs
                print("[EXCEPTION]", e)
                break

    def send_message(self, msg):
        """
        Send a message to the server.

        Args:
            msg (str): The message to be sent.
        """
        try:
            # Send the message to the server
            self.client_socket.send(bytes(msg, "utf8"))

            # If the message is "{quit}", disconnect the client
            if msg == "{quit}":
                self.disconnect()
        except Exception as e:
            # Print an error message, reconnect to the server, and handle the error
            print("[ERROR] Error sending message:", e)
            self.reconnect()

    def get_messages(self):
        """
        Get a copy of received messages and clear the original list.

        Returns:
            list[str]: List of received messages.
        """
        with self.lock:
            messages_copy = self.messages[:]  # Create a copy of the list
            self.messages = []  # Clear the original list
        return messages_copy

    def disconnect(self):
        """
        Disconnect the client by sending a "{quit}" message to the server.
        """
        self.send_message("{quit}")

    def reconnect(self):
        """
        Reconnect to the server by creating a new socket and connecting.
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        print("[INFO] Reconnected to the server.")
