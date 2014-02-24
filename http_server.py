import os
import socket
from email.utils import formatdate
from mimetypes import guess_type


def run_server(root_dir):
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
                file_type, body = map_URI(root_dir, uri)
                response = build_response(200, file_type, body)
            except MethodNotAllowedError:
                response = build_response(405, "text/html")
            except NotFoundError:
                response = build_response(404, "text/html")
            except:
                response = build_response(500, "text/html")
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


def map_URI(root, uri):
    filename = root + uri
    if os.path.isfile(filename):
        content_type = guess_type(filename)[0]
        with open(filename, 'rb') as filein:
            bytes_read = filein.read()
    elif os.path.isdir(filename):
        content_type = "text/plain"
        bytes_read = uri
        while bytes_read.endswith('/'):
            bytes_read = bytes_read[:-1]
        for i in os.listdir(filename):
            bytes_read += '\r\n\t' + i
    else:
        raise NotFoundError("Not found")
    return (content_type, bytes_read)


def build_response(code, file_type, body=''):
    code_table = {
        200: 'OK',
        404: 'Not found',
        405: 'Method not allowed',
        500: 'Some idiot built this server incorrectly'
        }
    response = []
    response.append("HTTP/1.1 %d %s" % (code, code_table[code]))
    response.append('Date: %s' % formatdate(usegmt=True))
    response.append("Content-Type: %s" % file_type)
    if code != 200:
        body += "<!DOCTYPE html>\n<html>\n<body>\n<h1>" + str(code) +\
            " Error: " + code_table[code] + "</h1>\n</body>\n</html>\n\n"
    response.append(("Content-Length: %d" % len(body)))
    response.append('') 
    response.append(body)
    return '\r\n'.join(response)


class ExceptionTemplate(Exception):
    def __call__(self, *args):
        return self.__class__(*(self.args + args))


class MethodNotAllowedError(ExceptionTemplate):
    pass


class NotFoundError(ExceptionTemplate):
    pass


if __name__ == '__main__':
    run_server("webroot")
