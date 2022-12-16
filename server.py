import sys
import zmq
import threading
import time



if len(sys.argv) != 3:
    raise Exception('wrong number of arguments')

writer_client_port, reader_client_port = map(int, sys.argv[1:])
INTERNAL_DURATION = 5.0

context = zmq.Context() 

writer_client_socket = context.socket(zmq.SUB)
writer_client_socket.bind(f'tcp://*:{writer_client_port}')
writer_client_socket.RCVTIMEO = 100
writer_client_socket.setsockopt_string(zmq.SUBSCRIBE, '')

reader_client_socket = context.socket(zmq.PUB)
reader_client_socket.bind(f'tcp://*:{reader_client_port}')

data = {}
time_diff = time.time()

try: 
    while True:
        try:
            received_message = writer_client_socket.recv_string()
            print(f"Received request: {received_message}") 
            name, message = received_message.split(':')
            if data.get(name) == None:
                data[name] = 1
            else: 
                data[name] = data.get(name) + 1
            reader_client_socket.send_string(received_message)
        except zmq.Again:
            pass 
        current = time.time()
        if current - time_diff  > INTERNAL_DURATION:
            summary = "SUMMARY:"
            for i in sorted(data.keys()):
                summary += f'\n\t{i}: {data[i]}'
                data[i] = 0
            reader_client_socket.send_string(summary)
            time_diff = current
except KeyboardInterrupt:
    print('Shutting down...')
    sys.exit(0)
