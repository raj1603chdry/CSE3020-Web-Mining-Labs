# Implementing sessionization on log entry dataset

# Importing the libraries
from csv import reader
from datetime import datetime

class Sessionize(object):
	"""
	Class that sessionozes the log entries per user.
	The users are identified by using their IP and user agent.
	Then timestamp is used to sessionize the logs based on the H1, H2 and
	H-REF rule that uses the value of delta i.e. the maximum time to be
	considered in a session and theta i.e. the minimum time to be spent
	per page.

	Parameters:
	-----------
	filename: string
		The name of the file that contains the server log entries.

	delta: int
		The maximum time in seconds that can be considered in the same
		session.

	Attributes:
	-----------
	dataset: 2d array
		Contains the entries of the server log file.

	separate: dict
		Contains the unique users using (IP, User-agent) as key and their 
		server log entries as value in a list.

	sessions: dict
		Contains the different sessions per user in which the user is the key
		and the differnet sessions are values.

	Returns:
	--------
	"""

	def __init__(self, filename, delta):
		"""Function to initialize the different parameters of the object."""
		self.delta = delta
		csvfile = open(filename, 'r')
		self.dataset_ = list(reader(csvfile))
		self.updateOrderingOfEntries()

	def separateUsers(self):
		"""Function to separate the server log entries based on the user 
		i.e. on the basis of the IP and user-agent."""
		self.separate_ = {}
		for row in self.dataset_:
			if row[0] not in self.separate_:
				self.separate_[row[0]] = []
			self.separate_[row[0]].append(row[1:])
		# Updating the timestamp field of the entries.
		self.updateTimestamp()

	def updateTimestamp(self):
		"""Function that updates the timestamp field in a format that 
		makes its processing by datetime module easy."""
		for i in self.separate_:
			for j in self.separate_[i]:
				# Trimming unnecessary characters from the entries
				date_time = j[0][1:-6]
				j[0] = date_time

	# def updateOrderingOfEntries(self):
	# 	"""Function to sort the entries in ascending order based on the 
	# 	timestamp using Bubble Sort."""

	# 	for i in range(len(self.dataset_) - 1):
	# 		for j in range(i + 1, len(self.dataset_)):
	# 			t1 = datetime.strptime(self.dataset_[i][1][1:-6], 
	# 				 "%d/%b/%Y:%H:%M:%S")
	# 			t2 = datetime.strptime(self.dataset_[j][1][1:-6], 
	# 				 "%d/%b/%Y:%H:%M:%S")
	# 			if t1 > t2:
	# 				self.dataset_[i], self.dataset_[j] = self.dataset_[j], self.dataset_[i]

	def updateOrderingOfEntries(self):
		"""Function to sort the entries in ascending order based on the 
		timestamp using Selection Sort."""

		for i in range(len(self.dataset_)):
			# Find the minimum element in the remaining unsorted array.
			min_idx = i
			t1 = datetime.strptime(self.dataset_[i][1][1:-6], 
					 "%d/%b/%Y:%H:%M:%S")
			for j in range(i+1, len(self.dataset_)):
				t2 = datetime.strptime(self.dataset_[j][1][1:-6], 
					 "%d/%b/%Y:%H:%M:%S")
				if t1 > t2:
					min_idx = j

			# Swapping the minimum element at ith index
			self.dataset_[i], self.dataset_[min_idx] = self.dataset_[min_idx], self.dataset_[i]
	
	def createSession(self):
		"""Function to create session for each user based on the different
		rules of sessionization."""
		self.sessions_ = {}
		for i in self.separate_:
			if i not in self.sessions_:
				self.sessions_[i] = []
			for j in range(len(self.separate_[i])):
				temp = []
				present = False
				for l in self.sessions_[i]:
					if self.separate_[i][j] in l:
						present = True
				if not present:
					temp.append(self.separate_[i][j])
					for k in range(j + 1, len(self.separate_[i])):
						t1 = datetime.strptime(self.separate_[i][j][0], 
							"%d/%b/%Y:%H:%M:%S")
						t2 = datetime.strptime(self.separate_[i][k][0], 
							"%d/%b/%Y:%H:%M:%S")
						latest = max((t1, t2))
						old = min((t1, t2))
						difference = latest - old
						if(difference.seconds <= self.delta):
							temp.append(self.separate_[i][k])
					self.sessions_[i].append(temp)

	def printSessions(self):
		"""Function to print the sessions per user."""
		session_id = 1
		print('%s' % ('-' * 93))
		print('| {:^20} | {:^20} | {:^20} | {:^20} |'.format("Session Id",
			"IP address", "Start Time", "End Time"))
		print('%s' % ('-' * 93))
		for i in self.sessions_:
			for l in self.sessions_[i]:
				dates = []
				for row in l:
					dates.append(datetime.strptime(row[0], 
							"%d/%b/%Y:%H:%M:%S"))
				print('| {:^20} | {:^20} | {:^20} | {:^20} |'.format(session_id, i, str(min(dates)), str(max(dates))))
				session_id += 1
		print('%s' % ('-' * 93))

## Main code

filename = input('Enter the name of the dataset: ')
delta = int(input('Enter delta value (minutes): '))
# Coverting the delta form minutes to seconds.
delta *= 60
# Creating the Sessionize object and calling appropriate functions.
session_create = Sessionize(filename, delta)
session_create.separateUsers()
session_create.createSession()
session_create.printSessions()
