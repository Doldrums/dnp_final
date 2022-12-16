import sys
import zmq
import threading
import time



if len(sys.argv) != 3:
    raise Exception('wrong number of arguments')

writer_client_port, reader_client_port = map(int, sys.argv[1:])
INTERNAL_DURATION = 5.0

context = zmq.Context() 

writer_client_socket = context.socket(zmq.REP)
writer_client_socket.bind(f'tcp://*:{writer_client_port}')
writer_client_socket.RCVTIMEO = 100

reader_client_socket = context.socket(zmq.PUB)
reader_client_socket.bind(f'tcp://*:{reader_client_port}')

data = []
time_diff = time.time()

try: 
    while True:
        try:
            received_message = writer_client_socket.recv_string()
            print(f"Received request: {received_message}") 
            name, message = map(received_message.split(':'))
            if data.get(name) == None:
                data[name] = 0
            else: 
                data[name] = data.get(name) + 1
            reader_client_socket.send_string(received_message)
        except zmq.Again:
                continue 
        current = time.time()
        if current - time_diff  > INTERNAL_DURATION:
            summary = f"""SUMMARY:
                  {data}"""
            reader_client_socket.send_string(summary)
            time_diff = current
except KeyboardInterrupt:
    print('Shutting down...')
    sys.exit(0)
