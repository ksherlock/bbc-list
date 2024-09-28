
import random
import sys
import struct

def encode(x):
	lo = x & 0xff
	hi = (x >> 8) & 0xff

	return bytes([
		(((lo & 0xc0) >> 2) | (( hi & 0xc0) >> 4)) ^ 0x54,
		(lo & 0x3f) | 0x40,
		(hi & 0x3f) | 0x40,
	])


nums = [random.randint(1, 32767) for x in range(20)]
nums.sort()

for n in nums:

	line = b" \x8d" + encode(n)
	header = struct.pack(">BHB", 0x0d, n, len(line) + 4)
	sys.stdout.buffer.write(header)
	sys.stdout.buffer.write(line)

sys.stdout.buffer.write(b"\x0d\xff")