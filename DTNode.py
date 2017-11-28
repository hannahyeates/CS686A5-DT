class DTNode(object):
	def __init__(self, attribute):
		self.attribute = attribute
		self.infoGain = None
		self.threshold = None
		self.leftChild = None
		self.rightChild = None
		self.entropy = None

