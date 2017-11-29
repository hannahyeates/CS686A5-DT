# this class contains all information about each node in the decision tree for the learning process
class DTNode(object):
	def __init__(self, attribute):
		self.attribute = attribute
		self.infoGain = None
		self.threshold = None
		self.leftChild = None
		self.rightChild = None
		self.entropy = None

