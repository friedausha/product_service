# # utils/tcp_client.py
# import json
# import socket
# import time
# from contextlib import contextmanager
#
# from django.middleware.common import logger
# from product_service.settings import USER_SERVICE
# @contextmanager
# def tcp_socket_connection(address, timeout=60):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.settimeout(timeout)
#     try:
#         sock.connect(address)
#         yield sock
#     except socket.timeout:
#         logger.error('Connection timed out after %s seconds.', timeout)
#         raise
#     except socket.error as e:
#         logger.error('Socket error: %s', e)
#         raise
#     # TO DO: Investigate this
#     finally:
#         try:
#             sock.shutdown(socket.SHUT_RDWR)  # Gracefully shut down the connection
#         except socket.error:
#             pass
#         sock.close()
# def send_tcp_command(command, data):
#     # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # sock.settimeout(10)  # Set a 5-second timeout
#     # Format the payload as a string
#     try:
#         payload = "{command} {data}\n".format(command=command, data=data)
#     # Use the context manager to open and manage the socket connection
#         with tcp_socket_connection(USER_SERVICE) as sock:
#             # print ("Sending payload to Golang at: %s", time.time())
#             # Send the payload to the server
#             sock.sendall(payload.encode('utf-8'))
#             # Receive the response
#             response = sock.recv(1024).decode('utf-8')
#             # print ("Received response from Golang at: %s", time.time())
#
#             return json.loads(response)
#
#     except socket.timeout:
#         logger.error('Connection timed out when sending command: %s', command)
#         return {"error": "Connection timed out"}
#
#     except socket.error as e:
#         logger.error("Socket error occurred: %s", e)
#         return {"error": "Socket error: " + str(e)}
#
#     except Exception as e:
#         logger.error("Unexpected error occurred: %s", e)
#         return {"error": "Unexpected error: " + str(e)}
#
import atexit
import json
import socket
import time
from audioop import error

from django.middleware.common import logger
from requests import ConnectionError
from gevent.event import AsyncResult
# TO DO: find how gevent works
# from gevent.pool import Pool

from product_service.settings import USER_SERVICE
class TCPConnectionPool:
    def __init__(self, address, pool_size):
        self.address = address
        # self.pool = Pool(pool_size)
        self.pool_size = pool_size
        self.connections = []

    def create_connection(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print ('creating connection')
        try:
            # print ('about to connect')
            # print (self.address)
            conn.connect(address=self.address)
            conn.settimeout(10)
            # print ('connection created')
            # print (conn)
            return conn
        except ConnectionError as e:
            logger.error("Unexpected error occurred: %s", e)
            print (e)
            return None
        # conn.connect(address=self.address)
        # conn.settimeout(10)
        # return conn

    def get_connection(self):
        if self.connections:
            # print ('reuse connection')
            return self.connections.pop()
        else:
            return self.create_connection()

    def return_connection(self, conn):
        if len(self.connections) < self.pool_size:
            self.connections.append(conn)
        else:
            conn.shutdown(socket.SHUT_WR)

    def close(self):
        for conn in self.connections:
            conn.close()


pool_size = 500
pool = TCPConnectionPool(USER_SERVICE, pool_size)
atexit.register(pool.close)

# connection = pool.get_connection()

def send_tcp_command(command, data):
    # print (data)
    try:
        payload = "{command} {data}\n".format(command=command, data=data)

        # Get a connection from the pool
        sock = pool.get_connection()
        # print ('Sending payload to Golang at: %s', time.time())
        time_req = time.time()
        try:
            # print ('Sending payload to Golang at: %s', time_req)
            # Send the payload to the server
            sock.sendall(payload.encode('utf-8'))
            # print ('Sent payload to Golang at: %s', time.time())
            # Receive the response
            response = sock.recv(1024).decode('utf-8')
            # print ('Received response from Golang at: %s', time.time())
            # print ('response')
            time_resp = time.time()
            #if 'token' not in response:
            #    print ('Request completed in {} milliseconds {}'.format((time_resp - time_req) * 1000, response))
            print ('Request completed in {} milliseconds'.format((time_resp - time_req) * 1000))
            # return json.loads(response)
            # print (response)
            return json.loads(response)
        except Exception as e:
            return {"error": "Socket error: " + str(e)}
        finally:
            # Return the connection to the pool
            pool.return_connection(sock)

    except socket.timeout:
        # logger.error('Connection timed out when sending command: %s', command)
        return {"error": "Connection timed out"}

