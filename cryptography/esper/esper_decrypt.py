def rrot(n, d):
    return ((n >> d) | (n << (8 - d))) & 0xff


with open("/challenge/experkey.txt", "r") as f:
    line = f.read().strip()

key_str = line.split(" is ")[1].split(" rotated")[0]
rot = int(line.split("by ")[1].split()[0])

keyxor = [ord(c) for c in key_str]

with open("/challenge/ciphertext.txt", "rb") as f:
    ciphertext = f.read()

plaintext = bytearray()

for i, b in enumerate(ciphertext):
    x = b ^ keyxor[i % len(keyxor)]
    p = rrot(x, rot)
    plaintext.append(p)

with open("esper_plaintext.txt", "wb") as f:
    f.write(plaintext)
