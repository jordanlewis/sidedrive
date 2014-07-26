# mgram - Markov Chain model of a corpus based on n-gram frequencies.
from collections import namedtuple
from pmf import PMFArray as PMF

class MGramModel :
	"""
	Markov-Chain model of a corpus based on n-gram frequencies.
	"""

	# Trie node
	Node = namedtuple('Node', ('symbol', 'cmf', 'children'))

	def __init__ (self, n) :
		self.n = n
		self.root = MGramModel.Node(None, PMF(), {})

	def train (self, ngram, w = 1) :
		# incorporate ngram into frequency tables
		if len(ngram) != self.n :
			raise Exception("ngram length does not match n: %d"%len(ngram))

		node = self.root
		for symbol in ngram :
			node.cmf.count(symbol, w)
			if not node.children.has_key(symbol) :
				node.children[symbol] = MGramModel.Node(symbol, PMF(), {})
			node = node.children[symbol]

	def get_cmf (self, context=[]) :
		context = context[-(self.n-1):]
		node = self.root
		for symbol in context :
			node = node.children.get(symbol)
			if node is None :
				#FIXME recursive hack to step back ngram models 
				if len(context) > 0 :
					return self.get_cmf(context[1:])
				else :
					return PMF()

		return node.cmf

	def emit (self, n, context=[], entropy=True) :
		if len(self.root.children) == 0 :
			return None

		out = [] + context
		h = 0
		for i in xrange(n) :
			cmf = self.get_cmf(out)
			# restart at root if stuck
			if cmf.total == 0 :
				cmf = self.root.cmf

			symbol = cmf.sample()
			out.append(symbol)
			if entropy :
				h += cmf.entropy()

		out = out[len(context):]
		if entropy :
			return out, h
		else :
			return out

		

def mgm_from_corpus (corpus, n = 3) :
	import nltk
	words = nltk.word_tokenize(corpus)
	ngrams = nltk.ngrams(words, n)
	mgm = MGramModel(n)
	for ngram in ngrams :
		mgm.train(ngram)
	return mgm
