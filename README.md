# Information Security Coursework

Selected assignments from a graduate **Information Assurance & Security** course (CSE 543). The work covers classical cryptography, web application attacks, mutation-based fuzzing, and network spoofing. Each exercise was done against a controlled, instructor-provided lab environment (`pwn.college` and course-supplied targets), and each comes with a write-up explaining the reasoning rather than just the solution.

> **Scope & ethics.** Everything here was performed in isolated teaching labs built for exactly this purpose. The material is shared to document what I studied; it is not a toolkit for use against systems you don't own or aren't authorized to test. Captured flags and personal identifiers have been redacted.

## Contents

| Area | Assignment | Folder | What it demonstrates |
|---|---|---|---|
| Cryptography | Caesar cipher | `cryptography/caesar/` | Breaking a shift cipher by reversing the key and using modular arithmetic |
| Cryptography | Esper cipher | `cryptography/esper/` | Reversing a byte-level cipher (repeating-key XOR + bit rotation) |
| Web security | Pwn Them All | `web-attacks/` | Eight web-attack challenges, from client-side trust bugs to blind SQL injection |
| Fuzzing | Finding Crashes | `fuzzing/finding-crashes/` | Crafting inputs that crash a set-UID binary, with crash reproducers |
| Fuzzing | Fuzz Them All | `fuzzing/fuzz-them-all/` | A single target-agnostic mutation fuzzer run against ten binaries |
| Network security | TCP spoofing | `network-security/tcp-spoofing/` | Forging a TCP handshake to defeat source-IP authentication |
| Network security | UDP spoofing | `network-security/udp-spoofing/` | Source-IP spoofing against a connectionless service |

## Highlights

### Cryptography
Two decryption challenges where the goal was to recover plaintext from a known cipher construction. The **Caesar** solution reads the key letter, converts it to a numeric shift, and subtracts it modulo 26. The **Esper** solution reverses a more involved scheme that combines a repeating-key XOR with a per-byte bit rotation, operating on raw bytes rather than text. Each folder has the decryption script, the recovered plaintext, and a short write-up of how the cipher was reversed.

### Web attacks — Pwn Them All
A report covering eight escalating web challenges. Each one targets a different class of flaw, and the write-up explains the signal that exposed it and how it was exploited:
- Trusting client-controlled headers (`Referer`) to gate access to a script
- OS command injection through an unsanitized parameter
- Predictable record IDs derived from an MD5 of a known value
- Path traversal past a `realpath()` check that forgot to block `..`
- Hidden "admin" form fields that switched a script into a more trusting mode
- Server-side code execution via a header fed into `eval()`
- Boolean-based blind SQL injection to extract a password one character at a time
- Inspecting a raw HTTP response body that a browser would discard after a redirect

The throughline is that each bug comes from the server *trusting input it shouldn't* — headers, IDs, hidden fields, or a redirect body.

### Fuzzing
Two assignments on finding crashes through malformed input.
- **Finding Crashes** collects the specific inputs (`crashes/p_0` … `p_10`) that crash a stripped set-UID binary, alongside a report describing the static analysis (`strings`, `objdump`) that guided them.
- **Fuzz Them All** is the piece I'm most happy with: one mutation-based fuzzer, deliberately kept *blind* to which binary it targets. It only ever sees a fixed seed file, a PRNG seed, and an iteration count, so every run is fully reproducible. Finding each of the ten crashes came down to sweeping those two parameters until the target died from a SIGSEGV/SIGILL. The folder keeps the fuzzer, the seed, each level's crashing parameters (`levelN.txt`), the resulting crash input (`crashes/levelN.crash`), and the project report.

### Network security — spoofing
Two labs on bypassing authentication that relies only on a packet's source IP.
- **UDP spoofing** is the simpler case: UDP is connectionless, so a single forged datagram with a trusted source IP in the header is enough, with the real return address placed in the payload.
- **TCP spoofing** is harder and the write-up walks through why: completing a three-way handshake with a spoofed source means recovering the server's initial sequence number from the SYN-ACK, and stopping the kernel from tearing down a connection it doesn't recognize (an `iptables` rule to drop the stray RST). It's a concrete illustration of why TCP's handshake makes blind spoofing much more work than UDP's.

Both `readme` files lay out the objective, the thought process, and the key concepts (raw sockets, packet crafting with Scapy, sequence-number handling).

## What I practiced
- Reversing cryptographic constructions from their encryption code
- Recognizing and exploiting common web vulnerability classes (injection, traversal, broken access control, SSRF-style trust bugs)
- Building a reproducible mutation fuzzer and using crashes as evidence
- Low-level network behavior: raw sockets, the TCP handshake, and why source-IP trust is fragile
- Writing clear technical reports that explain the *why*, not just the exploit

## Notes on the files
- `report.pages` (Finding Crashes) is an Apple Pages document; `report.docx` (Fuzz Them All) is Word. GitHub won't preview Pages files — export to PDF before pushing if you want it viewable in the browser.
- The `.crash` files and `crashes/p_*` files are raw binary/byte inputs that trigger crashes; they aren't meant to be read as text.
