import pickle
import string
from collections import Counter
from sklearn import tree
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


Features = []

try:
	with open('segment.feature','rb') as feature_file:
		Features = pickle.load(feature_file)

except IOError as err:
	print('File error '+ str(err))
except pickle.PickleError as perr:
	print('Pickling error: ' + str(perr))

TempClass = []
Labelnames = []
LabelClass = []
#Prepare text features and the related labels
for each_line in Features:
	TempClass.append(each_line[0])
	each_line.pop(0)

Labelnames = list(set(TempClass))

for each_label in TempClass:
	n = Labelnames.index(each_label)
	LabelClass.append(n)


#Separate data with KFolds and fit for test, cross_validation

numFolds = 5

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
	EOSClassifier = tree.DecisionTreeClassifier(random_state = 0)
	EOSClassifier.fit(TrainFeatures,TrainLabels)

	accuracy.append(EOSClassifier.score(TestFeatures,TestLabels))
		
	

	if cnt == 0:
		GoodModel = EOSClassifier
		bestscore = accuracy[0]	
	elif cnt > 0:
		if accuracy[cnt] >= accuracy[cnt-1]:
			bestscore = accuracy[cnt]*100			
			GoodModel = EOSClassifier
			testF = TestFeatures
			testL = TestLabels 
	

	cnt += 1
#End of KFold

print("From cross validation, the best score it gets: %.2f" % bestscore,"%.") #Print best score



#Save the test feature/label for hand testing
PredictionLabel = GoodModel.predict(testF)


cnt = 0
wrong = 0

markedwrong = []

for each_label in PredictionLabel:
	if each_label != testL[cnt]:
		wrong += 1
		markedwrong.append(Labelnames[testL[cnt]])
	cnt += 1

accuracy = (len(testL) - wrong) / len(testL)
errpct = 100*wrong/len(testL) 

print("This many errors: ",wrong,".")
print("Percentage of errors: %.2f"%errpct,"%.")
print("These labels are labeled wrong: ",Counter(markedwrong))

try:

#	pickle the classifier for further use	

	with open('Part2.model','wb') as model_file:
		pickle.dump(GoodModel,model_file)
except IOError as err:
	print('File error: ' +str(err))


