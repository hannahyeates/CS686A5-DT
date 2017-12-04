'''
	This file contains all the logic for learning the decision tree
	from the training set of data given in horseTrain.py
'''


from __future__ import division
import math
import copy
from operator import itemgetter
from collections import deque 
from DTNode import DTNode

# Method to ensure that log(0) returns zero instead of an error
def safe_log(x):
	if x <= 0:
		return 0
	else:
		return math.log(x, 2)


# Gets the initial entropy of the training data set
def InitialEntropy(examples):
	healthy = 0
	colic = 0
	for ln in examples: 
		if ln[len(ln)-1] == 'healthy':
			healthy += 1
		if ln[len(ln)-1] == 'colic':
			colic += 1
	return - (colic/(healthy+colic))*math.log((colic/(healthy+colic)),2) - (healthy/(healthy+colic))*math.log((healthy/(healthy+colic)),2)

# Calculates the information gain for a given attribute with a given threshold over a set of examples
def InformationGain(examples, threshold, idx, initEntropy):
	over = []
	overHealthy = 0
	under = []
	underHealthy = 0
	for line in examples:
		# add to the set of data points that fall over the threshold of the attribute
		if (line[idx] >= threshold):
			over.append(line)
			if line[len(line)-1] == 'healthy':
				overHealthy += 1
		# add to the set of data points that fall under the threshold of the attribute
		else: 
			under.append(line)
			if line[len(line)-1] == 'healthy':
				underHealthy += 1
	# calculate the percentage of data points that fall over and under the threshold
	probOver = len(over)/len(examples)
	probUnder = len(under)/len(examples)
	
	# calcuulate the entropy of data points that fall over and under the threshold
	overEntropy = 0
	if len(over) > 0 :
		overEntropy = - overHealthy/(len(over))*safe_log(overHealthy/(len(over))) - (len(over) - overHealthy)/(len(over))*safe_log((len(over) - overHealthy)/(len(over)))
	underEntropy = 0
	if len(under) > 0 :
	 	underEntropy = - underHealthy/(len(under))*safe_log(underHealthy/(len(under))) - (len(under) - underHealthy)/(len(under))*safe_log((len(under) - underHealthy)/(len(under)))
	
	# Return the information gain of the given threshold
	return [initEntropy - probOver*overEntropy - probUnder*underEntropy, (probOver*overEntropy + probUnder*underEntropy)]

# Helper function to determine if all examples are classified the same
def allSameClassification(examples):
	if len(examples) == 1:
		return True
	value = examples[0][16]
	for i in range(1, len(examples)):
		if examples[i][16]!=value:
			return False
	return True

# Helper function to calculate the mode of a set of examples
def mode(examples):
	healthy = 0
	colic = 0
	for i in examples:
		if i[16] == 'healthy':
			healthy += 1
		else:
			colic += 1
	if healthy >= colic:
		return 'healthy'
	return 'colic'

# This method chooses which attribute gives the largest information gain by 
# calculating which attribute produces the best gain for each feature and comparing
# them.
# This method returns the best attribute, the threshold, the gain, and the resulting entropy
def chooseAttribute(attributes, completeAttributes, examples, initEntropy):
	thresholds = []
	infoGains = []
	bestGain = 0
	bestAttr = None
	bestAttrThreshold = 0
	bestAttrEntropy = 0
	# iterate through all of the attribute that have not already appeared in the tree
	for attr in range(len(attributes)):
		if attr not in completeAttributes:
			examples = sorted(examples, key = itemgetter(attr))
			infoGain = 0
			threshold = None
			entropy = 0
			# Calculate information gain for each example given an attribute to use
			for line in range(1, len(examples)-1):
				tmp = InformationGain(examples, examples[line][attr], attr, initEntropy)
				if infoGain < tmp[0]:
					infoGain = tmp[0]
					threshold = examples[line][attr]
					entropy = tmp[1]
			
			if infoGain > bestGain:
				bestGain = infoGain
				bestAttr = attr
				bestAttrThreshold = threshold
				bestAttrEntropy = entropy

	return [bestAttr, bestAttrThreshold, bestGain, entropy]

