import os
import socket
from email.utils import formatdate
from mimetypes import guess_type


def run_server():
    # Socket set-up
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP
        )
    try:
        address = ('127.0.0.1', 50000)
        server_socket.bind(address)
        server_socket.listen(1)

        while True:
            try:
                conn, client_address = server_socket.accept()
                rq = gather_request(conn)
                uri = parse_request(split_off_first_line(rq))
                resource_file = map_URI(uri)
                response = build_response(200, resource_file)
            except MethodNotAllowedError:
                response = build_response(405, "Method not allowed")
            except NotFoundError:
                response = build_response(404, "Not found")
            finally:
                conn.sendall(response)
                conn.shutdown(socket.SHUT_WR)
                conn.close()

    finally:
        server_socket.close()


def gather_request(conn):
    accu = ''
    while True:
        buff = conn.recv(32)
        accu += buff
        if accu[-4:] == "\r\n\r\n":
        # if not buff:
            conn.shutdown(socket.SHUT_RD)
            return accu


def split_off_first_line(request):
    return request.split('\r\n')[0]


def parse_request(header):
    word_list = header.split()
    if word_list[0] != 'GET':
        raise MethodNotAllowedError("Method not allowed")
    return word_list[1]


def map_URI(uri):
    filepath = "webroot%s" % uri
    if os.path.isfile(filepath) or os.path.isdir(filepath):
        return filepath
    raise NotFoundError("Not found")


def build_response(code, resource_file):
    code_table = {200: 'OK', 404: 'Not found', 405: 'Method not allowed'}
    h1 = "HTTP/1.1 %d %s" % (code, code_table[code])
    h2 = 'Date: %s' % formatdate(usegmt=True)
    if code == 200:
        file_type = guess_type(resource_file)[0]
        if file_type:
            h3 = "Content-Type: %s" % file_type
            with open(resource_file, 'rb') as filein:
                long_string = filein.read()
        else:
            h3 = "Content-Type: text/plain"
            long_string = resource_file[7:]
            for i in os.listdir(resource_file):
                long_string += '\r\n\t' + i
    else:
        h3 = "Content-Type: text/html"
        long_string = "<!DOCTYPE html>\n<html>\n<body>\n<h1>" + str(code) +\
            " Error: " + code_table[code] + "</h1>\n</body>\n</html>\n\n"
    h4 = "Content-Length: " + str(len(long_string))
    return '%s\r\n%s\r\n%s\r\n%s\r\n\r\n%s' % (h1, h2, h3, h4, long_string)


class ExceptionTemplate(Exception):
    def __call__(self, *args):
        return self.__class__(*(self.args + args))


class MethodNotAllowedError(ExceptionTemplate):
    pass


class NotFoundError(ExceptionTemplate):
    pass


if __name__ == '__main__':
    run_server()
