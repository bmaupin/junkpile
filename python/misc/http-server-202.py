#!/usr/bin/env python

# Simple HTTP server that serves a 202 to delete requests

from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_DELETE(self):
        # send 200 response
        self.send_response(202)
        # send response headers
        self.end_headers()
        # send the body of the response
        self.wfile.write(bytes("202", "utf-8"))

httpd = HTTPServer(('localhost', 10000), MyHandler)
httpd.serve_forever()
