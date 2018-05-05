import http.server
from urllib import parse

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

# TODO: Redefine and use or remove
#HELLO_WORLD_PATTERN = re.compile("/.*[Hh]ello.*")

class SerpentServerHandler(http.server.SimpleHTTPRequestHandler):

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_HEAD(self):
    self._set_headers()
      
  def do_GET(self):
    """Respond to a GET request."""
    self._set_headers()

    url_data = parse.urlparse(self.path)
    url = url_data.geturl()
    params = parse.parse_qs(url.query)

    # TODO: Implement param handling
    # if("address" in params):
    #     address = params["address"][0]
        
    # If someone went to "http://something.somewhere.net/foo/bar/",
    # then self.path equals "/foo/bar/".
    # TODO: Implement request handling
    # if HELLO_WORLD_PATTERN.match(self.path) != None:
    #     self.wfile.write(bytes("<html><head><title>This page brought to you by Python!</title></head>", "utf-8"))
    #     self.wfile.write(bytes("<body><p>Hello World</p>", "utf-8"))
    #     self.wfile.write(bytes("<p>You accessed path: %s</p>" % self.path, "utf-8"))
    #     self.wfile.write(bytes("</body></html>", "utf-8"))
    # elif MAP_PATTERN.match(self.path) != None:
    #     directions_page = DirectionsPageTemplate(address, instructions)
    #     self.wfile.write(bytes(directions_page.build(), "utf-8"))
    
  def do_POST(self):
    self._set_headers()
    # TODO: Implement
    data_string = self.rfile.read(int(self.headers['Content-Length']))
    
    self.send_response(200)
    self.end_headers()
    return

# Note: This function is not part of the above class
def start_server():
  server_class = http.server.HTTPServer
  httpd = server_class((HOST_NAME, PORT_NUMBER), SerpentServerHandler)
    
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
    
  httpd.server_close()
