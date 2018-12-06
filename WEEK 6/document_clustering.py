# Implementing Vector Space Model and performing Hierarchical Clustering of the documents.

# Importing the libraries
import string
import pandas as pd
import math
import matplotlib.pyplot as plt

class document_clustering(object):
    """Implementing the document clustering class.
    It creates the vector space model of the passed documents and then
    creates a Hierarchical Cluster to organize them.
    
    Parameters:
    -------------
    file_dict: dictionary
        Contains the path of the different files to be read.
        Format: {file_index: path}
    word_list: list
        Contains the list of words using which the vector space model is to be
        created.
        
    Attributes:
    -----------
    listing_dict_: dictionary
        Contains the frequency of the words in each document as file_index as key
        and frequency list as value.
    distance_matrix_ : pandas-dataframe
        Contains the sqaure matrix of documents containing the pairwise distance between them
    labels_: list
        Contains the labels for document names
    """
    
    def __init__(self, file_dict, word_list):
        self.file_dict = file_dict
        self.word_list = word_list
        
    def tokenize_document(self, document):
        """Returns a list of words contained in the document after converting 
        it to lowercase and striping punctuation marks"""
        terms = document.lower().split()
        return [term.strip(string.punctuation) for term in terms]
    
    def create_word_listing(self):
        """Function to create the word listing of the objects"""
        
        # Dictionary to hold the frequency of words in word_list with file_index as key
        self.listing_dict_ = {}
        
        for id in self.file_dict:
            temp_word_list = []
            f = open(self.file_dict[id], 'r')
            document = f.read()
            terms = self.tokenize_document(document)
            for term in self.word_list:
                temp_word_list.append(terms.count(term.lower()))
            self.listing_dict_[id] = temp_word_list
        
        print('Word listing of each document')
        for id in self.listing_dict_:
            print('%d:  %s' % (id, self.listing_dict_[id]))
            
    def create_document_matrix(self):
        """Function to create the document distance matrix"""
        self.labels_ = ['doc%d' % (id) for id in self.file_dict]
        main_list = []
        for id1 in self.file_dict:
            temp_list = []
            for id2 in self.file_dict:
                dist = 0
                for term1, term2 in zip(self.listing_dict_[id1], self.listing_dict_[id2]):
                    dist += (term1-term2)**2
                temp_list.append(round(math.sqrt(dist), 4))
            main_list.append(temp_list)
            
        self.distance_matrix_ = pd.DataFrame(main_list, index = self.labels_, columns = self.labels_)
        print('\nDistance Matrix')
        print(self.distance_matrix_)
    
    def cluster(self):
        """Create the vector space model from the documents. Perform Hierarchical
        Clustering"""
        from scipy.cluster.hierarchy import linkage
        row_cluster = linkage(self.distance_matrix_.values,
                              method = 'complete',
                              metric = 'euclidean')
        from scipy.cluster.hierarchy import dendrogram
        dn = dendrogram(row_cluster, labels = self.labels_)
        plt.ylabel('Euclidean Distance')
        plt.xticks(rotation = 90)
        plt.savefig('dendrogram1.png', dpi = 300)
        plt.show()
                
    
# Dictionary containing the file_index and path
file_dict = {1: 'documents/doc1.txt',
             2: 'documents/doc2.txt',
             3: 'documents/doc3.txt',
             4: 'documents/doc4.txt',
             5: 'documents/doc5.txt',
             6: 'documents/doc6.txt',
             7: 'documents/doc7.txt',
             8: 'documents/doc8.txt',
             9: 'documents/doc9.txt'}
# List containing the words using which the vector space model is to be created
word_list = ['Automotive', 'Car', 'motorcycles', 'self-drive', 'IoT', 'hire' ,'Dhoni']

# Creating class instance and calling appropriate functions
document_cluster = document_clustering(file_dict = file_dict, word_list = word_list)
document_cluster.create_word_listing()
document_cluster.create_document_matrix()
document_cluster.cluster()