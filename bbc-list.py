import sys
from struct import unpack, pack
from getopt import getopt

Tokens = {

	0x80: "AND",
	0x81: "DIV",
	0x82: "EOR",
	0x83: "MOD",
	0x84: "OR",
	0x85: "ERROR",
	0x86: "LINE",
	0x87: "OFF",
	0x88: "STEP",
	0x89: "SPC",
	0x8a: "TAB(",
	0x8b: "ELSE",
	0x8c: "THEN",
	#0x8d - line number
	0x8e: "OPENIN",
	0x8f: "PTR",

	0x90: "PAGE",
	0x91: "TIME",
	0x92: "LOMEM",
	0x93: "HIMEM",
	0x94: "ABS",
	0x95: "ACS",
	0x96: "ADVAL",
	0x97: "ASC",
	0x98: "ASN",
	0x99: "ATN",
	0x9a: "BGET",
	0x9b: "COS",
	0x9c: "COUNT",
	0x9d: "DEG",
	0x9e: "ERL",
	0x9f: "ERR",

	0xa0: "EVAL",
	0xa1: "EXP",
	0xa2: "EXT",
	0xa3: "FALSE",
	0xa4: "FN",
	0xa5: "GET",
	0xa6: "INKEY",
	0xa7: "INSTR(",
	0xa8: "INT",
	0xa9: "LEN",
	0xaa: "LN",
	0xab: "LOG",
	0xac: "NOT",
	0xad: "OPENUP",
	0xae: "OPENOUT",
	0xaf: "PI",

	0xb0: "POINT(",
	0xb1: "POS",
	0xb2: "RAD",
	0xb3: "RND",
	0xb4: "SGN",
	0xb5: "SIN",
	0xb6: "SQR",
	0xb7: "TAN",
	0xb8: "TO",
	0xb9: "TRUE",
	0xba: "USR",
	0xbb: "VAL",
	0xbc: "VPOS",
	0xbd: "CHR$",
	0xbe: "GET$",
	0xbf: "INKEY$",

	0xc0: "LEFT$(",
	0xc1: "MID$(",
	0xc2: "RIGHT$(",
	0xc3: "STR$",
	0xc4: "STRING$(",
	0xc5: "EOF",
	0xc6: "AUTO",
	0xc7: "DELETE",
	0xc8: "LOAD",
	0xc9: "LIST",
	0xca: "NEW",
	0xcb: "OLD",
	0xcc: "RENUMBER",
	0xcd: "SAVE",
	0xce: "EDIT",
	0xcf: "PTR",

	0xd0: "PAGE",
	0xd1: "TIME",
	0xd2: "LOMEM",
	0xd3: "HIMEM",
	0xd4: "SOUND",
	0xd5: "BPUT",
	0xd6: "CALL",
	0xd7: "CHAIN",
	0xd8: "CLEAR",
	0xd9: "CLOSE",
	0xda: "CLG",
	0xdb: "CLS",
	0xdc: "DATA",
	0xdd: "DEF",
	0xde: "DIM",
	0xdf: "DRAW",

	0xe0: "END",
	0xe1: "ENDPROC",
	0xe2: "ENVELOPE",
	0xe3: "FOR",
	0xe4: "GOSUB",
	0xe5: "GOTO",
	0xe6: "GCOL",
	0xe7: "IF",
	0xe8: "INPUT",
	0xe9: "LET",
	0xea: "LOCAL",
	0xeb: "MODE",
	0xec: "MOVE",
	0xed: "NEXT",
	0xee: "ON",
	0xef: "VDU",

	0xf0: "PLOT",
	0xf1: "PRINT",
	0xf2: "PROC",
	0xf3: "READ",
	0xf4: "REM",
	0xf5: "REPEAT",
	0xf6: "REPORT",
	0xf7: "RESTORE",
	0xf8: "RETURN",
	0xf9: "RUN",
	0xfa: "STOP",
	0xfb: "COLOR", # COLOUR
	0xfc: "TRACE",
	0xfd: "UNTIL",
	0xfe: "WIDTH",
	0xff: "OSCLI"
}

def p(*objects):
	print(*objects, sep='', end='')

def main():

	pretty = False
	opts, args = getopt(sys.argv[1:], "-p", ["pretty"])
	for k, v in opts:
		if k in ('-p', '--pretty'): pretty = True


	for fname in args:
		with open(fname, "rb") as io:

			asm = False
			while True:
				data = io.read(4)
				# end of file
				if len(data) == 2 and data == b"\x0d\xff": break

				if len(data) != 4: raise Exception("bad file (1)")
				if data[0] != 0x0d: raise Exception("bad file (2): {:02x}".format(data[0]))

				space = False

				_, line, length = unpack(">BHB", data)

				p("{:-5d}".format(line))
				if pretty:
					p(' ')
					space = True

				data = io.read(length - 4)


				num = 0
				scratch = []

				quote = False
				comment = False
				for x in data:
					if num > 0:

						scratch.append(x)
						num = num - 1
						# print("{:02x} ".format(x), end='')


# 6502 disassembly:
#
# .L9BEE
#        INY
#        LDA     (L0B),Y
#        ASL     A
#        ASL     A
#        TAX
#        AND     #$C0
#        INY
#        EOR     (L0B),Y
#        STA     L2A
#        TXA
#        ASL     A
#        ASL     A
#        INY
#        EOR     (L0B),Y
#        STA     L2B
#        INY
#        STY     L0A
#        SEC
#        RTS
#
# z80 code does rotate instead of shift but the and #$c0 clears out the bits so it's equivalent.
# see also:
# https://xania.org/200711/bbc-basic-line-number-format

						if num == 0:
							a, b, c = scratch
							l = ((a << 2) & 0xc0) ^ b
							h = ((a << 4) & 0xc0) ^ c

							line = (h << 8) | l
							p(line)


						continue

					if x == 0x22:
						# double-quote
						quote = not quote

					if x == 0x20:
						# space
						# todo -- REM? asm comment?
						if pretty and not quote:
							if not space: p(' ')
							space = True
						else:
							p(' ')
						continue

					if x >= 0x20 and x <= 0x7f:
						if x == 0x3a and pretty and not quote: # :
							p(' : ')
							space = True
							continue

						p(chr(x))
						space = False
						continue

					if x == 0x8d: # line number...
						num = 3
						scratch = []
						continue

					if x in Tokens:
						if x == 0xf4: comment == True

						t = Tokens[x]
						if pretty and not space:
							p(' ')
						p(t)
						if pretty and t[-1] != '(':
							p(' ')
							space = True

						continue

					p(" **{:02x}** ".format(x))

				print("")



if __name__ == '__main__':
	main()
