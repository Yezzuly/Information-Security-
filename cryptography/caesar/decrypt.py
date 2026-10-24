with open("/challenge/caesarkey.txt", "r") as f:
    key_letter = f.read().strip()[-1]

key = ord(key_letter) - ord('A')

with open("/challenge/ciphertext.txt", "r") as f:
    ciphertext = f.read().strip()

plaintext = ""

for ch in ciphertext:
    c = ord(ch) - ord('A')
    p = (c - key) % 26
    plaintext += chr(p + ord('A'))

with open("caesarplaintext.txt", "w") as f:
    f.write(plaintext)