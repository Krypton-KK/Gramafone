import datetime
import threading
from socket import *
import os

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
fh = open(r'Program files/programlevelvariables.txt', 'r')
x = eval(fh.read())
print("thread established")

# dictvar = {'username': username, 'password': passwd, "mode": mode, "anuser": ""}
usnm = x['username']
tonm = x['anuser']
client.send(usnm.encode() + b' ' * (header - len(usnm.encode())))


def sendid(touid, fruid):
    programlevelvar = open('Program files/programlevelvariables.txt')
    # {'username': 'GRAMAFONEANNOUNCEMENTS', 'password': 'instagramisuseless@2023#',
    # 'mode': 'All In One', 'anuser': 'Kavin_Karthik'}
    programlevelvar.seek(0, 0)  # start the file each time at the file start
    prlvvar = eval(programlevelvar.readline())
    touid = prlvvar['anuser']
    fruid = prlvvar['username']
    sendmsg(touid)
    sendmsg(fruid)


def sendmsg(msg):
    mode = sndmsg.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    if type(msg) is bytes:
        message = msg
    else:
        message = msg.encode(frmt)
    msglen = len(message)
    sendlen = str(msglen).encode(frmt)
    sendlen += b" " * (header - len(sendlen))
    import cnctflNtrfns as cnct
    message, key = cnct.msgencryptor(message)
    key += b"~" * (header - len(key))
    client.send(key)
    client.send(sendlen)
    client.send(message)


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
    sendmsg(username)
    sendmsg(password)
    tf = eval(client.recv(header).decode(frmt).strip())
    return tf


def displhm(username):
    mode = dsphm.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    sendmsg(username)
    length = int(client.recv(header).decode(frmt).strip())
    hm = ""
    for i in range(length // header):
        data = client.recv(header).decode(frmt)
        hm += data
    else:
        data = client.recv(length % header)
        hm += data
    hm = eval(hm)
    return hm


def getuid(username):
    mode = gtuid.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    sendmsg(username)
    x = client.recv(header).decode(frmt).strip()
    return x


def getuslst(username):
    mode = gtuslst.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    sendmsg(username)
    length = int(client.recv(header).decode(frmt).strip())
    hm = ""
    for i in range(length // header):
        data = client.recv(header).decode(frmt)
        hm += data
    else:
        data = client.recv(length % header)
        hm += data
    hm = eval(hm)
    return hm


def checkusr(username):
    mode = chkusr.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    sendmsg(username)
    y = client.recv(header).decode(frmt).strip()
    return y


def createuser(username, password):
    mode = crtusr.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    sendmsg(username)
    sendmsg(password)
    y = client.recv(header).decode(frmt).strip()
    return y


def collectmsgs(toid, frid):
    mode = clctmsg.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    sendmsg(toid)
    sendmsg(frid)
    length = int(client.recv(header).decode(frmt).strip())
    hm = ""
    for i in range(length // header):
        data = client.recv(header).decode(frmt)
        hm += data
    else:
        data = client.recv(length % header)
        hm += data
    hm = eval(hm)
    return hm


def connctusr(username, password):
    mode = cnusr.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    sendmsg(username)
    sendmsg(password)
    y = client.recv(header).decode(frmt).strip()
    return y


def getusername(uid):
    mode = gtusrnm.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    sendmsg(uid)
    x = client.recv(header).strip().decode()
    return x


def call(uid):
    mode = callusr.encode(frmt)
    client.send(mode + b' ' * (header - len(mode)))
    sendmsg(uid)
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