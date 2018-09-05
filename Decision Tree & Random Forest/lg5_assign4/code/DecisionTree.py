import sys
from random import randrange


def read_data(file_path):
	with open(file_path) as f:
		data = []
		for line in f:
			line = line.strip().split(' ')
			pairs = line[1:]
			dic = {-1:int(line[0])}
			for pair in pairs:
				pair = [int(i) for i in pair.split(':')]
				dic[pair[0]] = pair[1]
			data.append(dic)
	return data


def train_attributes(train):
	dic = {}
	attributes = sorted(train[0].keys())[1:]
	for idx in attributes:
		values = [row[idx] for row in train]
		values = list(set(values))
		dic[idx] = values
	return dic


def divide_groups(index,dataset,attr_values):
	dic = {}
	values = attr_values[index]
	for i in values:
		dic[i] = []
	for row in dataset:
		dic[row[index]].append(row)
	return dic.keys(), dic.values()


def gini_index(groups, classes):
	D = float(sum([len(group) for group in groups]))
	gini = 0.0
	for group in groups:
		Di = float(len(group))
		if Di == 0:
			continue
		summ = 0.0
		for val in classes:
			pi = [row[-1] for row in group].count(val) / Di
			summ += pi * pi
		gini += (1.0 - summ) * (Di / D)
	return gini


def best_attr(dataset, attributes, attr_values): 
	classes = list(set(row[-1] for row in dataset))
	best_gini, best_groups = 1000, None
	best_idx, best_vals = None, None
	for idx in attributes:
		values, groups = divide_groups(idx, dataset, attr_values)
		gini = gini_index(groups, classes)
		if gini < best_gini:
			best_idx, best_gini, best_vals, best_groups = idx, gini, values, groups
	child_attr = list(attributes)
	child_attr.remove(best_idx)
	return {'index': best_idx, 'values': best_vals, 'groups': best_groups, 'child_attr' : child_attr}



def leaf(group, majority):
	if len(group) == 0:
		return majority
	class_val = [row[-1] for row in group]
	classes = set(class_val)
	num, clas = 0, None
	for val in classes:
		if class_val.count(val)>num :
			clas, num = val, class_val.count(val)
	return clas


def children(node, max_depth, min_num, depth, attr_values):
	node['child'] = []
	majority_vote = []
	for group in node['groups']:
		if len(group) != 0:
			for row in group:
				majority_vote.append(row[-1])
	majority = max(set(majority_vote), key=majority_vote.count)
	if depth >= max_depth-1 or not node['child_attr']:
		for group in node['groups']:
			node['child'].append(leaf(group, majority))
		return
	for idx, group in enumerate(node['groups']):
		classes = set([row[-1] for row in group])
		if len(group) <= min_num or len(classes)==1:
			node['child'].append(leaf(group, majority))
		else:
			node['child'].append(best_attr(group, node['child_attr'], attr_values))
			children(node['child'][idx], max_depth, min_num, depth+1, attr_values)
	return


def build_tree(dataset, max_depth, min_num, attr_values):
	attributes = sorted(dataset[0].keys())[1:]
	root = best_attr(dataset,attributes, attr_values)
	children(root, max_depth, min_num, 0, attr_values)
	return root


def predict(node, row):
	index = -2
	for idx,value in enumerate(node['values']):
		if value == row[node['index']]:
			index = idx; break;
	if index == -2:
		index = randrange(len(node['values']))
	if isinstance(node['child'][index], dict):
		return predict(node['child'][index], row)
	else:
		return node['child'][index]

def decision_tree(train, test, max_depth, min_num):
	attr_values = train_attributes(train)
	tree = build_tree(train, max_depth, min_num, attr_values)
	predictions = [predict(tree, row) for row in test]
	return predictions



def conf_matrix(actual_labels, predict_labels, classes):
	confusion_matrix = []
	idx_dict = {}
	for idx,value in enumerate(actual_labels):
		if(idx_dict.get(value) == None):
			idx_dict[value] = []
		idx_dict[value].append(idx)
	total_num = 0.0
	for clas in classes:
		if idx_dict.has_key(clas):
			index = idx_dict[clas]
			predicts = [predict_labels[i] for i in index]
			counts = [predicts.count(cl) for cl in classes]
		else:
			counts = [0] * len(classes)
		confusion_matrix.append(counts)
		total_num += sum(counts)
	summ = 0.0
	for i in range(len(confusion_matrix[0])):
		summ += confusion_matrix[i][i]
	for row in confusion_matrix:
		print('\t'.join(map(str,row)))
	accuracy = summ/total_num
	return total_num, accuracy, confusion_matrix

def parameters(file):
	max_depth = 8
	if 'balance.scale' in file:
		max_depth = 3
	if 'nursery' in file:
		max_depth = 7
	if 'led' in file:
		max_depth = 7
	if 'synthetic.social' in file:
		max_depth = 8
	return max_depth



train_file = sys.argv[1]
test_file = sys.argv[2]
train_data = read_data(train_file)
test_data = read_data(test_file)
max_depth = parameters(train_file)
classes = sorted(list(set([row[-1] for row in train_data]+[row[-1] for row in test_data])))
actual_labels = [row[-1] for row in test_data]
predict_labels = decision_tree(train_data, test_data, max_depth, 1)
conf_matrix(actual_labels, predict_labels, classes)



