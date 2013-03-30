import socket, os, sys, thread
import SimpleHTTPServer as simp
import SocketServer
class IonicServer:
    def __init__(self):
        self.port = int(sys.argv[1])
        self.commands = {

            'get':self.get,
            'send':self.send,
            'del':self.delete,
            'list':self.list,
            "senddir":self.senddir,
            "deldir":self.delete_dir,
            }
        self.users = {
                "4edf66bc2bc22f6ff95e9c238682d84d55849000e34321f88cb2720ad3da57e2":"4edf66bc2bc22f6ff95e9c238682d84d55849000e34321f88cb2720ad3da57e2"
                }
        #Format of users, "username":"password" hashed using SHA256
        #Users must be added manually. 
    def main(self):
        self.sock = socket.socket()
        self.sock.bind(('', self.port))
        self.sock.listen(1)
        print "\nIonic Backup Has Started.\n"
        while True:
            obj,con = self.sock.accept()
            self.obj = obj
            data = obj.recv(1024)
            self.data = data
            if not data:
                return 1
            else:
                data = data.split()
                username = data[len(data)-2]
                password = data[len(data)-1]
                if username not in self.users or self.users[username] != password:
                    print "Login Failed From", con[0]
                    continue
                else:
                    self.data = self.data.split()
                    self.data.remove(username)
                    self.data.remove(password)
                    self.data = ' '.join(self.data)
                try:
                    self.commands[data[0]]()
                except Exception, error:
                    print error
    def get(self):
        data = self.data.split()[1]
        with open(data, 'rb') as file:
            for x in file:
                self.obj.send(x)
        self.obj.close()
    def send(self):
        data = self.data.split()[1]
        with open(data, 'wb') as file:
            while True:
                data = self.obj.recv(1024)
                if not data:
                    self.obj.close()
                    break
                file.write(data)
    def delete(self):
        data = self.data.split()[1]
        try:
            os.remove(data)
        except:
            pass
    def delete_dir(self):
        data = self.data.split()[1]
        try:
            os.rmdir(data)
        except:
            pass

    def senddir(self):
        dir = self.data.split()[1]
        if not os.path.exists(dir):
            try:
                os.mkdir(dir)
            except:
                pass
    def list(self):
        files = []
        dirs = []
        for x,y,z in os.walk(os.getcwd()):
            for f in y:
                g =  x + "/" + f
                try:
                    dirs.append(g.replace(os.getcwd(), "").strip("/"))
                except:
                    pass
            for b in z:
                file = x+"/"+b
                try:
                    files.append(file.replace(os.getcwd(), '').strip("/"))
                except:
                    pass
        files.remove(sys.argv[0])
        data = str(dirs)+":"+str(files)
        for x in data:
            self.obj.send(x)
        self.obj.close()
def http_server():
    port = 5643
    handle = simp.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(('', port), handle)
    print "HTTP server started on port "+ str(port)
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        if len(sys.argv) > 2:
            if sys.argv[2] == 'http':
                thread.start_new_thread(http_server, ())
        IonicServer().main()
    except IndexError:
        print "Usage: python server.py <port>"
