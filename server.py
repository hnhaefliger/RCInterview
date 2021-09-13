import socket

def parse_request(request):
    '''
    Break down URL.
    (NEEDS TO BE MODIFIED FOR REQUESTS OTHER THAN GET)
    '''
    request = request.split('\n')[0]

    request = request.split(' ')
    request = [request[0]] + request[1].split('?')

    if len(request) > 2:
        request = request[:2] + [{
            line.split('=')[0]: line.split('=')[1] for line in request[2].split('&')
        }]

    return request

SERVER_HOST = 'localhost'
SERVER_PORT = 4000

'''
Initialize socket.
'''
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

'''
Current database.
'''
data = {}

while True:
    client_connection, client_address = server_socket.accept() # Accept incoming connections.

    request = client_connection.recv(1024).decode() # Recieve request.
    request = parse_request(request) # Get relevant info.

    if request[0] == 'GET': # Error handling.
        if request[1] == '/set':
            if len(request) == 3:
                data.update(request[2])
                response = 'HTTP/1.0 201 CREATED\n\n'

            else: 
                response = 'HTTP/1.0 400 BAD REQUEST\n\n'

        elif request[1] == '/get':
            if len(request) == 3:
                response = f'HTTP/1.0 200 OK\n\n{data[request[2]["key"]]}'

            else:
                response = 'HTTP/1.0 400 BAD REQUEST\n\n'

        else:
            response = 'HTTP/1.0 404 NOT FOUND\n\n'

    else:
        response = 'HTTP/1.0 405 Method Not Allowed\n\n'

    client_connection.sendall(response.encode()) # Respond to request
    client_connection.close() # End connection
