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

# Data intercepted from Wazuh Agent to Wazuh Manager
received_encrypted_data = 'fa0000002130303921234145533a613952813d9956ed042a68493d592e0e2934c5937a47f9fec1165fe67c5f2afa672bc948e2b8c49ea4258c14d93082120ca40db32c692e9a7a28acb028926d4d851ee295f7ae2b0d4ff7084f3fee041c72182c8c47514f71381829205db82c8ddc75f50532cc2e8dcd6f01bc4cb75914d0445f1bd5597676d8ea8a40550c7be1b2e57d3a4552f842df78b05c28f509fecfd161c8a42bcc1bb5f32d6ed83eb2eb293154a4633318cd4854216f2a87292317a109b0e60dbe5f3c620b69a5264ed9b2b9ec291367140828598dcb45818aec58f5d17c727bb1bffe4541b334410b179f124a9a4b2d3f597696ec89bdc26f56'  # Replace this with the actual encrypted data from your encryption script

# Convert hex data to bytes
data = bytes.fromhex(received_encrypted_data)

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
