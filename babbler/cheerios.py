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
#
# TODO: DRY for branching logic
# TODO: eliminate recursion with stacks

import numpy as np
from BitVector import BitVector
from pmf import PMFArray as PMF
from random import randint, random

class CCNode :
	def __init__ (self, symbol=None, zero = None, one = None, \
									 zsp = 0.0, osp = 0.0, bv = None) :
		self.symbol = symbol
		self.zero = zero
		self.one = one
		self.zsp = zsp
		self.osp = osp

	def _node (self, g) :
		# simple recursive call to populate graph with binary tree
		from pydot import Node, Edge
		label = '%r'%self.symbol
		if self.symbol != None :
			label += '\n%s'%self.bv
		n = Node(repr(self), label = label)
		g.add_node(n)
		if not self.zero is None :
			g.add_edge(Edge(n, self.zero._node(g), 
					label = '0\n%.3f'%(self.zsp)))
		if not self.one is None :
			g.add_edge(Edge(n, self.one._node(g), 
					label = '1\n%.3f'%(self.osp)))
		return n

class CheerioCodec :
	"""
	Steganography codec emitting based on the given PMF.
	"""
	def __init__ (self, pmf) :
		# populate codec tree
		self.root = CCNode()
		self.lookup = {}

		self._build_tree(pmf, self.root)
		self._build_table(self.root)

	def _build_table (self, node, code = None) :
		if code is None :
			code = BitVector(bitstring='')
		node.bv = code
		if not node.symbol is None :
			self.lookup[node.symbol] = code
		if not node.zero is None :
			self._build_table(node.zero, code + BitVector(bitstring='0'))
		if not node.one is None :
			self._build_table(node.one, code + BitVector(bitstring='1'))

	def _build_tree (self, pmf, node) :
		# pick partitions to move largest entries highest in tree
		# sort symbols by descending probability
		l = [ (pmf.get_p(symbol), symbol) for symbol in pmf.outcomes ]
		l.sort(reverse = True)

		# greedily assign each to smallest partition
		zs = []
		zp = 0.0
		os = []
		op = 0.0
		for (p, s) in l :
			if zp <= op :
				zs.append((p, s))
				zp += p
			else :
				os.append((p, s))
				op += p

		if zp == 0.5 :
			# perfect split! don't waste symbol on node
			node.symbol = None
			node.zsp = node.osp = 0.0
		elif zp == 1.0 :
			# terminal node! skip the rest
			node.symbol = zs[0][1]
			node.zero = node.one = None
			node.zsp = node.osp = 1.0
			return
		else :
			# always put more weight on zero partition to simplify code
			if zp < op :
				zp, op = op, zp
				zs, os = os, zs

			# remove overweight and assign to node
			p, s = zs.pop()
			zp -= p	
			node.symbol = s
			node.zsp = 1 - 2 * zp
			node.osp = 1 - 2 * op

		# recur left if more symbols
		if len(zs) :
			zs = [ s for p, s in zs ]
			node.zero = CCNode()
			self._build_tree(pmf.set_condition(zs), node.zero)
		else :
			node.zero = None
			node.zsp = 1.0
			node.osp = 2 * p - 1

		# recur right if more symbols
		if len(os) :
			os = [ s for p, s in os ]
			node.one = CCNode()
			self._build_tree(pmf.set_condition(os), node.one)
		else :
			node.one = None
			node.osp = 1.0
			node.zsp = 2 * p - 1

	def is_degenerate (self) :
		# can codec represent any bit sequence?
		return (self.root.zero is None) or (self.root.one is None)

	def encode (self, binary, max_symbols = None) :
		# collect emitted symbols in list until binary consumed and return
		# NOTE: Cheerio symbols may encode extra bits.  External protocol
		# must encode message tokenization (e.g. length header or stop code)
		symbols = []
		bits = 0
		while len(binary) > 0 and \
				(max_symbols is None or len(symbols) < max_symbols) :
			node = self.root
			bits = 0
			while node != None:
				# determine next branch
				if len(binary) > 0 :
					bit = binary[0]
				else :
					bit = randint(0,1)
				if bit == 0 :
					p = node.zsp
					n = node.zero
				else :
					p = node.osp
					n = node.one

				# attempt to continue or emit on failure
				if random() < p :
					symbols.append(node.symbol)
					bits += len(self.lookup[node.symbol])
					break
				else :
					node = n
					if len(binary) == 1 :
						binary = BitVector(bitstring='')
					else :
						binary = binary[1:]
		return symbols, bits

	def decode (self, symbols) :
		# construct a bitstream from the list of symbols
		bv = BitVector(bitstring = '')
		for symbol in symbols :
			bs = self.lookup[symbol]
			if len(bs) > 0 :
				bv += self.lookup[symbol]
		return bv

	def graph (self) :
		# generate a pydot graph of codec
		from pydot import Dot
		g = Dot()
		self.root._node(g)
		return g

	def information (self) : 
		pmf = self.pmf()
		h = 0
		for symbol in pmf.outcomes :
			h += pmf.get_p(symbol) * len(self.lookup[symbol])

		return h
		
	def pmf (self, node = None, pmf = None, in_p = 1.0) :
		if node == None :
			node = self.root
			pmf = PMF()

		if not node.symbol is None :
			pmf.count(node.symbol, in_p * 0.5 * (node.zsp + node.osp))
		if not node.zero is None :
			self.pmf(node.zero, pmf, in_p * (1.0 - node.zsp) * 0.5)
		if not node.one is None :
			self.pmf(node.one, pmf, in_p * (1.0 - node.osp) * 0.5)

		return pmf

