# pmf - implementations of frequency table pmf functions
import numpy as np
from random import random

class PMFArray :
	"""
	Represents a categorical distribution with numpy arrays for vector-based
	calculations.
	"""
	def __init__ (self) :
		self.k = 0
		self.idx = {}
		self.outcomes = []
		self.counts = np.array([])
		self.cumsum = np.array([])
		self.total = 0

		# flags whether cumsum needs recomputation
		self._dirty = False

	def __str__ (self) :
		return str([(self.outcomes[i], self.counts[i]) for i in xrange(self.k)])

	def _clean (self) :
		# updates cumsum if necessary; called before cumsum is used
		if self._dirty :
			self.cumsum = np.cumsum(self.counts)
			self._dirty = False

	def count (self, outcome, n = 1) :
		# increment frequency for given outcome by n
		idx = self.idx.get(outcome)
		if idx is None :
			idx = self.k
			self.idx[outcome] = idx
			self.k += 1
			self.outcomes.append(outcome)
			self.counts = np.append(self.counts, 0)

		self.counts[idx] += n
		self.total += n
		self._dirty = True

	def inv_cmf (self, p) :
		if p < 0 or p > 1 :
			raise Exception("p outside [0,1]: %f"% p)
		self._clean()

		v = p * self.total
		idx = np.searchsorted(self.cumsum, v)
		return self.outcomes[idx]

	def get_p (self, outcome) :
		idx = self.idx.get(outcome)
		if idx is None :
			raise Exception("Unknown outcome: %s"%outcome)
		return self.counts[idx] / self.total

	def range_condition (self, p0, p1) :
		if p0 < 0 or p0 > 1 :
			raise Exception("p0 outside [0,1]: %f" % p0)
		if p1 < 0 or p1 > 1 :
			raise Exception("p1 outside [0,1]: %f" % p1)
		if p1 <= p0 :
			raise Exception("p0 >= p1: %s" % (p0, p1))
		self._clean()

		# cuts in frequency space
		v0 = self.total * p0
		v1 = self.total * p1

		# iterate through touched values and add to new PMF
		cpmf = PMFArray()
		i0, i1 = np.searchsorted(self.cumsum, (v0,v1))
		for i in xrange(i0, i1+1) :
			vi = min(self.cumsum[i], v1)
			cpmf.count(self.outcomes[i], vi - v0)
			v0 = vi
	
		return cpmf

	def sample (self) :
		if self.total == 0 :
			return None
		p = random()
		return self.inv_cmf(p)


class PMFTree :
	"""
	Represents a categorical distribution as a Fenwick tree based on its
	frequency count, allowing fast online adjustments and inverse CDF lookups 
	(and thus sampling).
	"""
	pass
