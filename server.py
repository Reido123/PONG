# Adding the required libraries
import socket
import pickle
import threading

# Initializing global parameters
HOST = 'localhost'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a socket object for communication using IPv4 and the TCP protocol (SOCK_STREAM)
server.bind((HOST, PORT))  # Binds the socket to a specific machine (localhost) and port (5555)
server.listen()  # Listens for incoming connections

# Defining the dimensions of the paddle (paddle_width, paddle_height) and the game window (width, height)
paddle_width, paddle_height = 20, 100
width, height = 800, 600

clients = []  # List storing connected clients

paddle_positions = [height // 2 - paddle_height // 2, height // 2 - paddle_height // 2]  # Initial paddle positions on the Y-axis

# This function runs in a separate thread for each connected client.
# It continuously receives the paddle position from the client and sends the opponent's position.
def handle_client(client, player_id):
    global clients, paddle_positions

    try:
        while True:
          
            data = client.recv(1024)
            if not data:
                break
            paddle_positions[player_id] = pickle.loads(data)

        
            opponent_paddle_position = paddle_positions[1 - player_id]
            client.send(pickle.dumps(opponent_paddle_position))
    except:
        pass
    finally:
    
        clients.remove(client)
        client.close()

# Waits for two clients to connect to the server.
# Once a client connects, it sends them their player ID and starts a separate thread to handle the client using the handle_client function.
while len(clients) < 2:
    client, addr = server.accept()
    clients.append(client)
    player_id = len(clients) - 1

    # Sending the player ID to the client
    client.send(pickle.dumps(player_id))

    # Initializing a thread to handle the client
    thread = threading.Thread(target=handle_client, args=(client, player_id))
    thread.start()
