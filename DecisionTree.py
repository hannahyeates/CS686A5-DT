from __future__ import division
import math
from operator import itemgetter

'''
def DecsionTreeLearn(examples, attributes, default):
	if examples == []:
		return default
	else if : 

'''
def safe_log(x):
	if x <= 0:
		return 0
	else:
		return math.log(x, 2)

def InitialEntropy(data):
	healthy = 0
	colic = 0
	for ln in data: 
		if ln[len(ln)-1] == 'healthy':
			healthy += 1
		if ln[len(ln)-1] == 'colic':
			colic += 1
	return - (colic/(healthy+colic))*math.log((colic/(healthy+colic)),2) - (healthy/(healthy+colic))*math.log((healthy/(healthy+colic)),2)

def InformationGain(data, threshold, idx, initEntropy):
	over = []
	overHealthy = 0
	under = []
	underHealthy = 0
	for line in data:
		if (line[idx] >= threshold):
			over.append(line)
			if line[len(line)-1] == 'healthy':
				overHealthy += 1
		else: 
			under.append(line)
			if line[len(line)-1] == 'healthy':
				underHealthy += 1
	probOver = len(over)/len(data)
	probUnder = len(under)/len(data)
	overEntropy = 0
	if len(over) > 0 :
		overEntropy = - overHealthy/(len(over))*safe_log(overHealthy/(len(over))) - (len(over) - overHealthy)/(len(over))*safe_log((len(over) - overHealthy)/(len(over)))
	underEntropy = 0
	if len(under) > 0 :
	 	underEntropy = - underHealthy/(len(under))*safe_log(underHealthy/(len(under))) - (len(under) - underHealthy)/(len(under))*safe_log((len(under) - underHealthy)/(len(under)))
	return initEntropy - (probOver*overEntropy + probUnder*underEntropy)

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

def chooseAttribute(attributes, examples):
	raise NotImplementedError



def DTL(examples, attributes, default):
	if len(examples) == 0:
		return default
	elif allSameClassification(examples):
		return examples[0][16]
	elif len(attributes) == 0:
		return mode(examples)
	else:
		bestAttribute = chooseAttribute(attributes, examples)





attributes = {
	'K' : 0,
	'Na': 1, 
	'CL': 2, 
	'HCO3' : 3, 
	'Endotoxin': 4, 
	'Aniongap': 5, 
	'PLA2': 6, 
	'SDH': 7, 
	'GLDH': 8, 
	'TPP' : 9,
	'Breath Rate': 10,
	'PCV': 11,
	'Pulse Rate': 12,
	'Fibrinogen': 13, 
	'Dimer':14,
	'FibPerDem':15
}

f = open("horseTrain.txt", "r")
data = []
for line in f:
	ln = line.split(',')
	values = []
	for i in range(len(ln)-2):
		values.append(float(ln[i]))
	values.append(ln[len(ln)-1][:-3])
	data.append(values)
initEntropy =  InitialEntropy(data)

thresholds = []
infoGains = []
for attr in range(len(attributes)-1):
	data = sorted(data, key = itemgetter(attr))
	infoGain = 0
	threshold = None

	for line in range(1, len(data)-1):
		tmp = InformationGain(data, data[line][attr], attr, initEntropy)
		if infoGain < tmp:
			infoGain = tmp
			threshold = data[line][attr]
	thresholds.append(threshold)
	infoGains.append(infoGain)

for i in thresholds:
	print i












