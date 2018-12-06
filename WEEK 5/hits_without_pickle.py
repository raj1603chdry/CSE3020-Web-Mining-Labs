# Implementing HITS Algorithm

import numpy as np

# Function to calculate the authority and hub score of the nodes
def authority_hub_score(outlinks):
	"""
	Function to calculate the authority and hub score of all the nodes in the 
	network.
	
	Parameters:
	------------
	outlinks: (n, n) int matrix where 1 represents the presence of a link and 0
		represents absence of a link
	
	Returns:
	---------
	hub_score: nd-array, containing the hub scores of the nodes
	
	authority_score: nd-array, containing the authority scores of the nodes
	"""
	
	# size of the matrix
	size = outlinks.shape[0]
	
	# Initializing the lists
	hub_scores = [1.0 for i in range(size)]
	authority_scores = [1.0 for i in range(size)]
	
	# Printing initial Hub scores
	print(hub_scores)
	
	for _ in range(100):
		# Calculating the authority scores of the nodes
		for j in range(size):
			temp_auth = 0.0
			for i in range(size):
				if outlinks[i][j] == 1:
					temp_auth += hub_scores[i]
			authority_scores[j] = temp_auth
			
		# Normalizing the authority scores
		auth_sum = sum(authority_scores)
		# print(auth_sum)
		for i in range(len(authority_scores)):
			authority_scores[i] /= auth_sum
		
		# Calculating the hub scores of the nodes
		for i in range(size):
			temp_hub = 0.0
			for j in range(size):
				if outlinks[i][j] == 1:
					temp_hub += authority_scores[j]
			hub_scores[i] = temp_hub
			
		# Normalizing the hub scores
		hub_sum = sum(hub_scores)
		# print(hub_sum)
		for i in range(len(hub_scores)):
			hub_scores[i] /= hub_sum
	
	return authority_scores, hub_scores
					

n = int(input('Enter the size of the matrix:\t'))
outlinks = []
for i in range(n*n):
	temp = int(input('Enter the element:\t'))
	outlinks.append(temp)
outlinks = np.reshape(outlinks, (n, n))
authority_scores, hub_scores = authority_hub_score(outlinks)
print("Authority Scores:")
for i in (authority_scores):
	print(round(i, 4))
print("Hub Scores:")
for i in (hub_scores):
	print(round(i, 4))
