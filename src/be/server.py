from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re

import methods

host_name = "127.0.0.1"
server_port = 3001

method_name_pat = re.compile(r'^/(\S+)$')


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            method_name = self.get_method_name()
            request = self.get_request()
            resp = {'data': self.invoke_method(method_name=method_name, request=request)}
            self.write_response(code=200, resp_body=resp)
        except Exception as ex:
            resp = {'err': {'code': -1, 'msg': str(ex)}}
            self.write_response(code=500, resp_body=resp)
            raise ex

    def get_method_name(self):
        m = method_name_pat.match(self.path)
        return m.group(1)

    def get_request(self):
        content_length = int(self.headers['Content-Length'])
        body_str = self.rfile.read(content_length).decode("utf-8")
        return json.loads(body_str)

    def invoke_method(self, method_name: str, request: dict):
        return getattr(methods, method_name)(**request)

    def write_response(self, code: int, resp_body: dict):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(resp_body), 'utf-8'))


if __name__ == "__main__":
    webServer = HTTPServer((host_name, server_port), RequestHandler)
    print(f'Server started at http://{host_name}:{server_port}')
    webServer.serve_forever()
