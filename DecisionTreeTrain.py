from __future__ import division
import math
import copy
from operator import itemgetter
from collections import deque 
from DTNode import DTNode

def safe_log(x):
	if x <= 0:
		return 0
	else:
		return math.log(x, 2)

def InitialEntropy(examples):
	healthy = 0
	colic = 0
	for ln in examples: 
		if ln[len(ln)-1] == 'healthy':
			healthy += 1
		if ln[len(ln)-1] == 'colic':
			colic += 1
	return - (colic/(healthy+colic))*math.log((colic/(healthy+colic)),2) - (healthy/(healthy+colic))*math.log((healthy/(healthy+colic)),2)

def InformationGain(examples, threshold, idx, initEntropy):

	over = []
	overHealthy = 0
	under = []
	underHealthy = 0
	for line in examples:
		if (line[idx] >= threshold):
			over.append(line)
			if line[len(line)-1] == 'healthy':
				overHealthy += 1
		else: 
			under.append(line)
			if line[len(line)-1] == 'healthy':
				underHealthy += 1
	probOver = len(over)/len(examples)
	probUnder = len(under)/len(examples)
	overEntropy = 0
	if len(over) > 0 :
		overEntropy = - overHealthy/(len(over))*safe_log(overHealthy/(len(over))) - (len(over) - overHealthy)/(len(over))*safe_log((len(over) - overHealthy)/(len(over)))
	underEntropy = 0
	if len(under) > 0 :
	 	underEntropy = - underHealthy/(len(under))*safe_log(underHealthy/(len(under))) - (len(under) - underHealthy)/(len(under))*safe_log((len(under) - underHealthy)/(len(under)))
	
	return [initEntropy - probOver*overEntropy - probUnder*underEntropy, (probOver*overEntropy + probUnder*underEntropy)]

def allSameClassification(examples):
	if len(examples) == 1:
		return True
	value = examples[0][16]
	for i in range(1, len(examples)):
		if examples[i][16]<>value:
			return False
	return True


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

#return attribute and threshold
def chooseAttribute(attributes, completeAttributes, examples, initEntropy):
	thresholds = []
	infoGains = []
	bestGain = 0
	bestAttr = None
	bestAttrThreshold = 0
	bestAttrEntropy = 0
	attr = 4
	for attr in range(len(attributes)):
		if attr not in completeAttributes:
			examples = sorted(examples, key = itemgetter(attr))
			infoGain = 0
			threshold = None
			entropy = 0
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
				if (bestAttr == 10 and bestAttrThreshold == 12.00) or (bestAttr == 15 and bestAttrThreshold == 5.0031):
					print infoGain

	return [bestAttr, bestAttrThreshold, bestGain, entropy]


def makeAttributeList(complete, new):
	attributes = []
	for i in complete:
		attributes.append(complete)
	attributes.append(new)
	return attributes


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
		bestAttribute = chooseAttribute(attributes, completeAttributes, examples, initEntropy)
		dt = DTNode(bestAttribute[0])
		dt.threshold = bestAttribute[1]
		dt.infoGain = bestAttribute[2]
		dt.entropy = bestAttribute[3]
		leftExamples = []
		rightExamples = []
		for example in examples: 
			if example[dt.attribute] < dt.threshold:
				leftExamples.append(example)
			else:
				rightExamples.append(example)
		leftAttributes = makeAttributeList(completeAttributes, dt.attribute)
		rightAttributes	= makeAttributeList(completeAttributes, dt.attribute)
		dt.leftChild = DTL(leftExamples, attributes, leftAttributes, mode(leftExamples), dt.entropy)
		dt.rightChild = DTL(rightExamples, attributes, rightAttributes, mode(rightExamples), dt.entropy)
		return dt
			

		


def printDT(dt, attributes): 
	f = open('decisionTree.txt', 'w')
	q = deque()
	q.append(dt)
	while len(q) > 0:
		n = q.popleft()
		if n.leftChild <> None or n.rightChild <> None:
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

f = open("horseTrain.txt", "r")
examples = []
for line in f:
	ln = line.split(',')
	values = []
	for i in range(len(ln)-1):
		values.append(float(ln[i]))
	values.append(ln[len(ln)-1][:-3])
	examples.append(values)
initEntropy =  InitialEntropy(examples)

dt = DTL(examples, attributes, [], 'healthy', initEntropy)

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












