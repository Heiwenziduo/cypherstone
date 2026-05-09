# import time
# from Crypto.Cipher import AES, PKCS1_OAEP
# from Crypto.PublicKey import RSA
# from Crypto.Random import get_random_bytes

# # 测试数据：1KB (RSA 2048 无法直接加密 1KB，需分块，这正好体现了它的笨重)
# data = get_random_bytes(1024) 

# # AES 测试
# start = time.time()
# cipher_aes = AES.new(get_random_bytes(32), AES.MODE_EAX)
# cipher_aes.encrypt(data)
# print(f"AES 耗时: {time.time() - start:.6f}s")

# # RSA 测试 (仅加密一小段密钥，模拟它的正常用法)
# key = RSA.generate(2048)
# cipher_rsa = PKCS1_OAEP.new(key.publickey())
# start = time.time()
# cipher_rsa.encrypt(get_random_bytes(128)) # RSA 只能加密极小数据
# print(f"RSA 加密小块耗时: {time.time() - start:.6f}s")