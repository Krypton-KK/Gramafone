import socket
import threading
from cnctflNtrfns import *

header = 2048
frmt = 'utf-8'
port1 = 6000
server = socket.gethostbyname(socket.gethostname())
print(server)
address = (server, port1)
serv = None
srsnd = None

stk = {}

# the server will recive the commands to be executed

dsphm = '_<_displ+home_>_'
ssnchk = '_<_sessn+chk_>_'
gtuid = '_<_get+uid_>_'
gtuslst = '_<_get+user+lst_>_'
chkusr = '_<_check+user_>_'
crtusr = '_<_crt+user_>_'
sndfl = '_<_file+mode_>_'
clctmsg = '_<_collect+msg_>_'
cnusr = '_<_connect+usrs_>_'
disconnect = "_<_end+close_>_"
sndmsg = '_<_snd_msg_>_'
gtusrnm = '_<_get+uname_>_'
callusr = '_<_checkusronline_>_'

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((server, port1))

def popusr(user, nm):
    global stk
    if not stk:
        print('stk is empty')
    else:
        stk.pop(nm)


def viewuser(nm):
    global stk
    if not stk:
        print('stk is empty')
        return None
    else:
        return stk[nm]


def addusr(user, nm):
    global stk
    stk[nm] = user


def usronl(user):
    global stk
    if user in stk:
        return True
    else:
        return False


def frwd(connector, adrs, toid, msg, img='', mode='t'):  # toid
    global srsnd
    if mode == 't':
        mode = sndmsg.encode(frmt)
        client = srsnd
        client.send(mode + b' ' * (header - len(mode)))
        adrs = str([adrs, toid]).encode()
        client.send(adrs + b' ' * (header - len(adrs)))
        if type(msg) is bytes:
            message = msg
        else:
            message = msg.encode(frmt)
        msglen = len(message)
        sendlen = str(msglen).encode(frmt)
        sendlen += b" " * (header - len(sendlen))
        message, key = msgencryptor(message)
        key += b"~" * (header - len(key))
        client.send(key)
        client.send(sendlen)
        client.send(message)


def modechk(connector, adrs, nm):
    mode = connector.recv(header).decode(frmt)
    mode = mode.strip()
    print(mode)
    connected = True
    msg = ''

    # check the messages for commands
    # if the commands are present then execute the fns

    if mode == disconnect:  # done
        popusr(adrs, nm)
        connected = False

    elif mode == sndfl:  # done
        cliflrcv(connector, adrs, nm)

    elif mode == dsphm:  # done
        x = reciver(connector, adrs, nm)
        dpl = dsplyhm(username=x[1])
        y = len(dpl)
        connector.send(str(y).encode() + b' ' * (header - len(str(y).encode())))
        connector.sendall(dpl)

    elif mode == ssnchk:  # done
        x = reciver(connector, adrs, nm)
        y = reciver(connector, adrs, nm)
        tf = sessioncheck(username=x[1], passwd=y[1])
        connector.send(tf.encode(frmt) + b" " * (header - len(tf.encode(frmt))))

    elif mode == gtuid:  # done
        x = reciver(connector, adrs, nm)
        y = getuid(x[1])
        connector.send(y.encode(frmt) + b" " * (header - len(y.encode(frmt))))

    elif mode == gtuslst:  # done
        x = reciver(connector, adrs, nm)
        dpl = getuslst(x[1])
        y = len(dpl)
        connector.send(str(y).encode() + b' ' * (header - len(str(y).encode())))
        connector.sendall(dpl)

    elif mode == chkusr:  # done
        x = connector.recv(header).decode().strip()
        y = usercheck(x)
        connector.send(y.encode(frmt) + b" " * (header - len(y.encode(frmt))))

    elif mode == crtusr:  # done
        x = connector.recv(header).decode().strip()  # usr
        y = connector.recv(header).decode().strip()  # pass
        usercreate(x, y)
        connector.send("done".encode(frmt) + b" " * (header - len("done".encode(frmt))))

    elif mode == clctmsg:  # done
        x = reciver(connector, adrs, nm)  # toid
        y = reciver(connector, adrs, nm)  # frid
        dpl = cltmsg(x[1], y[1])
        y = len(dpl)
        connector.send(str(y).encode() + b' ' * (header - len(str(y).encode())))
        connector.sendall(dpl)

    elif mode == cnusr:  # done
        x = reciver(connector, adrs, nm)  # toid
        y = reciver(connector, adrs, nm)  # frid
        conuse(x[1], y[1])
        connector.send("done".encode(frmt) + b" " * (header - len("done".encode(frmt))))

    elif mode == sndmsg:  # done
        key = connector.recv(header)
        key = key.strip(b" ")
        msg_length = connector.recv(header).decode(frmt)
        if msg_length == disconnect:
            connected = False
        elif msg_length:
            msg_length = msg_length
        msg = connector.recv(int(msg_length)).decode(frmt)
        print(msgdecryptor(st2=msg, gnkey=key).decode())
        x = reciver(connector, adrs, nm)  # toid
        y = reciver(connector, adrs, nm)  # frid
        sndimg(touid=x[1], fruid=y[1], txtmsg=msg, image="", keys=key)
        if usronl(x[1]):
            frwd(connector, adrs, x[1], msgdecryptor(st2=msg, gnkey=key).decode())
        if not (x[1] == server):
            msg = {'msg': msg, 'touid': x[1], 'fruid': y[1]}
        else:
            msg = msg

    elif mode == gtusrnm:
        x = reciver(connector, adrs, nm)
        uid = x[1]
        w = usnm(uid).encode()
        connector.send(w + b' ' * (header - len(w)))

    elif mode == callusr:
        x = reciver(connector, adrs, nm)
        uid = x[1]
        if usronl(uid):
            connector.send('alive'.encode() + b' ' * (header - len('alive'.encode())))
            connector.send(str(viewuser(uid)).encode() + b' ' * (header - len(str(viewuser(uid)).encode())))
            x = connector.recv().decode().strip()
            fwdcall(uid,x)
        else:
            connector.send('dead-'.encode() + b' ' * (header - len('alive'.encode())))

    return connected, mode, msg


