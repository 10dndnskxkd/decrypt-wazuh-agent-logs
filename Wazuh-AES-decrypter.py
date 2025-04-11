import re
from Crypto.Cipher import AES
import zlib
import binascii
import hashlib

# Function to remove padding
def remove_padding(data):
    return re.sub(b'^!+', b'', data)

# Function to decrypt the encrypted data using AES
def decrypt_data(encrypted_data, key, iv):
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

# Convert Key to MD5
def generate_hashkey(key):
    md5key = hashlib.md5(key.encode()).hexdigest()
    return md5key

# Agent Key and Intial Vector
key = "b6a55196436b30d5c61e0394db7b5d2cfe61cd31557413586c1b80fb5981041c"
iv = b"FEDCBA0987654321"

received_encrypted_data = '8a0000002130303921234145533a9aac9950d3096134f3166ae3f965989f1f613de843e1d0e4aa9a894750a2f1531c2e9a19231bab4d10a9a583a8bcf89551971f732e14195a1e71dca509174ed633deea1498e0ae8c580a3e1f9be5904dfffabd59beab278dd93a70be39bb846795a6a4eb59c3ffc6084f9284dcef6ad355a4ee2d87e286dc7bcfcb761c00d1ff'  # Replace this with the actual encrypted data from your encryption script

# Step 0: Convert Key to MD5 (make sure it's 16 characters)
key = generate_hashkey(key)
print(f"Agent MD5 Key: {key} \n")

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
    print(f"Decompressed Plaintext: {decompressed_data.decode('utf -8')} \n" )
except zlib.error as e:
    print("Error during decompression:", e)
