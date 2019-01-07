import base64, hashlib

def shakikoo(string):
	"""Encrypt a password with the ShaKikoo algorithm."""
	sha256 = hashlib.sha256(string.encode()).hexdigest() # SHA256
	sha_chars = [ord(l) for l in sha256] # Convert result to integers
	sha_chars.extend([-9,26,-90,-34,-113,23,118,-88,3,-99,50,-72,-95,86,-78,-87,62,-35,67,-99,-59,-35,-50,86,-45,-73,-92,5,74,13,8,-80]) # salt it

	shakikoo = bytes([((b>>4) & 15)*16+(b & 15) for b in sha_chars]) # doing shakikoo stuff

	# re-hash with SHA256 and converting to base64 string
	return base64.b64encode(hashlib.sha256(shakikoo).digest()).decode() # return the hash