import socket, os, sys

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
    def main(self):
        self.sock = socket.socket()
        self.sock.bind(('', self.port))
        self.sock.listen(1)
        print "Ionic Backup Has Started."
        while True:
            obj,con = self.sock.accept()
            self.obj = obj
            data = obj.recv(1024)
            self.data = data
            print con[0], data
            if not data:
                return 1
            else:
                data = data.split()
                self.commands[data[0]]()

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
            os.mkdir(dir)
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
        self.obj.send(str(dirs)+":"+str(files))
if __name__ == "__main__":
    IonicServer().main()
