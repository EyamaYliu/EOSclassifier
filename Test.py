import pickle
import string
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import  cross_val_predict

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
		negLEN.append([length])

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

	LableClass = []
	for each_word in Result:
	#If end of sentence,label '1'. If not,lable '0'
		if each_word == 'EOS':
			LableClass.append(1)
		else:
			LableClass.append(0)
			

	cnt = 0

	Features = []
#Init the first attribute of Features to be negative word length
	for each_item in negLEN:
		Features.append(each_item)



	for each_word in Features:
	#Adding Negative Word attributes
		each_word.append(int(negPUNCcheck[cnt]))
		each_word.append(int(negNUMcheck[cnt]))
		each_word.append(int(negCAPcheck[cnt]))
		each_word.append(int(negINABBREV[cnt]))
		each_word.append(int(negININTERNAL[cnt]))

	#Adding Positive Word attributes
		each_word.append(int(posLEN[cnt]))
		each_word.append(int(posPUNCcheck[cnt]))
		each_word.append(int(posNUMcheck[cnt]))
		each_word.append(int(posCAPcheck[cnt]))
		each_word.append(int(posINABBREV[cnt]))
		each_word.append(int(posININTERNAL[cnt]))

	#Adding Next/Prev Delimiter and Spaces follow attributes
		each_word.append(int(NextDeli[cnt]))
		each_word.append(int(PrevDeli[cnt]))
		each_word.append(int(SpacesFollow[cnt]))
		cnt += 1

##########################################
	


	#Separate data with Training and Test groups. Train on 80%, test on 20%
	numofTrain = int(len(Features)*0.8)

	TrainFeatures = Features[0:numofTrain]
	TrainLabels = LableClass[0:numofTrain]
	TestFeatures = Features[numofTrain:len(Features)]
	TestLables = LableClass[numofTrain:len(Features)]
	

	#Use LinearSVC to train the model with cross validation
	EOSClassifier = LinearSVC(random_state = 0)
	EOSClassifier.fit(TrainFeatures,TrainLabels)
	#score = cross_val_score(EOSClassifier,TrainFeatures,TrainLabels,cv = 5)
	
	
	#Test accuracy on train data, and predict a label
	
	accuracy = EOSClassifier.score(TestFeatures,TestLables)
	PredictionLabel = EOSClassifier.predict(TestFeatures)
	print(PredictionLabel)
	
	Right = 0
	Wrong = 0
	cnt = 0

	"""#Check for accuracy
	for each_item in predict:
		if each_item == TestLables[cnt]:
			Right += 1
		else:
			Wrong += 1
		cnt += 1
	accuracy = 100*(Right/(Right+Wrong))"""

	print(accuracy)
	
	

	


	data.close()
	abbrevclass.close()
	internalclass.close()
except IOError as err:
	print('File error:' + str(err))
		

	



