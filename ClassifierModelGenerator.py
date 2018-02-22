import sys
import argparse
import pickle
import string
from collections import Counter
from sklearn import tree
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

def get_args():
	parser = argparse.ArgumentParser(description = 'Eat in feature files and train a decisiontree model')
	parser.add_argument("--mode", type=str, required=True, help="Training or testing, use either 'train' or 'test'. ")
	parser.add_argument("--fp", type=str, required=True, help="The feature file path")
	parser.add_argument("--mp", type=str, required=True, help="File name and path for saving generated model")
	parser.add_argument("--k", type=int, help="K-fold numbers for data sets to be divided ", default=10)
	args = parser.parse_args()
	return args

args = get_args()

mode = args.mode
featurefilepath = args.fp
modelsavepath = args.mp
knumber = args.k

Labelnames = []
Features = []

try:
	with open('Label.Names','rb') as feature_file:
		Labelnames = pickle.load(feature_file)
	with open(featurefilepath,'rb') as feature_file:
		Features = pickle.load(feature_file)
except IOError as err:
	print('File error '+ str(err))
except pickle.PickleError as perr:
	print('Pickling error: ' + str(perr))

TempClass = []
LabelClass = []
#Prepare text features and the related labels
for each_line in Features:
	TempClass.append(each_line[0])
	each_line.pop(0)


for each_label in TempClass:
	n = Labelnames.index(each_label)
	LabelClass.append(n)



#In training mode
if mode == 'train':
	#Separate data with KFolds and fit for test in cross_validation

	numFolds = knumber

	kf = KFold(n_splits = numFolds)


	cnt = 0
	accuracy = []
	testF = []
	testL = []
	bestscore = 0
	for train_index, test_index in kf.split(Features):
	
	
		TrainFeatures = []
		TrainLabels = []
		TestFeatures = []
		TestLabels = []

		for index in train_index:
			TrainFeatures.append(Features[index])
			TrainLabels.append(LabelClass[index])
		for index in test_index:
			TestFeatures.append(Features[index])
			TestLabels.append(LabelClass[index])



		#Use DecisionTree to train the model with cross validation
		Classifier = tree.DecisionTreeClassifier(random_state = 0)
		Classifier.fit(TrainFeatures,TrainLabels)

		accuracy.append(Classifier.score(TestFeatures,TestLabels))
		
	

		if cnt == 0:
			GoodModel = Classifier
			bestscore = accuracy[0]	
		elif cnt > 0:
			if accuracy[cnt] >= accuracy[cnt-1]:
				bestscore = accuracy[cnt]*100			
				GoodModel = Classifier
				testF = TestFeatures
				testL = TestLabels 
	

		cnt += 1
	#End of KFold


	#Print best score
	print("From cross validation, the best score it gets: %.2f" % bestscore,"%.") 



	#Save the test feature/label for hand testing
	PredictionLabel = GoodModel.predict(Features)


	cnt = 0
	wrong = 0

	markedwrong = []

	for each_label in PredictionLabel:
		if each_label != LabelClass[cnt]:
			wrong += 1
			markedwrong.append(Labelnames[LabelClass[cnt]])
		cnt += 1

	accuracy = (len(testL) - wrong) / len(testL)
	errpct = 100*wrong/len(testL) 


	print("This many errors: ",wrong,".")
	print("Percentage of errors: %.2f"%errpct,"%.")
	print("These labels are labeled wrong: ",Counter(markedwrong))

	try:

	#	pickle the classifier for further use	

		pickle.dump(GoodModel,open(modelsavepath,'wb'))
	except IOError as err:
		print('File error: ' +str(err))
elif mode == 'test':
	
	try:
		GoodModel = pickle.load(open(modelsavepath,'rb'))
	except IOError:
		pass

	PredictionLabel = GoodModel.predict(Features)

	cnt = 0
	wrong = 0

	markedwrong = []

	for each_label in PredictionLabel:
		if each_label != LabelClass[cnt]:
			wrong += 1
			markedwrong.append(Labelnames[LabelClass[cnt]])
		cnt += 1

	accuracy = (len(LabelClass) - wrong) / len(LabelClass)
	errpct = 100*(1-wrong/len(LabelClass))


	print("Percentage of accuracy: %.2f"%errpct,"%.")
	print("This many errors: ",wrong,".")
	print("These labels are labeled wrong: ",Counter(markedwrong))

else:
	print("Error: 'Wrong mode keyword. Either use 'train' or 'test' for related mode.'")
	exit()



