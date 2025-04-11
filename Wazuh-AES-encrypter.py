from Crypto.Cipher import AES
import hashlib
import zlib
import binascii

# Function to create the block
def create_block(random_bytes, global_counter, local_counter, event):
    com1 = str(random_bytes) + str(global_counter)
    block = ":".join([str(com1), str(local_counter), event])
    return block

# Function to generate the MD5 hash of the block
def generate_hash(block):
    md5 = hashlib.md5(block.encode()).hexdigest()
    return md5

# Function to compress data
def compress_data(merged_data):
    return zlib.compress(merged_data)

# Function to add "!" padding to the compressed data
def add_padding(compressed_data):
    padding_len = (16 - len(compressed_data) % 16)
    padding = b'!' * padding_len
    return padding + compressed_data

# Function to encrypt the padded data using AES
def encrypt_data(padded_data, key, iv):
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
    return cipher.encrypt(padded_data)

# Convert Key to MD5
def generate_hashkey(key):
    md5key = hashlib.md5(key.encode()).hexdigest()
    return md5key

# Block Variables
random_bytes = '09660'
global_counter = '0000000217'
local_counter = '5417'
event = '5:fim_registry_value:{"component":"fim_registry_value","data":{"begin":"bf7d73bf961e87f87e29fcf6ef83a984099082c0","checksum":"a1a06a43ecd079ced172160cc4bb4ddea9f52bd6","end":"bf8703e84effcff1863e5410ac022229045d23b3","id":1744015875},"type":"integrity_check_right"}'

# Agent Key and Initial Vector
key = "b6a55196436b30d5c61e0394db7b5d2cfe61cd31557413586c1b80fb5981041c"
iv = b"FEDCBA0987654321"

# Step 0: Convert Key to MD5 (make sure it's 16 characters)
md5key = generate_hashkey(key)
print(f"Agent MD5 Key: {md5key} \n")

# Step 1: Create the block
block = create_block(random_bytes, global_counter, local_counter, event)
print(f"Block: {block} \n")

# Step 2: MD5 Hash
hash_value = generate_hash(block)
print(f"MD5 Block Hash (32-byte hexadecimal): {hash_value} \n")

# Step 3: Merge the MD5 hash with the block
merged_data = str(hash_value) + block
print(f"Merged Data (MD5 + Block): {merged_data} \n")

# Step 4: Compress data using zlib
compressed_data = compress_data(merged_data.encode())

# Step 5: Add "!" padding to the compressed data
padded_data = add_padding(compressed_data)
print(f"Data before Padding: {padded_data} \n")

# Step 6: Encrypt data using AES
encrypted_data = encrypt_data(padded_data, md5key, iv)
print(f"Encrypted Data Before Tagging: {encrypted_data} \n")

# Final Payload
agent_id = "009"
payload = f"!{agent_id}!#AES:".encode('utf-8') + encrypted_data
print(f"Payload after Tagging (Bytes): {payload} \n")
print(f"Final Payload (Hex): {binascii.hexlify(payload)} \n")
