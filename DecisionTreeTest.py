'''
	This file contains all code related to testing (or using) the decision tree 
	to classify the examples of horses.
	This file takes the decision tree as output and will print out the classifications 
	of the test set to the console.
'''

from collections import deque

# classifies the data based on the attribute values given
def Classify(dt, startNode, data):
	attribute = startNode
	while True:
		# return if we reach a terminal node
		if attribute == 'healthy' or attribute == 'colic':
			return attribute
		check = data[int(attribute)]
		# check thresholds to determine whether to take the left path or the
		# right path
		if check < dt[attribute]['threshold']:
			attribute = dt[attribute]['leftChild']
		elif check >= dt[attribute]['threshold']:
			attribute = dt[attribute]['rightChild']
		



tree = open("decisionTree.txt", "r")
dt = {}
startNode = None
queue = deque()	
data = []
# Builds a dictionary to represent the decision tree
for line in tree:
	if startNode == None:
		startNode = line[0].strip()
	data.append(line.split(','))
	line = line.split(',')
	dt[line[0].strip()] = {'threshold': float(line[1].strip()), 'leftChild': line[2].strip(), 'rightChild': line[3].strip()}

f = open("horseTest.txt", "r")
data = []
correctClassifications = []
# read in and format the data for classification
for line in f:
	tmp = line.split(',')
	features = []
	for i in tmp:
		i = i.strip()
		if i <> 'healthy.' and i <> 'colic.':
			features.append(float(i))
	data.append(features)
	correctClassifications.append(tmp[16].strip()[:-1])

classifications = []
# classify and print data, ending with printing the error. 
for i in data:
	classifications.append(Classify(dt,startNode, i))
	print classifications[len(classifications)-1]
error = 0
for i in range(len(correctClassifications)):
	if classifications[i] <> correctClassifications[i]:
		error += 1
print error





