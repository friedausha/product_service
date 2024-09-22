# import atexit
# import json
# import socket
# import time
# from audioop import error
#
# from django.middleware.common import logger
# from requests import ConnectionError
# from gevent.event import AsyncResult
# # TO DO: find how gevent works
# # from gevent.pool import Pool
#
# from product_service.settings import USER_SERVICE
# class TCPConnectionPool:
#     def __init__(self, address, pool_size):
#         self.address = address
#         # self.pool = Pool(pool_size)
#         self.pool_size = pool_size
#         self.connections = []
#
#     def create_connection(self):
#         conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         # print ('creating connection')
#         try:
#             # print ('about to connect')
#             # print (self.address)
#             conn.connect(address=self.address)
#             conn.settimeout(10)
#             # print ('connection created')
#             # print (conn)
#             return conn
#         except ConnectionError as e:
#             logger.error("Unexpected error occurred: %s", e)
#             print (e)
#             return None
#         # conn.connect(address=self.address)
#         # conn.settimeout(10)
#         # return conn
#
#     def get_connection(self):
#         if self.connections:
#             # print ('reuse connection')
#             return self.connections.pop()
#         else:
#             return self.create_connection()
#
#     def return_connection(self, conn):
#         if len(self.connections) < self.pool_size:
#             self.connections.append(conn)
#         else:
#             conn.shutdown(socket.SHUT_WR)
#
#     def close(self):
#         for conn in self.connections:
#             conn.close()
#
#
# pool_size = 500
# pool = TCPConnectionPool(USER_SERVICE, pool_size)
# atexit.register(pool.close)
#
# # connection = pool.get_connection()
#
# def send_tcp_command(command, data):
#     # print (data)
#     try:
#         payload = "{command} {data}\n".format(command=command, data=data)
#
#         # Get a connection from the pool
#         sock = pool.get_connection()
#         # print ('Sending payload to Golang at: %s', time.time())
#         time_req = time.time()
#         try:
#             # print ('Sending payload to Golang at: %s', time_req)
#             # Send the payload to the server
#             sock.sendall(payload.encode('utf-8'))
#             # print ('Sent payload to Golang at: %s', time.time())
#             # Receive the response
#             response = sock.recv(1024).decode('utf-8')
#             # print ('Received response from Golang at: %s', time.time())
#             # print ('response')
#             time_resp = time.time()
#             #if 'token' not in response:
#             #    print ('Request completed in {} milliseconds {}'.format((time_resp - time_req) * 1000, response))
#             print ('Request completed in {} milliseconds'.format((time_resp - time_req) * 1000))
#             # return json.loads(response)
#             # print (response)
#             return json.loads(response)
#         except Exception as e:
#             return {"error": "Socket error: " + str(e)}
#         finally:
#             # Return the connection to the pool
#             pool.return_connection(sock)
#
#     except socket.timeout:
#         # logger.error('Connection timed out when sending command: %s', command)
#         return {"error": "Connection timed out"}
#

import atexit
import json
import socket
import time

from django.db.transaction import get_connection
from gevent import monkey, pool, lock, spawn, joinall
from django.middleware.common import logger
from product_service.settings import USER_SERVICE

monkey.patch_all()

class TCPConnectionPool:
    def __init__(self, address, size, connection_timeout=15, retry_attempts=3):
        self.address = address
        self.pool = pool.Pool(size)  # gevent Pool
        self.pool_size = size
        self.connections = []
        self.lock = lock.Semaphore(size)  # Semaphore to ensure thread-safe access to the connections list
        self.connection_timeout = connection_timeout
        self.retry_attempts = retry_attempts

    def create_connection(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            conn.settimeout(self.connection_timeout)
            conn.connect(self.address)
            return conn
        except Exception as e:
            logger.error("Error creating connection: %s", e)
            return None

    def get_connection(self):
        with self.lock:
            if self.connections:
                # print ("Reusing an existing connection.")
                return self.connections.pop()
            else:
                # print ("Creating a new connection (pool empty).")
                return self.create_connection()

    def return_connection(self, conn):
        if len(self.connections) < self.pool_size:
            self.connections.append(conn)
        else:
            conn.shutdown(socket.SHUT_WR)
            conn.close()

    def close(self):
        with self.lock:
            for conn in self.connections:
                if conn:
                    conn.close()

pool_size = 500
connection_pool = TCPConnectionPool(USER_SERVICE, pool_size)
atexit.register(connection_pool.close)
def send_tcp_command(command, data):
    retry_count = 0
    max_retries = 3
    while retry_count < max_retries:
        try:
            greenlet = connection_pool.pool.spawn(_send_command_task, command, data)
            return greenlet.get()
        except socket.timeout:
            retry_count += 1
            logger.error("Connection timed out. Retrying... ({}/{})".format(retry_count, max_retries))
        except socket.error as e:
            retry_count += 1
            logger.error("Socket error: {}. Retrying... ({}/{})".format(e, retry_count, max_retries))

    return {"error": "Connection failed after retries"}

def _send_command_task(command, data):
    try:
        payload = "{command} {data}\n".format(command=command, data=data)
        sock = connection_pool.get_connection()
        if not sock:
            return {"error": "Connection failed"}

        time_req = time.time()
        logger.info("Sending payload at {}".format(time_req))
        try:
            sock.sendall(payload.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            time_resp = time.time()
            logger.info('Request completed in {} milliseconds'.format((time_resp - time_req) * 1000))
            return json.loads(response)
        except (socket.timeout, socket.error) as e:
            logger.error("Socket error: {}".format(e))
            return None
        finally:
            connection_pool.return_connection(sock)
    except Exception as e:
        logger.error("Unexpected error: {}".format(e))
        return None
