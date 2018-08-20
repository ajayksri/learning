import optparse

class xdump:
	def __init__(self, blocksize, decimal, encoding):
		self.__blocksize = blocksize
		self.__decimal = decimal
		self.__encoding = encoding

	@property
	def blocksize(self):
		return self.__blocksize

	@property
	def encoding(self):
		return self.__encoding

	@property
	def decimal(self):
		return self.__decimal

	@property
	def blockNumberFormat(self):
		return "{0:08}" if self.decimal else "{0:08X}"

	@property
	def headerLineOne(self):
		encodeHeader = "{0} characters".format(self.encoding)
		width = self.blocksize*2 + (self.blocksize//4) - 1
		return "Block     Bytes{0}  {1}".format(" "*(width-5), encodeHeader)

	@property
	def headerLineTwo(self):
		encodeHeaderLength = max(16, self.blocksize)
		width = self.blocksize*2 + (self.blocksize//4)
		return "________  {0}  {1}".format("_"*(width-1), "_"*encodeHeaderLength)

	def dumpFile(self, filename):
		blockNum = 0
		fh = None

		try:
			fh = open(filename, "rb")
			data = fh.read(self.blocksize)
			while data:
				blockSentence = self.blockNumberFormat.format(blockNum)
				bytesSentence = ""
				encodeSentence = []

				for byteNum,byteD in enumerate(data):
					if ((byteNum != 0) and (byteNum%4 == 0)):
						bytesSentence += " "
					bytesSentence += "{0:02X}".format(byteD)
					encodeSentence.append(byteD if 32 <= byteD < 127 else ord("."))

				if (len(data) < self.blocksize):
					remPlaces = (self.blocksize-len(data))*2 + (self.blocksize//4 - len(data)//4) - 1
					bytesSentence += " "*remPlaces

				line = [blockSentence, bytesSentence, bytes(encodeSentence).decode(self.encoding, "replace").replace("\uFFFD", ".")]
				print("  ".join(line))
				
				blockNum += 1
				data = fh.read(self.blocksize)
		except EnvironmentError as error:
			print(error)
		finally:
			if fh is not None:
				fh.close()

def parseOptions():
	parser = optparse.OptionParser(usage="usage: %prog [options] file1 [file2 [... fileN]]")
    
	parser.add_option("-b", "--blocksize", dest="blocksize", type="int", help=("block size (8..80) [default: 16]"))
	parser.add_option("-d", "--decimal", dest="decimal", action="store_true", help=("decimal block numbers [default: hexadecimal]"))
	parser.add_option("-e", "--encoding", dest="encoding", help=("encoding (ASCII..UTF-32) [default: %default]"))
	parser.set_defaults(blocksize=16, decimal=False, encoding="UTF-8")
	 
	return parser.parse_args()


if __name__ == "__main__":
	opts, files = parseOptions()
	xd = xdump(opts.blocksize, opts.decimal, opts.encoding)
	print(xd.headerLineOne)
	print(xd.headerLineTwo)
	for afile in files:
		xd.dumpFile(afile)
