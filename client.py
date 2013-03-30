import socket, os, time, sys, thread, getpass, hashlib

class IonicClient:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = hashlib.sha256(username).hexdigest()
        self.password = hashlib.sha256(password).hexdigest()
        self.dirs = []
        self.files = {}
        for x,y,z in os.walk(os.getcwd()):
            for b in z:
                if b == sys.argv[0]:
                    continue
                with open(x+"/"+b, 'rb') as file:
                    self.files[b.strip("/")] = hash(file.read())
    def main(self):
        while True:
            time.sleep(1)
            stuff = self.list().split(":")
            try:
                dir = eval(stuff[0])
            except SyntaxError:
                print "\nLogin Failed"
                break
            file = eval(stuff[1])
            for x in dir:
                if not os.path.exists(x.strip("/")):
                    os.mkdir(x.strip("/"))
                    self.dirs.append(x)
            for x in file:
                if not os.path.exists(x) and x not in self.files:
                    self.get(x)
                    with open(x, 'rb') as f:
                        self.files[x] = hash(f.read())
                if not os.path.exists(x) and x in self.files:
                    self.delete(x)
                    del self.files[x]
            for x,y,z in os.walk(os.getcwd()):
                for d in y:
                    direc = x.strip(os.getcwd())+"/"+d
                    direc = direc.strip("/")
                    if direc not in self.dirs:
                        self.dirs.append(direc)
                    if direc not in dir:
                        self.senddir(direc)
                for f in z:
                    file_c = x +"/"+ f
                    file_c = file_c.replace(os.getcwd(), '').strip("/")
                    if file_c == sys.argv[0]:
                        continue
                    if file_c in self.files and file_c not in file:
                        self.send(file_c)
                    elif file_c not in self.files and file_c not in file:
                        with open(file_c, 'rb') as f:
                            self.files[file_c] = hash(f.read())
                        self.send(file_c)
                    elif file_c in self.files and file_c in file:
                        with open(file_c, 'rb') as f:
                            if hash(f.read()) != self.files[file_c]:
                                self.send(file_c)
                                with open(file_c, 'rb') as f:
                                    self.files[file_c] = hash(f.read())
            
    def senddir(self, direc):
        senddir = socket.socket()
        try:
            senddir.connect((self.ip, self.port))
        except:
            print "Could not connect to server."
        send = "senddir {0} {1} {2}".format(direc, self.username, self.password)
        senddir.send(send)
        senddir.close()
    def list(self):
        list = socket.socket()
        try:
            list.connect((self.ip, self.port))
        except:
            print "Could not connect to server."
        send = "list {0} {1}".format(self.username, self.password)
        list.send(send)
        data = ''
        while True:
            d = list.recv(1024)
            data = data + d
            if not d:
                break
        return data
        list.close()
    def send(self, file):
        print "sending", file
        send = socket.socket()
        send.connect((self.ip, self.port))
        sends = "send {0} {1} {2}\r\n\r\n".format(file, self.username, self.password)
        send.send(sends)
        with open(file, 'rb') as file_:
            for x in file_.readlines():
                send.send(x)
            print "Done sending", file
        send.close()
    def get(self, file):
        print "Downloading", file
        get = socket.socket()
        try:
            get.connect((self.ip, self.port))
        except:
            print "Could not connect to server"
        send = "get {0} {1} {2}".format(file, self.username, self.password)
        get.send(send)
        with open(file, 'wb') as name:
            while True:
                data = get.recv(1024)
                if not data:
                    print "Done downloading", file
                    get.close()
                    break
                name.write(data)
    def delete(self, file):
        if file == sys.argv[0]:
            print "You can not delete Ionic Backup Client"
        else:
            try:
                os.remove(file)
            except:
                print "File doesn't exist"

            delete = socket.socket()
            try:
                delete.connect((self.ip, self.port))
            except:
                print "Could not connect to server."
            send = "del {0} {1} {2}".format(file, self.username, self.password)
            delete.send(send)
            delete.close()
    def delete_dir(self, file):
        try:
            os.rmdir(file)
        except:
            print "Directory doesn't exist"
        deldir = socket.socket()
        try:
            deldir.connect((self.ip, self.port))
        except:
            print "Could not connect to server."
        
        send = "deldir {0} {1} {2}".format(file, self.username, self.password)
        deldir.send(send)
        deldir.close()

def shell(ip, port, username, password):
    while True:
        cmd = raw_input("IonicShell> ")
        if cmd == "help":
            print """

                rm <file> - Deletes a file on the server and locally.
                rmdir <dir> - Deletes a directory on the server and locally.
                ls - Returns all the files on the server.

                """
        elif cmd.startswith("rm "):
            cmd = cmd.split()[1]
            IonicClient(ip, port, username, password).delete(cmd)

        elif cmd.startswith("rmdir "):
            cmd = cmd.split()[1]
            IonicClient(ip, port, username, password).delete_dir(cmd)
        elif cmd == "ls":
            stuff = IonicClient(ip, port, username, password).list().split(":")
            print "Directories: \n"+'\n'.join(eval(stuff[0]))
            print "\n"
            print "Files: \n"+'\n'.join(eval(stuff[1]))

if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        port = int(sys.argv[2])
    except IndexError:
        print "Usage: python client.py <ip> <port>"
    else:
        username = raw_input("Username: ")
        password = getpass.getpass("Password: ")
        thread.start_new_thread(shell, (ip, port, username, password))
        IonicClient(ip, port, username, password).main()
