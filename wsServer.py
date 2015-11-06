import SocketServer
import hashlib
import base64
import time
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return
    def handle(self):
        data = self.request.recv(1024)
        handshake = data.split("\r\n")
        print handshake
        reply = ["HTTP/1.1 101 Switching Protocols"]
        for i in handshake:
            if i.startswith("Upgrade:"):
                reply.append(i)
            elif i.startswith("Connection:"):
                reply.append(i)
            elif i.startswith("Sec-WebSocket-Key:"):
                key = hashlib.sha1(i.split()[1]+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").digest()
                key = base64.b64encode(key)
                reply.append("Sec-WebSocket-Accept:"+key)
            elif i.startswith("Sec-WebSocket-Protocol:"):
                reply.append(i.split(",")[0])
        print reply
        self.request.sendall("\r\n".join(reply)+"\r\n\r\n")
        """
        data = bytearray([0x81, 0x05, 0x48, 0x65, 0x6c, 0x6c, 0x6f])   # hello
        self.request.sendall(data)
        data = bytearray([0x82, 0x05, 0x48, 0x65, 0x6c, 0x6c, 0x5f])   # hello
        self.request.sendall(data)
        head = bytearray([0x02, 0x05])
        data = bytearray([0x48, 0x65, 0x6c, 0x6c, 0x5f])   # hello
        self.request.sendall(head+data)
        head = bytearray([0x00, 0x05])
        data = bytearray([0x48, 0x65, 0x6c, 0x6c, 0x5f])   # hello
        self.request.sendall(head+data)
        head = bytearray([0x80, 0x05])
        data = bytearray([0x48, 0x65, 0x6c, 0x6c, 0x5f])   # hello
        self.request.sendall(head+data)
        return
        """

        for i in range(1, 9422):
            jpgName = "../jpg/output{:08d}.jpg".format(i)
            with open(jpgName, "rb") as f:
                b = bytearray(f.read())
                if len(b) > 0xffff:
                    head = bytearray([0x82, 0x7f, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                    head.append(len(b)>>16)
                    head.append((len(b)>>8)&0xff)
                    head.append(len(b)&0xff)
                else:
                    head = bytearray([0x82, 0x7e])
                    head.append(len(b)>>8)
                    head.append(len(b)&0xff)
                self.request.sendall(head + b)
                print "send", jpgName, len(b), "bytes"
            time.sleep(0.05)

def main():
    HOST, PORT = "", 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
