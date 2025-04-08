import re
from Crypto.Cipher import AES
import zlib
import binascii

# Function to remove padding
def remove_padding(data):
    return re.sub(b'^!+', b'', data)

# Function to decrypt the encrypted data using AES
def decrypt_data(encrypted_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

# Agent Key and Intial Vector
key = b"2bbc195974c7e0f66fe4a2e4b32f4cc4"
iv = b"FEDCBA0987654321"

received_encrypted_data = '2130303921234145533a4eb448d19d13126b42743833cc823071371d3f73bab521ee4e40294e615f59163057870964f22dba56473ef91f9c0858ac9c6f67a017b6cf9d6e0e6f92d3815a04acddcfdd13ce08e2827643f1d95feaa88e242508b7d25499385230e82bfa0a6e842e447884db033c8cc1054326b53a61f11a6c5bed38e19dd85ac269218dc376f5f3c38da056039abf4d35f1a5518dd873f13428b0021660efab852c531391e445680183a0bd0be2b057ed2103edd91087db52ed6ce627fb1aaeb00c3715909812005f303913aa3f30b9a7f1b6f2ef4b4571f6abf56d3eb4ac8919b6a51dc3'  # Replace this with the actual encrypted data from your encryption script

# Convert hex data to bytes
data = bytes.fromhex(received_encrypted_data)
print()
print(f"Message in bytes: {data}\n")
# Step 1: Check if the pattern "!<3-digit numbers>!#AES" exists in the payload
pattern = re.compile(rb'!(\d{3})!#AES:')

# Check if the pattern is found in the data
match = pattern.search(data)

if not match:
    print("The expected pattern !<3-digit numbers>!#AES was not found. Aborting decryption.")
else:
    print(f"Pattern matched: {match.group(0)} \n")
    
    match_start_index = match.end()
    data = data[match_start_index:]
    print(f"Remove Identifier: {data} \n")

# Step 1: Decrypt the received data
decrypted_data = decrypt_data(data, key, iv)
print(f"Decryted Message: {decrypted_data}\n")

# Step 2: Remove padding using regex
cleaned_data = remove_padding(decrypted_data)
print(f"Remove Padding: {cleaned_data} \n")

# Step 3: Decompress the cleaned data
try:
    decompressed_data = zlib.decompress(cleaned_data)
    print(f"Decompressed Plaintext: {decompressed_data} \n" )
except zlib.error as e:
    print("Error during decompression:", e)