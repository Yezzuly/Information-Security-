TCP Spoofing
------------------------------------------
OBJECTIVE
------------------------------------------
The goal of this assignment was to bypass source-IP-based authentication
on a TCP service (FlagIt) running at 10.0.0.3:13337. The service trusts
only the IP address 10.2.4.10, and sends a flag via UDP to port 13337
of a user-specified destination IP.

------------------------------------------
THOUGHT PROCESS & SOLUTION
------------------------------------------

Step 1 - Understanding the Authentication Mechanism
    FlagIt authenticates users solely based on the source IP address of
    the incoming TCP connection. If the source IP is 10.2.4.10, the
    server considers the user trusted and sends the flag via UDP to the
    destination IP provided in the TCP payload.

Step 2 - Identifying the Attack Vector
    Since authentication is based only on the source IP, I can forge
    (spoof) the source IP of my TCP packets to 10.2.4.10 using raw
    sockets. This is a classic IP spoofing attack.

Step 3 - Challenges with TCP Spoofing

    Challenge 1: Unknown Server ISN
        TCP requires a proper 3-way handshake (SYN → SYN-ACK → ACK).
        The server responds to my SYN with a SYN-ACK containing a
        randomly chosen Initial Sequence Number (ISN). My ACK must
        correctly acknowledge this ISN (ISN+1), or the server will
        discard subsequent packets.
        Solution: Use Scapy's sr1() to actually receive the SYN-ACK
        and extract the server's ISN before sending the ACK.

    Challenge 2: Kernel Sending RST Automatically
        When the server sends SYN-ACK to 10.2.4.10, the packet arrives
        at my machine (same /24 subnet). Since my machine does not own
        10.2.4.10, the Linux kernel automatically sends a RST packet,
        tearing down the connection before I can complete the handshake.
        Solution: Use iptables to drop outgoing RST packets on the
        specific source port used for this session:
        iptables -A OUTPUT -p tcp --sport <PORT> --tcp-flags RST RST -j DROP

    Challenge 3: ARP / MAC Resolution Failure
        Without specifying the network interface explicitly, Scapy fails
        to resolve the MAC address and sends packets as broadcast or
        drops them entirely.
        Solution: Explicitly set iface="eth0" in all Scapy send/receive
        calls.

Step 4 - Attack Execution Flow
    1. Add iptables rule to block RST on the chosen source port.
    2. Start a background UDP sniffer on port 13337 to capture the flag.
    3. Send a spoofed SYN packet (src=10.2.4.10) to 10.0.0.3:13337.
    4. Receive the SYN-ACK using sr1() and extract the server's ISN.
    5. Send a spoofed ACK with ack=server_ISN+1 to complete the handshake.
    6. Send the payload "10.0.0.2\n" so the server sends the flag via
       UDP to our real IP address (10.0.0.2) on port 13337.
    7. Capture the incoming UDP packet and print the flag.
    8. Clean up the iptables rule.

------------------------------------------
KEY CONCEPTS DEMONSTRATED
------------------------------------------
- Raw socket programming
- IP spoofing using Scapy
- Manual TCP 3-way handshake construction
- ISN (Initial Sequence Number) extraction
- Bypassing kernel RST interference via iptables
- UDP flag capture via packet sniffing

------------------------------------------
TOOLS USED
------------------------------------------
- Python 3
- Scapy (packet crafting and sniffing)
- iptables (RST suppression)
- Linux raw sockets
