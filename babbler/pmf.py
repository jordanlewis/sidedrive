# pmf - implementations of frequency table pmf functions

class PMFArray :
	"""
	Represents a categorical distribution with numpy arrays for vector-based
	calculations.
	"""
	def __init__ (self) :
		pass

	def count (self, outcome, n = 1) :
		# increment frequency for given outcome by n
		pass

	def inv_cdf (self, p) :
		# get the outcome at a given probability
		pass

	def sample (self, context) :
		pass

	def get_count (self, outcome = None) :
		# return total count or count of given outcome
		pass


class PMFTree :
	"""
	Represents a categorical distribution as a Fenwick tree based on its
	frequency count, allowing fast online adjustments and inverse CDF lookups 
	(and thus sampling).
	"""
	def __init__ (self) :
		pass

	def count (self, outcome, n = 1) :
		# increment frequency for given outcome by n
		pass

	def inv_cdf (self, p) :
		# get the outcome at a given probability
		pass

	def sample (self, context) :
		pass

	def get_count (self, outcome = None) :
		# return total count or count of given outcome
		pass
