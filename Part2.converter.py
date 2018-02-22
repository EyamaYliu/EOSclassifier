import pickle
import argparse
import string
import re

def get_args():
	parser = argparse.ArgumentParser(description = 'Convert file in assignment2 format into Text Classification feature file')
	parser.add_argument("--rp", type=str, required=True, help="Raw data file in Part 2 format")
	parser.add_argument("--fp", type=str, required=True, help="Path to save feature file")
	args = parser.parse_args()
	return args

args = get_args()


datafilepath = args.rp
savepath = args.fp



#Clean out label of sentence tool

def labelcleaner(sentence):
	deletecnt = 0
	for each_str in sentence:
		
		if each_str not in string.whitespace:
			deletecnt += 1
		else:			
			sentence = sentence[deletecnt:]
			return sentence

#Counting tool
count = lambda l1,l2: len(list(filter(lambda c: c in l2,l1)))

#Split without any puncuation
def CleanSplitter(sentence):
	sentence = ''.join(c for c in sentence if c not in string.punctuation)
	sentence = sentence.split()
	return sentence

def findLABEL(sentence):
	label = CleanSplitter(sentence)[0]
	return label




#Feature extractors

def WORDcnt(sentence):
	num = len(CleanSplitter(sentence))
	return num

def WHITEcnt(sentence):
	num = count(sentence,string.whitespace)
	return num

def PUNCcnt(sentence):
	num = count(sentence,string.punctuation)
	return num

def NUMcnt(sentence):
	num = count(sentence,string.digits)
	return num

def leadingspace(sentence):
	sentence = labelcleaner(sentence)
	num = len(sentence) - len(sentence.lstrip())
	return num

def LETTERcnt(sentence):
	num = count(sentence,string.ascii_letters)
	return num

def UPPERcnt(sentence):
	num = count(sentence,string.ascii_uppercase)
	return num

def EMAILMARKcnt(sentence):
	num = count(sentence,'@')
	return num
	
def INDENTcnt(sentence):
	num = count(sentence,'\t')  

	return num

def QUOTATIONcnt(sentence):
	num = count(sentence,':')

	return num

def firstPUNCsignpos(sentence):
	cnt = 0
	quotpos = 0
	while cnt < len(sentence):
		if sentence[cnt] in string.punctuation:
			quotpos = cnt
			return quotpos
		cnt += 1
	return quotpos





#Open up file and put everything into a list of strings
try:
	data = open(datafilepath)

	lines = [] #Text themselfs
	Labelnames = [] #Unique label names
	Tempclass = []

	try:
		cnt = 0
		for each_line in data:	
			#Skip feature extracting for #BLANK# lines
			#if findLABEL(each_line) == 'BLANK':
				#continue

			lines.append(each_line)	
			#Convert Label 

			Tempclass.append(findLABEL(lines[cnt]))

			cnt += 1

		#Set Unique Label classes
		#Labelnames = list(set(Tempclass))
	except ValueError:
			pass
except IOError as err:
	print('File error:' + str(err))
	exit()

#################################################
# Feature extraction rules:			#
#	Num of words				#
#	Num of whitespaces			#
#	Num of punctuations			#
#	Num of numbers				#
#	Num of leadingspaces			#
#	Num of letters				#
#	Num of UPPERletters			#
#	Num of EMAILMARKs			#
#	Num of INDENTations			#
#	Num of QUOTATIONs			#
#	Position of 1st QUOTATIONs		#
#################################################

cleanlines = []


#Make sure cleanlines only have lines without any label in front
cnt = 0
while cnt < len(lines):
	if CleanSplitter(lines[cnt])[0] in Labelnames:
		cleanlines.append(labelcleaner(lines[cnt]))
	else:
		cleanlines.append(lines[cnt])
	cnt += 1





numWords = []
numWhtspc = []
numPunc = []
numNum = []
numLdspc = []
numLetter = []
numUpper = []
numEmlMk = []
numIndent = []
posPunc = []

for each_line in cleanlines:
	numWords.append(WORDcnt(each_line))
	numWhtspc.append(WHITEcnt(each_line))
	numPunc.append(PUNCcnt(each_line))
	numNum.append(NUMcnt(each_line))
	numLdspc.append(leadingspace(each_line))
	numLetter.append(LETTERcnt(each_line))
	numUpper.append(UPPERcnt(each_line))
	numEmlMk.append(EMAILMARKcnt(each_line))
	numIndent.append(INDENTcnt(each_line))
	posPunc.append(firstPUNCsignpos(each_line))




#Initializing Features with label, then append each converted features
Features = []
cnt = 0



while cnt <len(Tempclass):
	Features.append([Tempclass[cnt]])
	cnt += 1

cnt = 0
for each_item in Features:
	each_item.append(numWords[cnt])
	each_item.append(numWhtspc[cnt])
	each_item.append(numPunc[cnt])
	each_item.append(numNum[cnt])
	each_item.append(numLdspc[cnt])
	each_item.append(numLetter[cnt])
	each_item.append(numUpper[cnt])
	each_item.append(numEmlMk[cnt])
	each_item.append(numIndent[cnt])
	each_item.append(posPunc[cnt])

	cnt+=1
	
try:


	#	Let's test for pickle	

	with open(savepath,'wb') as converted_file:
		pickle.dump(Features,converted_file)
except IOError as err:
	print('File error: ' +str(err))


Labelnames = ['TABLE', 'ADDRESS', 'HEADL', 'SIG', 'BLANK', 'GRAPHIC', 'NNHEAD', 'QUOTED', 'PTEXT', 'ITEM']


try:


	#	Let's test for pickle	

	with open('Label.Names','wb') as converted_file:
		pickle.dump(Labelnames,converted_file)
except IOError as err:
	print('File error: ' +str(err))









