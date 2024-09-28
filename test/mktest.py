from itertools import batched
import sys
import struct

n = 10
for chunk in batched(range(0x80, 0x100), 8):
	chunk = [bytes([x]) for x in chunk if x != 0x8d ]
	line = b' ' + b' '.join(chunk)


	header = struct.pack(">BHB", 0x0d, n, len(line) + 4)
	sys.stdout.buffer.write(header)
	sys.stdout.buffer.write(line)

	n = n + 10


sys.stdout.buffer.write(b"\x0d\xff")

