import pickle
import string
from sklearn import datasets

filepath = 'sent.data.train'
abbrev = 'classes/abbrevs'
internal = 'classes/sentence_internal'


#Integer



try:
	data = open(filepath)
	abbrevclass = open(abbrev)
	internalclass = open(internal)

	#Segregate the datafile into different lists
	Result = []
	LineNum = []
	NegWords = []
	PosWords = []
	NextDeli = []
	PrevDeli = []
	SpacesFollow = []

	abrevlist = []
	interlist = []

	try:

		for each_word in abbrevclass:
			each_word = each_word.split()
			abrevlist.append(each_word[0])

		for each_word in internalclass:
			each_word = each_word.split()
			interlist.append(each_word[0])



		for each_line in data:
			each_line = each_line.split() #Separate attributes of each line by space
			

			Result.append(each_line[0])
			LineNum.append(each_line[1])
			NegWords.append(each_line[4])
			PosWords.append(each_line[6])
			NextDeli.append(each_line[9])
			PrevDeli.append(each_line[10])
			SpacesFollow.append(each_line[11])
	except ValueError:
			pass

		

#################################################
# +- Word Features:				#
#	Length					#
#	If is punctuation			#
#	If is number				#
# 	If capital 				#
#	In abbrev class				#
#	In internal class			#
#################################################

#################################################
#Running check for neg words

	#Check Length
	negLEN = []
	for each_item in NegWords:
		length=len(each_item)
		negLEN.append(length)

	#Check if in abbrev class
	negINABBREV = []
	for each_item in NegWords:
		if each_item in abrevlist:
			negINABBREV.append('1')
		else:
			negINABBREV.append('0')

	
	#Check if in internal class
	negININTERNAL = []
	for each_item in NegWords:
		if each_item in interlist:
			negININTERNAL.append('1')
		else:
			negININTERNAL.append('0')
			

	#Check if is not puntcuation 
	negPUNCcheck = []

	for each_item in NegWords:
		if each_item in string.punctuation or each_item =="<P>" or each_item == "``"or each_item == "''":
			negPUNCcheck.append('1')
		else:
			negPUNCcheck.append('0')

	#Check if is a number
	negNUMcheck = []

	for each_item in NegWords:
		IsNum = each_item.replace('.','').isdigit()  #Replace decimal point and check if result is number
		if IsNum:
			negNUMcheck.append('1')
		else:
			negNUMcheck.append('0')

	#Check if is capital
	negCAPcheck = []

	for each_item in NegWords:
		each_item = list(each_item)
		IsCap = each_item[0].isupper()
		if IsCap:
			negCAPcheck.append('1')
		else:
			negCAPcheck.append('0')



			

##################################################
#Running check for pos words

	#Check Length
	posLEN = []
	for each_item in PosWords:
		length=len(each_item)
		posLEN.append(length)

	#Check if in abbrev class
	posINABBREV = []
	for each_item in PosWords:
		if each_item in abrevlist:
			posINABBREV.append('1')
		else:
			posINABBREV.append('0')

	
	#Check if in internal class
	posININTERNAL = []
	for each_item in PosWords:
		if each_item in interlist:
			posININTERNAL.append('1')
		else:
			posININTERNAL.append('0')

	#Check if is not puntcuation 
	posPUNCcheck = []

	for each_item in PosWords:
		if each_item in string.punctuation or each_item =="<P>" or each_item == "``"or each_item == "''":
			posPUNCcheck.append('1')
		else:
			posPUNCcheck.append('0')

	#Check if is a number
	posNUMcheck = []

	for each_item in PosWords:
		IsNum = each_item.replace('.','').isdigit()  #Replace decimal point and check if result is number
		if IsNum:
			posNUMcheck.append('1')
		else:
			posNUMcheck.append('0')

	#Check if is capital
	posCAPcheck = []

	for each_item in PosWords:
		each_item = list(each_item)
		IsCap = each_item[0].isupper()
		if IsCap:
			posCAPcheck.append('1')
		else:
			posCAPcheck.append('0')



##################################################
#	Append all Features together

	SentenceAttributes = []
	for each_word in Result:
		SentenceAttributes.append([each_word])

	cnt = 0

	for each_word in SentenceAttributes:

	#Adding Negative Word attributes
		each_word.append(negLEN[cnt])
		each_word.append(negPUNCcheck[cnt])
		each_word.append(negNUMcheck[cnt])
		each_word.append(negCAPcheck[cnt])
		each_word.append(negINABBREV[cnt])
		each_word.append(negININTERNAL[cnt])

	#Adding Positive Word attributes
		each_word.append(posLEN[cnt])
		each_word.append(posPUNCcheck[cnt])
		each_word.append(posNUMcheck[cnt])
		each_word.append(posCAPcheck[cnt])
		each_word.append(posINABBREV[cnt])
		each_word.append(posININTERNAL[cnt])

	#Adding Next/Prev Delimiter and Spaces follow attributes
		each_word.append(NextDeli[cnt])
		each_word.append(PrevDeli[cnt])
		each_word.append(SpacesFollow[cnt])
	
		cnt += 1

##########################################

		



except IOError as err:
	print('File error:' + str(err))
		

	



