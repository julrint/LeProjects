from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# Global CONSTANTS
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512    # Buffer size for message handling

# Global Variables
persons = []    # List to store connected Person instances
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)  # set up server

def broadcast(msg, name):
    """
    Send message to all clients.

    Args:
        msg (bytes): The message to be broadcast.
        name (str): The name of the sender.
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[ERROR] Error broadcasting message: ", e)


def client_communication(person):
    """
    Thread to handle all messages from client.

    Args:
        person (Person): The Person instance representing the client.
    """
    client = person.client

    
    # get person's name 
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)

    # Broadcast welcome message
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")  # broadcast welcome message

    
    while True:     
        # Wait for any messages from person
        msg = client.recv(BUFSIZ)

        if msg != bytes("{quit}", "utf8"):
            # Broadcast the message to all clients            
            broadcast(msg, name + ": ")  # Broadcast the message to all clients
            print(f"{name}: ", msg.decode("utf8"))
        else:   
            # Otherwise send mesesage to other clients
            client.close()
            persons.remove(person)
            broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
            print(f"[DISCONNECTED] {name} disconnected")
            break

# loop and wait for connections from different clients
def wait_for_connection():
    """
    Wait for connection from new clients, start new thread once connected.
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)

            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[FAILURE]", e)
            run = False

    print("SERVER CRASHED")




if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # listen for connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()