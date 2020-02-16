import paramiko, getpass, time, telnetlib, subprocess

def iptest(ip):
    try:
        s = subprocess.check_output(["ping", "-c", "1", ip])
        if s:
            print "Host " + ip + " is ip"
            return True
    except:
        return False

class sshcon:
    def __init__(self, hostname, username):
        self.hostname = hostname
        self.username = username
        self.password = None
        self.port = 22
        self.client = None
        self.iptest = iptest(self.hostname)
        paramiko.util.log_to_file("filename.log")
        if self.iptest:
            try:
                self.client = paramiko.SSHClient()
                self.client.load_system_host_keys()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.password = getpass.getpass()
                self.client.connect(self.hostname, self.port, self.username, self.password)
            except:
                print "Eroare de conectare"
            self.chan = self.client.get_transport().open_session()
            self.chan.invoke_shell()
        else:
            print "Host " + self.hostname + " is down"
    def Command(self, command=None):
        if self.iptest:
            if(type(command) is list):
                self.chan.sendall('terminal length 0\n')
                while self.chan.recv_ready():
                    self.chan.recv(9999)
                for i in command:
                    self.chan.sendall(i)
                    self.chan.sendall("\n")
                    time.sleep(1)
                    print self.chan.recv(9999)
            elif(type(command) is str):
                self.chan.sendall('terminal length 0\n')
                while self.chan.recv_ready():
                    self.chan.recv(9999)
                self.chan.sendall(command)
                self.chan.sendall("\n")
                time.sleep(1)
                print self.chan.recv(9999)

                self.client.close()
                #stdin, stdout, stderr = self.client.exec_command("show ip int br")
                #print stdout.read()
                #print stderr.read()  

class telnetcon:
    def __init__(self, hostname, username):
        self.hostname = hostname
        self.username = username
        self.iptest = iptest(self.hostname)
        if self.iptest:
            self.password = getpass.getpass()
            self.tn = telnetlib.Telnet(self.hostname)

            self.tn.read_until(b"Username: ")
            self.tn.write(self.username.encode('ascii') + b"\n")
            if self.password:
                self.tn.read_until(b"Password: ")
                self.tn.write(self.password.encode('ascii') + b"\n")
        else:
            print "Host " + self.hostname + " is down"

    def Command(self, command):
        if self.iptest:
            self.tn.write(b"en\n")
            if type(command) is list:
                for i in command:
                    self.tn.write(i.encode('ascii') + b"\n\n")
            elif type(command) is str:
                self.tn.write(command.encode('ascii') + b"\n")
            self.tn.write(b"exit\n")
            print self.tn.read_all().decode('ascii')

#s1 = sshcon("192.168.0.121", "admin")
#s1.Command("show ver")

s2 = telnetcon("192.168.0.120", "admin")
s2.Command("show ip int br")


