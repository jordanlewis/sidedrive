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
import BitVector
from pmf import PMFArray as PMF

def emit (pmf, bv) :
	# return a symbol and the number of bits consumed
	symbol = None
	bits = 0
	while True :
		bit = bv[0]
		if bit == 0 :
			pmf2 = pmf.range_condition(0,0.5)
		else :
			pmf2 = pmf.range_condition(0.5, 1.0)
		symbol = pmf2.sample()

		
class CCNode :
	def __init__ (self, symbol=None, sp = 0.0, one = None, zero = None) :
		self.symbol = symbol
		self.sp = sp
		self.one = one
		self.zero = zero

	def _node (self, g) :
		# simple recursive call to populate graph with binary tree
		from pydot import Node, Edge
		n = Node(repr(self.symbol), label = "%r\nsp = %0.3f"%(self.symbol, self.sp))
		g.add_node(n)
		if not self.zero is None :
			g.add_edge(Edge(n, self.zero._node(g), label = '0'))
		if not self.one is None :
			g.add_edge(Edge(n, self.one._node(g), label = '1'))
		return n

class CheerioCodec :
	"""
	Steganography codec emitting based on the given PMF.
	"""
	def __init__ (self, pmf) :
		# populate codec tree
		self.root = CCNode()

		# if there is a perfect split, root need not consume symbol
		if pmf.cmf(pmf.inv_cmf(0.5)) == 0.5 :
			self.root.zero = CCNode()
			self.root.one = CCNode()
			self._split(pmf.range_condition(0.0, 0.5), self.root.zero)
			self._split(pmf.range_condition(0.5, 1.0), self.root.one)
		else :
			self._split(pmf, self.root)

		self.decode = {}

	def _split (self, pmf, node) :
		s = pmf.inv_cmf(0.5)
		p = pmf.get_p(s)
		node.symbol = s
		node.sp = p

		# establish bounds
		p1 = pmf.cmf(s)
		p0 = p1 - p

		# recur left if more symbols
		if pmf.outcomes[0] != s :
			node.zero = CCNode()
			self._split(pmf.range_condition(0.0, p0), node.zero)
		else :
			# if no chance to recur, lower stop probability
			node.sp *= 0.5

		# recur right if more symbols
		if pmf.outcomes[-1] != s :
			node.one = CCNode()
			self._split(pmf.range_condition(p1, 1.0), node.one)
		else :
			# if no chance to recur, lower stop probability
			node.sp *= 0.5

	def is_degenerate (self) :
		# can codec represent any bit sequence?
		return self.root.zero is None or self.root.one is None

	def emit (self, binary) :
		# return a symbol to emit and the number of bits consumed
		pass

	def encode (self, binary) :
		# collect emitted symbols in list until binary consumed and return
		pass

	def decode (self, symbols) :
		# construct a bitstream from the symbol or list of symbols
		pass

	def graph (self) :
		# generate a pydot graph of codec
		from pydot import Dot
		g = Dot()
		self.root._node(g)
		return g

	def information (self, node = None, depth = 0, in_p = 1.0) :
		if node == None :
			node = self.root

		h = depth * in_p * node.sp
		if node.zero is None :
			h += depth * (in_p / 2.0 - in_p * node.sp)
		else :
			h += self.information(node.zero, depth+1, in_p / 2 - in_p * node.sp)
		if node.one is None :
			h += depth * (in_p / 2.0 - in_p * node.sp)
		else :
			h += self.information(node.one, depth+1, in_p / 2 - in_p * node.sp)

		return h
		
	def pmf (self, node = None, pmf = None, in_p = 1.0) :
		if node == None :
			node = self.root
			pmf = PMF()

		if not node.symbol is None :
			pmf.count(node.symbol, in_p * node.sp)

		if node.zero is None :
			pmf.count(node.symbol, in_p * (1.0 - node.sp) * 0.5)
		else :
			self.pmf(node.zero, pmf, in_p * (1.0 - node.sp) * 0.5)
		if node.one is None :
			pmf.count(node.symbol, in_p * (1.0 - node.sp) * 0.5)
		else :
			self.pmf(node.one, pmf, in_p * (1.0 - node.sp) * 0.5)

		return pmf

