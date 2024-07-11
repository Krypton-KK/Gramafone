import threading
import miniupnpc
from vidstream import AudioSender
from vidstream import AudioReceiver
import socket


# open the ports first
def calling(otherpublicip):
    x = otherpublicip
    upnp = miniupnpc.UPnP()
    upnp.discoverdelay = 10
    upnp.discover()
    upnp.selectigd()
    port2 = 91424  # port for reciving the voice
    port1 = 91425  # port for sending the voice
    # addportmapping(external-port, protocol, internal-host, internal-port, description, remote-host)
    upnp.addportmapping(port2, 'TCP', upnp.lanaddr, port2, 'testing', '')
    upnp.addportmapping(port1, 'TCP', upnp.lanaddr, port1, 'testing', '')

    # code for calling

    audiorecv = AudioReceiver(socket.gethostbyname(socket.gethostname()), port2)
    audiosend = AudioSender(x, port1)

    # threads
    recivethread = threading.Thread(target=audiorecv.start_server)
    sendthread = threading.Thread(target=audiosend.start_stream)

    # sending and recive
    recivethread.start()
    sendthread.start()

    # close the ports
    # Get a list of all forwarded ports
    forwarded_ports = miniupnpc.get_forwarded_ports()
    # Close each forwarded port
    for port in forwarded_ports:
        miniupnpc.delete_port_mapping(port['external_port'], port['protocol'])
