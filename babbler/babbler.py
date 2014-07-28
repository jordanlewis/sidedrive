# Babbler - Embed messages in natural-ish language.
#
# Uses the Cheerios codec to embed arbitrary binary in text matching the
# distribution from an ngram-based language model.

from mgram import MGramModel
from cheerios import CheerioCodec as CC
from math import ceil
from BitVector import BitVector as BV

DELIM = ' '

class Babbler :
	"""
	Codec to string using mgram model.
	"""
	#FIXME 255 character max

	def __init__ (self, mgm) :
		self.mgm = mgm

	def encode (self, bv) :
		header = BV(intVal = int(ceil(len(bv)/8)), size = 8)
		bv = header + bv
		symbols = []
		while True :
			pmf = self.mgm.get_cmf(symbols)
			if hasattr(pmf, 'cc') :
				cc = pmf.cc
			else :
				cc = CC(pmf)
				pmf.cc = cc
			symbol, bits = cc.encode(bv, 1)
			symbols.append(symbol[0])
			if bits >= len(bv) :
				return DELIM.join(symbols)
			else :
				bv = bv[bits:]

	def decode (self, s) :
		bv = BV(size=0)
		symbols = s.split(DELIM)
		while len(symbols) :
			symbol = symbols.pop()
			pmf = self.mgm.get_cmf(symbols)
			if hasattr(pmf, 'cc') :
				cc = pmf.cc
			else :
				cc = CC(pmf)
				pmf.cc = cc
			bv = cc.decode([symbol]) + bv
		header = bv[:8]
		length = header.intValue()
		msg = bv[8:8+8*length]
		return msg
