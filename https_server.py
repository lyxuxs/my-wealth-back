import http.server
import ssl

# Define the handler to use for serving files
handler = http.server.SimpleHTTPRequestHandler

# Create an HTTP server instance
httpd = http.server.HTTPServer(('localhost', 4443), handler)

# Wrap the server socket with SSL
httpd.socket = ssl.wrap_socket(httpd.socket,
                               server_side=True,
                               keyfile="server.key",
                               certfile="server.crt",
                               ssl_version=ssl.PROTOCOL_TLS)

print("Serving on https://localhost:4443")
httpd.serve_forever()
