import socket

HOST = 'localhost'
PORT = 8080

def handle_request(client_socket):
    """ Gets, process the recieved socket and sends the response """

    request_data = client_socket.recv(1024).decode('utf-8')
    if not request_data:
        return

    path = request_data.split()[1]
    print("Requested:", path)

    # Handle css and js links
    if ".css" in path:
        with open(path[1:], "r", encoding="utf-8") as f:
            content = f.read()
            response_data = 'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n{}'.format(content)
    elif ".js" in path:
        with open(path[1:], "r", encoding="utf-8") as f:
            content = f.read()
            response_data = 'HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\n\r\n{}'.format(content)

    # Server routing
    elif path == '/':
        with open('./templates/index.html', 'r', encoding="utf-8") as file:
            content = file.read()

        response_data = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{}'.format(content)
    else:
        response_data = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n404 Not Found'

    # Sends the response
    client_socket.send(response_data.encode('utf-8'))

    
def run_server():
    """ Runs the server """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print("Serving on http://{0}:{1}".format(HOST, PORT))

    while True:
        client_socket, addr = server_socket.accept()
        with client_socket:
            handle_request(client_socket)

if __name__ == "__main__":
    run_server()
