# Implementing Page Rank Algorithm
import numpy as np

# Function to calculate the PageRank 
def calculate_PageRank(outlinks):
	"""
	A function that returns the PageRank of the various nodes
	
	Parameters:
	-----------
	outlinks: (nxn) int matrix that contains the outlinks for each node
	
	Returns:
	--------
	page_ranks: list, containing the PageRank for each node
	"""
	
	# Damping factor
	d = 0.85
	
	# size of the matrix
	size = outlinks.shape[0]
	
	# list to hold page ranks
	page_ranks = [1 for i in range(size)]
	
	# Calculating the out degree of each node and storing in a list
	out_degrees = []
	for i in range(size):
		sums = 0
		for j in range(size):
			sums += outlinks[i][j]
		out_degrees.append(sums)
		
	#print(out_degrees)
	
	print('Initial page ranks:')
	print(page_ranks)
	
	for _ in range(100):
		for j in range(size):
			temp = 0
			for i in range(size):
				if outlinks[i][j] == 1:
					temp += page_ranks[i] / out_degrees[i]
			temp *= d
			temp += (1-d)
			page_ranks[j] = round(temp, 4)
		
	return page_ranks
			
outlinks = [0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0]
outlinks = np.reshape(outlinks, (5, 5))
page_ranks = calculate_PageRank(outlinks)	
print()
print('The converged page rank is:')
print(page_ranks)
print()
sums = 0
for i in page_ranks:
	sums += i
print('The sum of page ranks is: ', round(sums, 4))
