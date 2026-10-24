========================================================================
UDP Spoofing Assignment - Solution Thought Process & Design
========================================================================

1. Problem Analysis & Objective:
   - A UDP service named 'FlagServ' is active at 10.0.0.3:13337.
   - The service implements a Source-IP-based authentication scheme, strictly trusting only the IP address '10.2.4.10'.
   - Upon validating the packet, the service reads the target IP string from the UDP payload and transmits the flag via UDP to port 13337 of that specified target.
   - Objective: Bypass the Source-IP validation mechanism using raw sockets to successfully exfiltrate the flag.

2. Technical Design & Exploit Analysis:
   - Unlike TCP, UDP is entirely connectionless and lacks a handshake protocol. Consequently, the target server processes incoming datagrams individually and validates the identity of the sender relying solely on the "Source IP" field inside the IP header.
   - By leveraging raw sockets via Python's Scapy library, low-level network control is gained to manually forge the network stack.
   - A forged IP layer with 'src="10.2.4.10"' is injected to bypass FlagServ's authentication filter.
   - Instead of hardcoding an uninitialized Layer 2 MAC address, the script builds a Layer 3 packet, allowing Scapy to dynamically resolve the destination MAC address of 10.0.0.3 via ARP.
   - Simultaneously, the actual environment IP '10.0.0.2' is provided within the data payload. This forces the authenticated server to transmit the flag back to the local terminal host.

3. Step-by-Step Execution & Verification:
   - Step 1: A background UDP socket listener is initialized on the local container interface to capture the incoming flag payload: `nc -ulu 13337`
   - Step 2: The attack script (`attack_spoof.py`) is executed. The script injects the manually crafted, identity-spoofed raw UDP packet into the virtual network.
   - Step 3: FlagServ receives the frame, matches the forged source IP against the trusted whitelist, parses the payload ("10.0.0.2"), and successfully forwards the flag directly to the waiting Netcat listener instance.

4. Captured Flag Result:
   - The exploit successfully forced the server to leak the flag to the active listener:
     pwn.college{REDACTED}

5. Conclusion:
   - The flag was successfully fetched and captured. This challenge highlights the fundamental architectural risks of relying purely on connectionless transport parameters (such as UDP Source IP) for establishing security boundaries and access control.

========================================================================
