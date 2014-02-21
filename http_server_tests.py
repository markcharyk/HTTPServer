from email.utils import formatdate
import unittest
import http_server


class testSplitFirstLine(unittest.TestCase):
    def setUp(self):
        self.input = "GET /index.html HTTP/1.1\r\nmore data more data more data\r\n\r\n"
        self.first_line = "GET /index.html HTTP/1.1"

    def test_split(self):
        self.assertEqual(http_server.split_off_first_line(self.input), self.first_line)


class testBuildResponse(unittest.TestCase):
    def setUp(self):
        self.found_code = 200
        self.resource_file = "webroot/a_web_page.html"
        self.file_response = "HTTP/1.1 200 OK\r\nDate: " + formatdate(usegmt=True) + "\r\nContent-Type: text/html\r\nContent-Length: 136\r\n\r\n<!DOCTYPE html>\n<html>\n<body>\n\n<h1>North Carolina</h1>\n\n<p>A fine place to spend a week learning web programming!</p>\n\n</body>\n</html>\n\n"

        self.resource_dir = "webroot/images"
        self.dir_response = "HTTP/1.1 200 OK\r\nDate: " + formatdate(usegmt=True) + "\r\nContent-Type: text/plain\r\nContent-Length: 66\r\n\r\n/images\r\n\tJPEG_example.jpg\r\n\tSample_Scene_Balls.jpg\r\n\tsample_1.png"

        self.not_found_code = 404
        self.not_found_error = "Not found"
        self.four04_response = "HTTP/1.1 404 Not found\r\nDate: " + formatdate(usegmt=True) + "\r\nContent-Type: text/html\r\nContent-Length: 77\r\n\r\n<!DOCTYPE html>\n<html>\n<body>\n<h1>404 Error: Not found</h1>\n</body>\n</html>\n\n"

        self.not_allowed_code = 405
        self.not_allowed_error = "Not allowed"
        self.four05_response = "HTTP/1.1 405 Method not allowed\r\nDate: " + formatdate(usegmt=True) + "\r\nContent-Type: text/html\r\nContent-Length: 86\r\n\r\n<!DOCTYPE html>\n<html>\n<body>\n<h1>405 Error: Method not allowed</h1>\n</body>\n</html>\n\n"

    def test_build(self):
        self.assertEqual(http_server.build_response(self.found_code, self.resource_file), self.file_response)
        self.assertEqual(http_server.build_response(self.found_code, self.resource_dir), self.dir_response)
        self.assertEqual(http_server.build_response(self.not_found_code, self.not_found_error), self.four04_response)
        self.assertEqual(http_server.build_response(self.not_allowed_code, self.not_allowed_error), self.four05_response)

if __name__ == '__main__':
    unittest.main()
