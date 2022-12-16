import sys
import zmq

if len(sys.argv) != 3:
    raise Exception('wrong number of arguments')

client_inputs_port = int(sys.argv[0])
name = str(sys.argv[1])

context = zmq.Context()

client_inputs_socket = context.socket(zmq.REQ)
client_inputs_socket.connect(f'tcp://localhost:{client_inputs_port}')

try:
    while True:
        message = input("> ")
        if len(message) != 0:
            client_inputs_socket.send_string(f'{name}:{message}')
except KeyboardInterrupt:
    print('Exiting...')
    sys.exit(0)
