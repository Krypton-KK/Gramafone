import csv
from datetime import datetime
from cryptography.fernet import Fernet as Cfr
# import pypyodbc as pyodbc
import mysql.connector as pps


Databasename1 = "Messages"
Databasename2 = "users"
paswd = "kavin"


def msgcon():
    connection = pps.connect(host='localhost', database=Databasename1, user='root', password=paswd)
    if connection.is_connected():
        print('connected')
    return connection


def uscon():
    connection = pps.connect(host='localhost', database=Databasename2, user='root', password=paswd)
    if connection.is_connected():
        print('connected')
        return connection


def sessioncheck(username, passwd):
    cn = uscon()
    cur = cn.cursor()
    cur.execute("select * from usernid where usnm = '%s' and passwd = '%s'" % (username, passwd))
    val = cur.fetchall()
    if not val:
        return False
    elif len(val) == 1:
        return True
    else:
        raise "more than 2 accounts are present"


def getuid(username):
    # getting uid from given username
    cn = uscon()
    cur = cn.cursor()
    cur.execute("select usid from usernid where usnm = '%s'" % username)
    [(x,)] = cur.fetchall()
    return x


def getuslst(username):
    cn = uscon()
    cur = cn.cursor()
    cur.execute("select conted from usernid where usnm = '{}'".format(username))
    [(x,)] = cur.fetchall()
    tup = eval(x)
    return tup


def usercheck(username):
    cn = uscon()
    cur = cn.cursor()
    cur.execute("select * from usernid where usnm = '%s'" % username)
    if cur.fetchall():  # yeilds true for non empty lists
        return "exception the username is already present choose any other"
    else:
        return "it is Vacant!!"


def usercreate(username, passwd):
    cn = uscon()
    cur = cn.cursor()
    cur.execute("select max(usid) from usernid;")
    [(maxuid,)] = cur.fetchall()
    cur.execute("insert into usernid(usid,usnm,passwd) values(%s,'%s','%s');" % (int(maxuid) + 1, username, passwd))
    cn.commit()


def dsplyhm(username):
    msgcn = msgcon()
    msgcur = msgcn.cursor()
    usid = getuid(username=username)
    userlist = getuslst(username=username)
    msgcur.execute('select distinct(touid),DOP from Messages where touid in %s and fruid = %s order by DOP desc'
                   % (userlist, usid))
    x = msgcur.fetchall()
    if not x:  # new account
        x = list(userlist)
    for i in range(len(x)):
        uscon().cursor().execute("select usnm from usernid where usid=%s" % x[i][0])
        w = uscon().cursor().fetchall()
        x[i] += (w,)
    return x


def usnm(uid):
    uscon().cursor().execute("select usnm from usernid where usid=%s" % uid)
    w = uscon().cursor().fetchall()
    return str(w)


def csvk(keys='', keyid=0):  # stores and retrives the keys
    fh = open(r"..\Program files/keys.csv", 'a+', newline='\r\n')
    c = csv.reader(fh)
    if keyid:
        for i in c:
            if keyid == i[0]:
                keys = i[1]
    elif keys:
        keylst = []
        for i in c:
            keylst.append(int(i[0]))
        keylst.sort()
        keyid = keylst.pop() + 1
        w = csv.writer(fh)
        w.writerow([keyid, keys])
    return keyid, keys


def sndimg(touid, fruid, txtmsg, image, keys):
    rslt = csvk(keys)
    keyid = rslt[0]
    dop = datetime.now()
    imgstr = str(image)
    msgcn = msgcon()
    msgcur = msgcn.cursor()
    msgcur.execute('insert into Messages values(%s,%s,%s,%s,%s,%s)' % (
        touid, fruid, txtmsg, imgstr, keyid, dop))  # keys column stores the keyid
    msgcn.commit()


def cltmsg(touid, fruid):
    msgcn = msgcon()
    msgcur = msgcn.cursor()
    msgcur.execute('select * Messages where fruid in (%s,%s) and touid in (%s,%s)' % (touid, fruid, touid, fruid))
    (touid, fruid, txtmsg, imgstr, keyid, dop) = msgcur.fetchall()
    keys = csvk(keyid=int(str(keyid)))[1]
    return touid, fruid, txtmsg, imgstr, keys, dop


'''
def encryptionchange():
    key = Cfr.generate_key()
    print(key)
    k = r.randint(1, 26)
    sl = list(str(key))
    print(sl)
    # adding noise "k" to key
    for i in range(2, len(key) + 2):  # +2 to encode the last 2 values also
        sl[i] = chr(ord(sl[i]) + k)
    print(sl)
    # convert list to string
    keymod = ("".join(sl))
    # checking -- value of key is unchanged
    """print(key, '\n', keymod)  # 2-42
    kmdcl = str(keymod)
    slw = list(str(kmdcl))
    for i in range(2, len(kmdcl) + 1):
        slw[i] = chr(ord(slw[i]) - k)
    print(kmdcl, '\n', key)"""
    return (keymod + str(k)).encode(), key  # first 44 are keys


def decryptionchange(key):
    # removes given noise from given key
    key = key.decode("utf-8")
    print(key, len(key))
    keymod = key[:47]
    sl = list(str(keymod))
    k = key[47:]
    for i in range(2, len(keymod)):
        sl[i] = chr(ord(sl[i]) - int(k))
    print(sl)
    keyor = "".join(sl)
    return keyor
'''


def msgencryptor(st1, key=Cfr.generate_key()):
    # encrypts data using givenkey
    en = Cfr(key)
    if type(st1) is bytes:
        st1 = en.encrypt(st1)
    else:
        st1 = en.encrypt(str(st1).encode())
    return st1, key


def msgdecryptor(st2, gnkey):
    # decrypts the message using givenkey
    en = Cfr(gnkey)
    st2 = en.decrypt(st2)
    return st2  # decode at fn call


def conuse(tonm, frnm):  # new chat
    usco = uscon()
    usco.cursor().execute(
        "update usernid set conted = conted + ',%s' where usid = %s" % (getuid(tonm), getuid(frnm)))
    usco.commit()
    usco.cursor().execute(
        "update usernid set conted = conted + ',%s' where usid = %s" % (getuid(frnm), getuid(tonm)))
    usco.commit()

