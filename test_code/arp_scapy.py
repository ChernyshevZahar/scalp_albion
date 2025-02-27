
from calendar import leapdays
import scapy.all as scapy
from scapy.layers import http
from scapy.all import raw
from scapy.all import bytes_hex

# print(scapy.ifaces)

arr_q_add = {}
arr_q=['104.66.114.184','192.168.0.139','51.105.71.137','162.254.198.104','188.114.98.160']#'192.168.0.152' '192.168.0.1',
arrtest =[]

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=proccer_sniffer_paket)
ports = ['2480','1680','2505','2509','8009','2516','https']
def proccer_sniffer_paket(pacet):
    try:
        f = open('text.txt', 'r')
        # print(f.read())
        arrIp = f.read().split()
        # print(arrIp)
        f.close()
        if pacet['IP'].src not in arrIp:
            # if pacet['IP'].src not in arrtest:

                print(pacet.getlayer('Raw').load)
                # pacet.show()
                # reqres(pacet,'192.168.0.152')
                print(pacet['IP'].src)
                arrtest.append(pacet['IP'].src)
                 
    except Exception as e:
        # print(e)
        pass
def reqres(pacet, q):
    if pacet['IP'].src == q or pacet['IP'].dst == q:
            if pacet['TCP'].ack != 0:
                if pacet['IP'].src == q:
                    arr_q_add[pacet['TCP'].ack] = pacet
                    # print(arr_q_add)
                elif pacet['IP'].dst == q:
                    if pacet['TCP'].seq in arr_q_add:
                        print('\n\n REQUEST\n\n')
                        print(arr_q_add[pacet['TCP'].seq].show())
                        arr_q_add.pop(pacet['TCP'].seq)
                        print('\n\n RESPONSE \n\n')
                        print(pacet.show())

sniff('Realtek 8822CE Wireless LAN 802.11ac PCI-E NIC')

