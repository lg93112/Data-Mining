import DecisionTree
import RandomForest
from math import sqrt
import sys

train_file = sys.argv[1]
test_file = sys.argv[2]
train_data = DecisionTree.read_data(train_file)
test_data = DecisionTree.read_data(test_file)
classes = sorted(list(set([row[-1] for row in train_data]+[row[-1] for row in test_data])))


#path = ['balance.scale','led','nursery','synthetic.social']
#file = [[path[i]+'/'+path[i]+'.train', path[i]+'/'+path[i]+'.test'] for i in range(4)]
'''
train_data = DecisionTree.read_data(file[3][0])
test_data = DecisionTree.read_data(file[3][1])

actual_labels = [row[-1] for row in test_data]
predict_labels = DecisionTree.decision_tree(train_data, test_data, 8, 1)

total, accuracy, conf_matrix = DecisionTree.conf_matrix(actual_labels, predict_labels)
print(accuracy)
'''

def metrices(train_data, test_data, classes):
    actual_labels = []
    predict_labels = []
    for method in range(2):
        if method == 0:
    		print('Decision Tree:')
    		max_depth = DecisionTree.parameters(train_file)
    		for sets in ['train_set', 'test_set']:
    			if sets == 'train_set':
    			    print('training set')
    			    actual_labels = [row[-1] for row in train_data] 
    			    predict_labels = DecisionTree.decision_tree(train_data, train_data, max_depth, 1)
    				    
   
    			if sets == 'test_set':
    			    print('testing set')
    			    actual_labels = [row[-1] for row in test_data]
    			    predict_labels = DecisionTree.decision_tree(train_data, test_data, max_depth, 1)
    				 
    			total, accuracy, conf_matrix = DecisionTree.conf_matrix(actual_labels, predict_labels,classes)
    			print('overall accuracy: {}'.format(accuracy))
    			print_metrices(conf_matrix, total)
    			continue
        else:
    		print('Random Forest:')
    		max_depth = len(train_data[0])-1
    		F_features, tree_number = RandomForest.parameters(train_file)
    		for sets in ['train_set', 'test_set']:
    			if sets == 'train_set':
    				print('training set')
    				actual_labels = [row[-1] for row in train_data]
    				predict_labels = RandomForest.random_forest(train_data, train_data, max_depth, 1, 1, tree_number, F_features)
    			if sets == 'test_set':
    				print('testing set')
    				actual_labels = [row[-1] for row in test_data]
    				predict_labels = RandomForest.random_forest(train_data, test_data, max_depth, 1, 1, tree_number, F_features)
    			total, accuracy, conf_matrix = RandomForest.conf_matrix(actual_labels, predict_labels, classes)
    			print('overall accuracy: {}'.format(accuracy))
    			print_metrices(conf_matrix, total)
    		
    	
    return





def print_metrices(conf_matrix, total):
	for idx in range(len(conf_matrix[0])):
		predict_i = float(sum([row[idx] for row in conf_matrix]))
		P = float(sum(conf_matrix[idx]))
		N = float(total- P)
		TP = float(conf_matrix[idx][idx])
		FP = float(predict_i - TP)
		TN = float(total - predict_i - (P-TP))
		FN = float(P - TP)
		print('Class {}'.format(idx))

		if TP+TN == 0 and P+N == 0:
			print('Accuracy : {}'.format('UNDEF'))
		elif P+N == 0:
			print('Accuracy : {}'.format('INF'))
		else:
		    print('Accuracy : {}'.format((TP+TN)/(P+N)))

		if TN == 0 and N == 0:
			print('Specificity : {}'.format('UNDEF'))
		elif N == 0:
			print('Specificity : {}'.format('INF'))
		else:
		    print('Specificity : {}'.format(TN/N))
		
		if TP == 0 and TP+FP == 0:
			print('Precision : {}'.format('UNDEF'))
		elif TP+FP == 0:
			print('Precision : {}'.format('INF'))
		else:
		    print('Precision : {}'.format(TP/(TP+FP)))
		
		if TP == 0 and P == 0:
			print('Recall : {}'.format('UNDEF'))
		elif P == 0:
			print('Recall : {}'.format('INF'))
		else:
		    print('Recall : {}'.format(TP/P))

		if TP == 0 and (1+1*1)*TP+(1*1)*FN+FP == 0:
			print('F-1 Score : {}'.format('UNDEF'))
		elif (1+1*1)*TP+(1*1)*FN+FP == 0:
			print('F-1 Score : {}'.format('INF'))
		else:
			F1 = ((1+1*1)*TP)/((1+1*1)*TP+(1*1)*FN+FP)
			print('F-1 Score : {}'.format(F1))

		if TP == 0 and (1+0.5*0.5)*TP+(0.5*0.5)*FN+FP == 0:
			print('0.5F Score: {}'.format('UNDEF'))
		elif (1+0.5*0.5)*TP+(0.5*0.5)*FN+FP == 0:
			print('0.5F Score: {}'.format('INF'))
		else:
			F0_5 = ((1+0.5*0.5)*TP)/((1+0.5*0.5)*TP+(0.5*0.5)*FN+FP)
			print('0.5F Score: {}'.format(F0_5))

		if TP == 0 and (1+2*2)*TP+(2*2)*FN+FP == 0:
			print('2F Score: {}'.format('UNDEF'))
		elif (1+2*2)*TP+(2*2)*FN+FP == 0:
			print('2F Score: {}'.format('INF'))
		else:
			F2 = ((1+2*2)*TP)/((1+2*2)*TP+(2*2)*FN+FP)
			print('2F Score: {}'.format(F2))
	return


metrices(train_data, test_data, classes)