def reciver(connector, adrs, nm):  # using recursion for checking the commands
    connected, mode, msg = modechk(connector, adrs, nm)
    print(f'{adrs}:{mode}')
    return connected, msg


def cliflrcv(connector, adrs, nm):
    print('reciving filekey')
    flkey = connector.recv(header).decode(frmt).strip()
    print("reciving file name")
    flnm = connector.recv(header).decode(frmt).strip()
    print(flnm, "", sep='\n')
    print('now reciving file size')
    flsz = connector.recv(header).decode(frmt).strip()
    flsz = int(flsz)
    print(flsz)  # encrypted file size
    file = open(r'tmp\tmp-'.rstrip() + flnm, "wb")  # the temp file is created
    print('reciving the file content')
    enflbts = b""
    for i in range(flsz // header):
        data = connector.recv(header)
        enflbts += data
    else:
        data = connector.recv(flsz % header)
        enflbts += data
        print(enflbts)
    x = reciver(connector, adrs, nm)  # toid
    y = reciver(connector, adrs, nm)  # frid
    w = reciver(connector, adrs, nm)  # textmsg
    sndimg(touid=x[1], fruid=y[1], txtmsg=w, image=enflbts, keys=flkey)
    file.write(msgdecryptor(enflbts, flkey))
    file.close()


def clientconnect(connector, adrs):
    nm = connector.recv(header).decode().strip()
    addusr(adrs, nm)
    print(f"the active connections now are {threading.active_count()}")
    print(f"connection started (with) : {adrs}")
    connected = True
    while connected:
        connected, msg = reciver(connector, adrs, nm)
    connector.close()


def start():
    serv.listen()
    while True:
        connection, adrs = serv.accept()
        x = threading.Thread(target=clientconnect(connection, adrs))
        x.start()
        

def fwdcall(nm,time):
# timed = datetime.strptime(str(time),'%Y-%d-%m %H:%M:%S.%f')
    tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    adrs = viewuser(nm)
    tmp.connect((adrs, port1))
    msg = callusr.encode()
    tmp.send(msg + b' ' * (header - len(msg)))
    tmp.send(time.encode() +  b' ' * (header - len(time.encode())))
    tmp.close()
# set client to parse the datetime as done in timed

start()
