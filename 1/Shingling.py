import os
import string
import binascii
import numpy as np

#Reading the content of the three documents
def readingDocs():
    files = {}
    for filename in os.listdir():
        if os.path.isfile(filename) and filename.endswith(".txt") and not filename in files:
            with open(filename, "r") as file:
                files[filename] = file.read()
    return files


#Splitting the docs in list of words and assigning an integer as the key for the document
def splitting(files):
    docs = {}
    i = 0
    for key,value in files.items():
        lowerVal = value.lower().replace('\n', '')
        readyString = lowerVal.translate(str.maketrans('', '', string.punctuation)) # To remove the punctuation from the string
        split = readyString.split(" ")
        i = i + 1
        docs[i] = split
    return docs



#Creating shingles from the documents of length k, hashing them to integers and return a dictionary of hashed shingles
def shingling(k, documents):

    docsAsShingles = {}
    docsAsHashedShingles = {}

    for i in range(1, len(documents) + 1):

        words = documents[i]

        shinglesInDocWords = set()

        shinglesInDocInts = set()

        shingle = []

        for j in range(len(words) - k + 1):

            shingle = words[j:j + k]

            shingle = ' '.join(shingle)

            crc = binascii.crc32(shingle.encode()) & 0xffffffff

            if shingle not in shinglesInDocWords:
                shinglesInDocWords.add(shingle)

            if crc not in shinglesInDocInts:
                shinglesInDocInts.add(crc)

        docsAsShingles[i] = shinglesInDocWords
        docsAsHashedShingles[i] = shinglesInDocInts

    return docsAsHashedShingles

#Three arguments, two sets of shingles and the universal set, Computes the jaccard_similarity of the two sets
def CompareSets(shingle1, shingle2, universal_set):
    count = 0

    for i in shingle1:
        if i in shingle2:
            count += 1

    jaccard_similarity = count / len(universal_set)
    return jaccard_similarity

docs = splitting(readingDocs())

#k is the length of the shingles
k = 0
while True:
    k = int(input("Please enter the size of shingles: "))
    if(k <= 0):
        print("Please enter a positive number")
        continue
    else:
        break

shingles = shingling(k, docs)

#Construct universal set that has all the shingles
universal_set = set()
for key, value in shingles.items():
    universal_set.update(value)


jaccard_similarity = CompareSets(shingles[1], shingles[2], universal_set)
print(jaccard_similarity)

# for i, j in shingles.items():
#     print("Document " + str(i))
#     print(j)

#EXPERIMENTATION WITH CHARACTERISTIC MATRIX
# row1 = []
# for i in universal_set:
#     if i in shingles[1]:
#         row1.append(1)
#     else:
#         row1.append(0)
#
# row2 = []
# for i in universal_set:
#     if i in shingles[2]:
#         row2.append(1)
#     else:
#         row2.append(0)
#
# row3 = []
# for i in universal_set:
#     if i in shingles[3]:
#         row3.append(1)
#     else:
#         row3.append(0)
#
# charMatrix = np.column_stack((row1, row2, row3))
