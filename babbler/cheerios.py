# Cheerios Steganography Library
# ==============================
# 
# Implements a codec similar in spirit to the cryptographic technique of
# chaffing and winnowing (http://en.wikipedia.org/wiki/Chaffing_and_winnowing).
#
# Chaffing involves interleaving a plaintext message with other emissions in
# the same alphabet, such that the latter can only be winnowed out by receiver 
# sharing a secret.  Instead, we will be encoding binary data into an arbitrary 
# alphabet, with the goal that our transmission appear to come from an expected
# distribution soas not to suggest a hidden channel.  A typical use case would 
# be to embed arbitrary binary data in spam text.

import numpy as np
import struct
import binascii
from pmf import PMFTree

class CheerioCodec :
	def __init__ (self, probabilities) :
		# read probability table into PMFTree and generate decode table
		pass

	def emit (self, binary) :
		# return a symbol to emit and the number of bits consumed
		pass

	def encode (self, binary) :
		# collect emitted symbols in list until binary consumed and return
		pass

	def decode (self, symbols) :
		# construct a bitstream from the symbol or list of symbols
		pass

