import sys
import zmq

if len(sys.argv) != 2:
    raise Exception('wrong number of arguments')

client_reader_port = int(sys.argv[0])

context = zmq.Context()

client_reader_socket = context.socket(zmq.SUB)
client_reader_socket.connect(f'tcp://localhost:{client_reader_port}')
client_reader_socket.setsockopt_string(zmq.SUBSCRIBE, '')
client_reader_socket.RCVTIMEO = 100

try:
    while True:
        try:
            while True:
                message = client_reader_socket.recv_string()
                print(message)
        except zmq.Again:
            pass
except KeyboardInterrupt:
    print('Exiting...')
    sys.exit(0)
