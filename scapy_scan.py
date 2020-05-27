import scapy.all

#Higher Layer Socket required to detect response on localhost
#https://scapy.readthedocs.io/en/latest/troubleshooting.html
scapy.all.conf.L3socket=scapy.all.L3RawSocket

for i in range(1,255):
    ip=("192.168.0.{}".format(i))
    #request=scapy.all.IP(dst=ip)/scapy.all.UDP(dport=0)
    #request=scapy.all.IP(dst=ip)/scapy.all.ICMP(type="timestamp-request")
    request=scapy.all.IP(dst=ip)/scapy.all.ICMP(type="echo-request")
    response=scapy.all.sr1(request,timeout=.2, verbose=0)
    print("{}: {}".format(ip, "Up" if response else "Down"))
