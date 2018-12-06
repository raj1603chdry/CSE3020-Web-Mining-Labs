# Implementing Naive Bayes Classifier for weighted attributes

from csv import reader

class NaiveBayesClassifier(object):
	"""Class to implement Naive Bayes Classifier for weighted attributes.
	
	Parameters:
	-----------
	dataset_filename: string
		The name of the file containing the records of the dataset
	test_component_filename: string
		The name of the file containing the elements of the test
		component
	Attributes:
	-----------
	dataset_: list
		Contains the records read from the dataset file
	test_component_: list
		Contains the elements read from the test component file
	total_length: int
		The number of records in dataset_
	separate_: dict
		Contains the classes of the dataset as key and list of rows
		belonging to the class as value
	probabilities_: dict
		Contains the classes of the dataset as key and the probability
		as value
	best_probability_: float
		The maximum prosterior probability
	best_class: string
		The class to which the test component belongs
	Returns:
	--------
	"""
	
	def __init__(self, dataset_filename, test_component_filename):
		"""Initializer function
		It takes the dataset_filename and test_componene_filename and
		reads in the contents of the file into respective objects"""
		csvfile = open(dataset_filename, 'r')
		self.dataset_ = list(reader(csvfile))
		csvfile1 = open(test_component_filename, 'r')
		self.test_component_ = list(reader(csvfile1))[0]
		print('\nRecords of the dataset')
		for row in self.dataset_:
			print(row)
		print('')
		print('Test components')
		print(self.test_component_)
		print('')
		self.modifyDataset()

	def modifyDataset(self):
		max, min = -1, 999
		for row in self.dataset_:
			for i in row[:-1]:
				i = int(i)
				if i > max:
					max = i
				if i < min:
					min = i
		avg = (min + max) // 2
		## Modifying the dataset based on the avg value
		for row in self.dataset_:
			for i in range(len(row[-1])):
				value = int(row[i])
				if value < avg:
					row[i] = 'Low'
				else:
					row[i] = 'High'
		print('\nRecords of the modified dataset')
		for row in self.dataset_:
			print(row)
		print('')
		## MOdifying the test component based on the avg value
		for i in range(len(self.test_component_)):
			value = int(self.test_component_[i])
			if value < avg:
				self.test_component_[i] = 'Low'
			else:
				self.test_component_[i] = 'High'
		print('Modified Test components')
		print(self.test_component_)
		print('')
		
	def separateDataset(self):
		"""This function splits the dataset based on the number of unique
		classes available and calculates the probability of each class
		in the dataset"""
		self.total_length = len(self.dataset_) + 0.0
		self.separate_ = {}
		self.probabilities_ = {}
		for row in self.dataset_:
			if row[-1] not in self.separate_:
				self.separate_[row[-1]] = []
			self.separate_[row[-1]].append(row[:-1])
		for i in self.separate_:
			self.probabilities_[i] = (len(self.separate_[i]) + 0.0)  / self.total_length
	
	def predict(self):
		"""Function that traverses through the test_components and
		calculates the posterioir probability and finds the class it
		belongs to"""
		self.best_probability = 0
		self.best_class = ''
		for i in self.separate_:
			temp_probability = 1
			for j, item in enumerate(self.test_component_):
				count = 0
				for k in self.separate_[i]:
					if k[j] == item:
						count = count + 1
				prob = count / len(self.separate_[i])
				temp_probability *= prob
			temp_probability *= self.probabilities_[i]
			print('Class %s probability %.4f' % (i, temp_probability))
			if temp_probability > self.best_probability:
				self.best_probability = temp_probability
				self.best_class = i
		print('\nThe given X belongs to %s with a probability of %.4f\n' % (self.best_class, self.best_probability))
				
## Main Code
dataset_file = input('Enter the name of the dataset file:\t')
test_component_file = input('Enter the name of the test component file:\t')
nvc = NaiveBayesClassifier(dataset_file, test_component_file)
nvc.separateDataset()
nvc.predict()
