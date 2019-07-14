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
        # Custom logging handler for systemd formatted output
        root_logger = logging.getLogger()
        root_logger.setLevel("INFO")
        root_logger.addHandler(SystemdHandler())
        # Set up non-blocking socket safely for restarts if we crash
        socket.setdefaulttimeout(60)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setblocking(0)

        try:
            # Init server bindings and queue dicts
            server.bind(('', port))
            server.listen(5)
            inputs = [server]
            outputs = []
            data_queues = {}
            message_queues = {}
            responses = {}
            logging.info('Listening on port: ' + str(port))
        except socket.error:
            # This shouldn't happen with SO_REUSEADDR
            logging.error('Bind failed.')
            sys.exit(1)

        while inputs:
            try:
                readable, writable, exceptional = select.select(
                    inputs, outputs, inputs)
                for s in readable:
                    if s is server:
                        # Each connection gets a unique set of queues
                        connection, client_address = s.accept()
                        connection.setblocking(0)
                        inputs.append(connection)
                        message_queues[connection] = Queue.Queue()
                        data_queues[connection] = Queue.Queue()
                        responses[connection] = Messages()
                        logging.info('New connection from ' + str(client_address[0]))
                        connection.send(Messages.MSG_CONNECT)
                        connection.send(Messages.MSG_NEWLINE)
                        connection.send(Messages.MSG_PROMPT)
                    else:
                        try:
                            incoming = s.recv(1024)
                            if incoming:
                                try:
                                    # data will continue to stream until the
                                    # connection is broken by the client
                                    data = data_queues[s].get_nowait()
                                except Queue.Empty:
                                    # when the client disconnects, we use
                                    # an empty bytearray to do cleanup
                                    data = bytearray(b'')
                                # if the incoming data exceeds 1024 bytes
                                # we keep extending as it comes
                                data.extend(incoming)
                                # if we find a newline, we know a full set
                                # of instructions have been passed. Parse.
                                if b'\n' in data:
                                    parts = data.split(b'\n')
                                    message_queues[s].put(parts[0])
                                    # keep the leftovers for the next message
                                    data = parts[1]
                                # store the completed instruction in data queue
                                data_queues[s].put(data)
                                # if this is our first data from a new
                                # connection, initialize the output for writing
                                if s not in outputs:
                                    outputs.append(s)
                            else:
                                # cleanup everything if the client disconnected
                                if s in outputs:
                                    outputs.remove(s)
                                inputs.remove(s)
                                s.close()
                                del message_queues[s]
                                del data_queues[s]
                                del responses[s]
                        except:
                                # cleanup everything if we have an error
                                if s in outputs:
                                    outputs.remove(s)
                                inputs.remove(s)
                                s.close()
                                del message_queues[s]
                                del data_queues[s]
                                del responses[s]

                for s in writable:
                    try:
                        # get any messages waiting for client from queue
                        next_msg = message_queues[s].get_nowait()
                    except Queue.Empty:
                        # if client disconnected, remove them from our list
                        outputs.remove(s)
                    else:
                        # send message to client
                        try:
                            resp, next = responses[s].check(next_msg)
                        except:
                            resp = ''
                        else:
                            if resp:
                                if (resp == Messages.CODE_ERROR.encode('utf-8')):
                                    s.send(Messages.MSG_ERROR)
                                    s.send(Messages.MSG_NEWLINE)
                                elif (resp == Messages.CODE_EXIT.encode('utf-8')):
                                    if s in outputs:
                                        outputs.remove(s)
                                    inputs.remove(s)
                                    s.close()
                                    del message_queues[s]
                                    del data_queues[s]
                                    del responses[s]
                                    break
                                else:
                                    s.send(resp)
                                    s.send(Messages.MSG_NEWLINE)
                            if next:
                                try:
                                    message_queues[s].put(bytes(next, 'utf-8'))
                                except:
                                    # probably a weird string like ` that broke
                                    # user input. Just ignore it.
                                    pass
                            else:
                                s.send(Messages.MSG_PROMPT)


                for s in exceptional:
                    # if errors, clean everything up
                    inputs.remove(s)
                    if s in outputs:
                        outputs.remove(s)
                    s.close()
                    del message_queues[s]
                    del data_queues[s]
                    del responses[s]

            # if we hit an error, close things down cleanly
            except KeyboardInterrupt:
                server.shutdown(2)
                server.close()
                logging.info('Shutting down socket connection.')
                sys.exit(1)
            except Exception as err:
                server.shutdown(2)
                server.close()
                logging.info('Shutting down socket connection.')
                # any error except ctrl-c should be raised for debugging
                raise err

# start the app on port 1822
if __name__ == '__main__':
    Allegra(1822)
