import numpy as np
import math
import sys

dictionary = []
documents = open(sys.argv[1], "r")
documents = documents.readlines()
id = 1

#Finds all unique words and puts it into a list
for document in documents:
    for word in document.split():
        if word not in dictionary:
            dictionary.append(word)
print("Words in dictionary: " + str(len(dictionary)))

#Identifies which words appears in which documents
inverted_index = {word : [] for word in dictionary}
for document in documents:
    for word in document.split():
        if id not in inverted_index[word]:
            inverted_index[word].append(id)
    id += 1

#Creates vectors for each document
id = 1
document_vectors = {id : np.zeros(len(dictionary), dtype=int) for id in range(1,len(documents)+1)}
for document in documents:
    for word in document.split():
        document_vectors[id][dictionary.index(word)] += 1
    id += 1

#Identifies which documents contain the words in the query and creates search vectors
queries = open(sys.argv[2], "r")
for query in queries.read().splitlines():
    list_of_document_IDs = ""
    search_vector = np.zeros(len(dictionary), dtype=int)
    print("Query: " + query)
    for document in documents:
        for word in query.split():
            if word not in document.split():
                break
        else:
            list_of_document_IDs += str(documents.index(document) + 1) + " "
    for word in query.split():
        search_vector[dictionary.index(word)] += 1
    print("Relevant documents: " + list_of_document_IDs)
    result = [[i*0, i*0] for i in range(len(list_of_document_IDs.split()))]
    #Calculates the angle between the document and search vector and prints out the angle and id
    index = 0
    for id in list_of_document_IDs.split():
        dot_product = np.dot(document_vectors[int(id)], search_vector)
        norm_product = np.linalg.norm(document_vectors[int(id)]) * np.linalg.norm(search_vector)
        radians = math.acos(dot_product/norm_product)
        angle = math.degrees(radians)
        result[index] = id, angle
        index += 1
    for id, angle in sorted(result, key=lambda x: x[1]):
        print(id + " {:.2f}".format(angle))
    
