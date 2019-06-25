#!/usr/bin/env python3

import logging
import sys
import time
import socket
import select
import queue as Queue
from systemdhandler import SystemdHandler
from messages import Messages

class Allegra():
    def __init__(self, port):
        root_logger = logging.getLogger()
        root_logger.setLevel("INFO")
        root_logger.addHandler(SystemdHandler())
        socket.setdefaulttimeout(60)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setblocking(0)

        try:
            server.bind(('', port))
            server.listen(5)
            inputs = [server]
            outputs = []
            data_queues = {}
            message_queues = {}
            responses = {}
            logging.info('Listening on port: ' + str(port))
        except socket.error:
            logging.error('Bind failed.')
            sys.exit(1)

        while inputs:
            try:
                readable, writable, exceptional = select.select(
                    inputs, outputs, inputs)
                for s in readable:
                    if s is server:
                        connection, client_address = s.accept()
                        connection.setblocking(0)
                        inputs.append(connection)
                        message_queues[connection] = Queue.Queue()
                        data_queues[connection] = Queue.Queue()
                        responses[connection] = Messages()
                        logging.info('New connection from ' + str(client_address[0]))
                    else:
                        incoming = s.recv(1024)
                        if incoming:
                            try:
                                data = data_queues[s].get_nowait()
                            except Queue.Empty:
                                data = bytearray(b'')
                            data.extend(incoming)
                            if b'\n' in data:
                                parts = data.split(b'\n')
                                message_queues[s].put(parts[0])
                                data = parts[1]
                            data_queues[s].put(data)
                            if s not in outputs:
                                outputs.append(s)
                        else:
                            if s in outputs:
                                outputs.remove(s)
                            inputs.remove(s)
                            s.close()
                            del message_queues[s]
                            del data_queues[s]
                            del responses[s]

                for s in writable:
                    try:
                        next_msg = message_queues[s].get_nowait()
                    except Queue.Empty:
                        outputs.remove(s)
                    else:
                        s.send(responses[s].check(next_msg))

                for s in exceptional:
                    inputs.remove(s)
                    if s in outputs:
                        outputs.remove(s)
                    s.close()
                    del message_queues[s]
            except KeyboardInterrupt:
                server.shutdown(2)
                server.close()
                logging.info('Shutting down socket connection.')
                sys.exit(1)
            except Exception as err:
                server.shutdown(2)
                server.close()
                logging.info('Shutting down socket connection.')
                raise err

if __name__ == '__main__':
    Allegra(1822)