# Helper function to make a new list of attributes to pass into the left and right child methods
def makeAttributeList(complete, new):
	attributes = []
	for i in complete:
		attributes.append(complete)
	attributes.append(new)
	return attributes

# Main function for learning the decision tree. 
def DTL(examples, attributes, completeAttributes, default, initEntropy):
	if len(examples) == 0:
		node = DTNode(default)
		return node
	elif allSameClassification(examples):
		node = DTNode(examples[0][16])
		return node
	elif len(completeAttributes) == 16:
		node = DTNode(mode(examples))
		return node
	else:
		# get the best attribute from the choose attribute function
		bestAttribute = chooseAttribute(attributes, completeAttributes, examples, initEntropy)
		# build the root of a decision tree containing that attribute
		dt = DTNode(bestAttribute[0])
		dt.threshold = bestAttribute[1]
		dt.infoGain = bestAttribute[2]
		dt.entropy = bestAttribute[3]
		leftExamples = []
		rightExamples = []
		# split examples into each side of the threshold
		for example in examples: 
			if example[dt.attribute] < dt.threshold:
				leftExamples.append(example)
			else:
				rightExamples.append(example)
		# get the attribute list for the left child and right child
		leftAttributes = makeAttributeList(completeAttributes, dt.attribute)
		rightAttributes	= makeAttributeList(completeAttributes, dt.attribute)
		dt.leftChild = DTL(leftExamples, attributes, leftAttributes, mode(leftExamples), dt.entropy)
		dt.rightChild = DTL(rightExamples, attributes, rightAttributes, mode(rightExamples), dt.entropy)
		return dt
			

		

# Helper function to write the decision tree to a file
def printDT(dt, attributes): 
	f = open('decisionTree.txt', 'w')
	q = deque()
	q.append(dt)
	while len(q) > 0:
		n = q.popleft()
		if n.leftChild != None or n.rightChild != None:
			f.write(str(n.attribute) + ',' + str(n.threshold) + ',' + str(n.leftChild.attribute) + ', ' + str(n.rightChild.attribute) +'\n') 
	
		if n.leftChild is not None:
			q.append(n.leftChild)
		if n.rightChild is not None:
			q.append(n.rightChild)
	f.close()

attributes = {
	0: 'K', 
	1: 'Na', 
	2: 'CL', 
	3: 'HCO3', 
	4: 'Endotoxin', 
	5: 'Aniongap', 
	6: 'PLA2', 
	7: 'SDH', 
	8: 'GLDH', 
	9: 'TPP',
	10: 'Breath Rate',
	11: 'PCV',
	12: 'Pulse Rate',
	13: 'Fibrinogen', 
	14: 'Dimer',
	15: 'FibPerDem'
}


# Start here
f = open("horseTrain.txt", "r")
examples = []
for line in f:
	ln = line.split(',')
	values = []
	# format all values for processing
	for i in range(len(ln)-1):
		values.append(float(ln[i]))
	values.append(ln[len(ln)-1][:-3])
	examples.append(values)
# calculate the initial entropy
initEntropy =  InitialEntropy(examples)

# recursively learn the decision tree
dt = DTL(examples, attributes, [], 'healthy', initEntropy)

# attributes to make it easier to print out the decision tree
displayAttributes = {
	0: 'K', 
	1: 'Na', 
	2: 'CL', 
	3: 'HCO3', 
	4: 'Endotoxin', 
	5: 'Aniongap', 
	6: 'PLA2', 
	7: 'SDH', 
	8: 'GLDH', 
	9: 'TPP',
	10: 'Breath Rate',
	11: 'PCV',
	12: 'Pulse Rate',
	13: 'Fibrinogen', 
	14: 'Dimer',
	15: 'FibPerDem',
	'colic': 'colic',
	'healthy' : 'healthy'
}

printDT(dt, displayAttributes)












