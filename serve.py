from textual_serve.server import Server

server = Server("python -m main.py")
server.serve()