import sys

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
			for key in sorted(dic.keys()):
				values.append(dic[key])
			data.append([int(line[0])] + values)
	return data

train_file = '/Users/lingsonggao/Documents/UI courses/CS412 Data Mining/HW/assignment_4/Dataset/synthetic.social/synthetic.social.train'
test_file = '/Users/lingsonggao/Documents/UI courses/CS412 Data Mining/HW/assignment_4/Dataset/synthetic.social/synthetic.social.test'
train_data = read_data(train_file)
test_data = read_data(test_file)


def divide_groups(index,dataset):
	dic = {}
	for row in dataset:
		if(dic.get(row[index]) == None):
			dic[row[index]] = []
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
			pi = [row[0] for row in group].count(val) / Di
			summ += pi * pi
		gini += (1.0 - summ) * (Di / D)
	return gini


def best_attr(dataset):
	classes = list(set(row[0] for row in dataset))
	best_gini, best_groups = 1000, None
	best_idx, best_vals = None, None
	attributes = [i+1 for i in range(len(dataset[0])-1)]
	remove_attr = []
	for idx in attributes:
		values, groups = divide_groups(idx, dataset)
		if len(groups) == 1:
			remove_attr.append(idx)
			continue
		gini = gini_index(groups, classes)
		if gini < best_gini:
			best_idx, best_gini, best_vals, best_groups = idx, gini, values, groups
	child_attr = list(attributes)
	if not remove_attr:
		for i in remove_attr:
			child_attr.remove(i)
	child_attr.remove(best_idx)
	return {'index': best_idx, 'values': best_vals, 'groups': best_groups, 'child_attr' : child_attr}



def leaf(group):
	class_val = [row[0] for row in group]
	classes = set(class_val)
	num = 0
	for val in classes:
		if class_val.count(val)>num :
			clas, num = val, class_val.count(val)
	return clas


def children(node, max_depth, min_num, depth):
	node['child'] = []
	if depth >= max_depth-1 or node['child_attr'] == None:
		for group in node['groups']:
			node['child'].append(leaf(group))
		return
	for idx, group in enumerate(node['groups']):
		classes = set([row[0] for row in group])
		if len(group) <= min_num or len(classes)==1:
			node['child'].append(leaf(group))
		else:
			node['child'].append(best_attr(group))
			children(node['child'][idx], max_depth, min_num, depth+1)
	return


def build_tree(dataset, max_depth, min_num):
	root = best_attr(dataset)
	children(root, max_depth, min_num, 0)
	return root


def predict(node, row):
	index = 0
	for idx,value in enumerate(node['values']):
		if value == row[node['index']]:
			index = idx; break;
	if isinstance(node['child'][index], dict):
		return predict(node['child'][index], row)
	else:
		return node['child'][index]

def decision_tree(train, test, max_depth, min_num):
	tree = build_tree(train, max_depth, min_num)
	predictions = [predict(tree, row) for row in test]
	return predictions

actual_labels = [row[0] for row in test_data]
predict_labels = decision_tree(train_data, test_data, 8, 3)
print(actual_labels[0:10])
print(predict_labels[0:10])

def conf_matrix(actual_labels, predict_labels):
	confusion_matrix = []
	classes = sorted(list(set(actual_labels)))
	idx_dict = {}
	for idx,value in enumerate(actual_labels):
		if(idx_dict.get(value) == None):
			idx_dict[value] = []
		idx_dict[value].append(idx)
	total_num = 0.0
	for clas in classes:
		index = idx_dict[clas]
		predicts = [predict_labels[i] for i in index]
		counts = [predicts.count(cl) for cl in classes]
		confusion_matrix.append(counts)
		total_num += sum(counts)
	summ = 0.0
	for i in range(len(confusion_matrix[0])):
		summ += confusion_matrix[i][i]
	for row in confusion_matrix:
		print('\t'.join(map(str,row)))
	accuracy = summ/total_num
	return accuracy

accuracy = conf_matrix(actual_labels, predict_labels)
print(accuracy)



