import datetime
import yaml
import os
from socket import *

header = 2048
frmt = 'utf-8'
port = 6000
server = "192.168.0.109"  # server ip
address = (server, port)
# cmds
dsphm = '_<_displ+home_>_'
ssnchk = '_<_sessn+chk_>_'
gtuid = '_<_get+uid_>_'
gtuslst = '_<_get+user+lst_>_'
chkusr = '_<_check+user_>_'
crtusr = '_<_crt+user_>_'
sndfl = '_<_file+mode_>_'
clctmsg = '_<_collect+msg_>_'
cnusr = '_<_connect+usrs_>_'
disconnection = "_<_end+close_>_"
sndmsg = '_<_snd_msg_>_'
gtusrnm = '_<_get+uname_>_'
callusr = '_<_checkusronline_>_'

client = socket(AF_INET, SOCK_STREAM)
client.connect(address)
with open(r'..\Program files/programvariables.yaml', 'r') as fh:
    content = yaml.safe_load(fh)

# {'username':'GRAMAFONEANNOUNCEMENTS','password':'instagramisuseless@2023#','mode':'Message Client','anuser': 'Kavin'}
usnm = content['username']
tonm = content['anuser']
client.send(usnm.encode() + b' ' * (header - len(usnm.encode())))


def sendid(toid, frid):
    '''with open('../Program files/programvariables.yaml', 'r') as fh:
        content = yaml.safe_load(fh)
    frid = content['username']
    toid = content['anuser']'''
    toid = toid.encode(frmt) + b' ' * (header - len(toid.encode(frmt)))
    frid = frid.encode(frmt) + b' ' * (header - len(frid.encode(frmt)))
    client.send(toid)
    client.send(frid)


def sendmsg(msg, fruid=0, touid=0):
    mode = sndmsg.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    if type(msg) is bytes:
        message = msg
    else:
        message = msg.encode(frmt)
    import cnctflNtrfns as cnct
    message, key = cnct.msgencryptor(message)
    print(message,key,sep='{hi}')
    key = str([key]).encode(frmt)
    client.send(key + b" " * (header - len(key)))
    msglen = len(message)
    sendlen = str(msglen).encode(frmt)
    sendlen += b" " * (header - len(sendlen))
    client.send(sendlen)
    if msglen > header:
        client.send(message)
    else:
        client.send(message + b' ' * (header - len(message)))
    if not (fruid == 0 or touid ==0):
        sendid(touid, fruid)


def disconnect():
    client.send(disconnection.encode() + b' ' * (header - len(disconnection.encode())))
    client.close()


def sendfile(filepath, fruid, touid, txtmsg):  # get input from the file dialog using the ctk
    mode = sndfl.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    file = open(filepath, "rb")
    flbts = file.read()
    import cnctflNtrfns as cnct
    enfbts, key = cnct.msgencryptor(st1=flbts)
    client.send(key + b' ' * (header - len(key)))
    flsz = len(enfbts)
    flnm = os.path.basename(filepath).encode(frmt)
    client.send(flnm + b' ' * (header - len(flnm)))
    w = str(flsz).encode(frmt)
    client.send(w + b' ' * (header - len(w)))
    client.sendall(enfbts)
    sendid(touid, fruid)
    sendmsg(txtmsg)
    print(enfbts)
    file.close()


def sessncheck(username, password):
    mode = ssnchk.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    username = username.encode()
    password = password.encode()
    client.send(username + b' ' * (header - len(username)))
    client.send(password + b' ' * (header - len(password)))
    tf = eval(client.recv(header).decode(frmt).strip())
    return tf


def displhm(username):
    mode = dsphm.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    username = username.encode(frmt) + b" " * (header - len(username.encode(frmt)))
    client.send(username)
    length = int(client.recv(header).decode(frmt).strip())
    print(length)
    hm = ""
    for i in range(length // header):
        data = client.recv(header).decode(frmt)
        print(data)
        hm = hm + data
    else:
        data = client.recv(length % header).decode(frmt)
        print(data)
        hm = hm + data
    print(hm)
    hm = eval(hm)
    return hm


def getuid(username):
    mode = gtuid.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    username = str(username).encode(frmt) + b" " * (header - len(str(username).encode(frmt)))
    client.send(username)
    x = client.recv(header).decode(frmt).strip()
    return x


def getuslst(username):
    mode = gtuslst.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    username = username.encode(frmt) + b" " * (header - len(username.encode(frmt)))
    client.send(username)
    length = int(client.recv(header).decode(frmt).strip())
    hm = ""
    for i in range(length // header):
        data = client.recv(header).decode(frmt)
        hm += data
    else:
        data = client.recv(length % header).decode(frmt)
        hm += data
    hm = eval(hm)
    return hm


def checkusr(username):
    mode = chkusr.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    username = username.encode(frmt)
    client.send(username + b' ' * (header - len(username)))
    y = client.recv(header).decode(frmt).strip()
    return y


def createuser(username, password):
    mode = crtusr.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    username = str(username).encode()
    client.send(username + b' ' * (header - len(username)))
    password = str(password).encode()
    client.send(password + b' ' * (header - len(password)))
    y = client.recv(header).decode(frmt).strip()
    return y


def collectmsgs(toid, frid):
    mode = clctmsg.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    toid = str(toid).encode(frmt) + b' '*(header - len(toid.encode(frmt)))
    frid = str(frid).encode(frmt) + b' '*(header - len(frid.encode(frmt)))
    client.send(toid)
    client.send(frid)
    length = int(client.recv(header).decode(frmt).strip())
    hm = ""
    for i in range(length // header):
        data = client.recv(header).decode(frmt)
        hm = hm + data
    else:
        data = client.recv(length % header).decode(frmt)
        hm = hm + data
    print(hm)
    if not hm:
        hm = []
    else:
        hm = eval(hm)
    return hm


def connctusr(toid, frid):
    mode = cnusr.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    toid = toid.encode(frmt) + b' ' * (header - len(toid.encode(frmt)))
    frid = frid.encode(frmt) + b' ' * (header - len(frid.encode(frmt)))
    client.send(toid)
    client.send(frid)
    y = client.recv(header).decode(frmt).strip()
    return y


def getusername(uid):
    mode = gtusrnm.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    uid = uid.encode(frmt) + b' ' * (header - len(uid.encode(frmt)))
    client.send(uid)
    x = client.recv(header).strip().decode()
    return x


def call(uid):
    mode = callusr.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    uid = uid.encode(frmt) + b' ' * (header - len(uid.encode(frmt)))
    client.send(uid)
    x = client.recv(header).decode().strip()
    if x == 'alive':
        nm = client.recv(header).decode().strip()
        print('call will be conducted at 120 seconds from now to maintain correct time')
        w = datetime.datetime.now() + datetime.timedelta(0,120)
        timestr = str(w).encode()
        client.send(timestr + b' ' * (header - len(timestr)))
        while datetime.datetime.now() == w:
            import callingfn
            callingfn.calling(nm)

    elif x == 'dead-':
        print('user is not online pls contact later')