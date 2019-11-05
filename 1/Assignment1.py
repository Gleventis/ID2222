import os
import string
import binascii
import random
import numpy as np

#Splitting the data file in smaller txt files, each one containing one review
def CreatingTextFiles(file):
    with open (file) as f:
        counter=1
        for x in f.read().split("\n"):
            with open(str(counter) + '.txt','w') as op:
                op.write(x)
                op.close()
                op=''
                counter+=1
        f.close()

#Reading the content of the txt documents
def ReadingFiles():
    files = {}
    for filename in os.listdir():
        if os.path.isfile(filename) and filename.endswith(".txt") and not filename in files:
            with open(filename, "r") as file:
                files[filename] = file.read()
    return files

#Splitting the docs in list of words and assigning an integer as the key for the document
def Splitting(files):
    docs = {}
    i = 0
    for key,value in files.items():
        lowerVal = value.lower().replace('\n', '')
        readyString = lowerVal.translate(str.maketrans('', '', string.punctuation)) # To remove the punctuation from the string
        split = readyString.split()
        docs[i] = split
        i = i + 1
    return docs

#Creating shingles from the documents of length k, hashing them to integers and return a dictionary of hashed shingles
def Shingling(k, documents):

    docsAsHashedShingles = {}

    for i in range(0, len(documents)):

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

        docsAsHashedShingles[i] = shinglesInDocInts

    return docsAsHashedShingles

#Three arguments, two sets of shingles and the universal set, Computes the jaccard_similarity of the two sets
def CompareSets(shingle1, shingle2, universal_set):
    intersection = shingle1.intersection(shingle2)
    jaccard_similarity = len(intersection) / len(universal_set)
    return jaccard_similarity


data_file = 'interior_toyota_camry_2007.data'
CreatingTextFiles(data_file)

files = ReadingFiles()

docs = Splitting(files)

#k is the length of the shingles
k = 0
while True: # Size of shingles
    k = int(input("Please enter the size of shingles: "))
    if(k <= 0):
        print("Please enter a positive number")
        continue
    else:
        break

shingles = Shingling(k, docs) # dictionary of (docID, shingle)


message1 = "Enter a number between 1 and " + format(len(shingles)) + " for the first document: "
message2 = "Enter a number between 1 and " + format(len(shingles)) + " for the second document: "

var1 = 0
while True:
    var1 = int(input(message1))
    if var1 < 1:
        print("The number has to be positive")
        continue
    else:
        break
while True:
    var2 = int(input(message2))
    if var2 < 1:
        print("The number has to be positive")
        continue
    else:
        break

doc1 = shingles[var1]
doc2 = shingles[var2]
universal_set = doc1.union(doc2)

print(CompareSets(doc1, doc2, universal_set))


maxID = len(shingles)
c = 113

# Picks random number for a and b
def pickingRandomNumbers(k = 100):
    randomNumbers = []

    while k > 0:

        a = random.randint(0, maxID)

        if a in randomNumbers:
            a = random.randint(0, maxID)

        randomNumbers.append(a)

        k -= 1

    return randomNumbers

a = pickingRandomNumbers() # a is a list
b = pickingRandomNumbers() # b is a list

def signatureCreation(shingles, a, b, k, c):

    signatures = {}

    for docID, shingle in shingles.items():
        signature = []

        for i in range(0, 100):

            for s in shingle:
                hash = (a[i] * s + b[i]) % c #Hash function formula given in the course

            signature.append(hash)

        signatures[docID] = signature

    return signatures

print(signatureCreation(shingles, a, b, 100, c)[1])
print("Minimum signature is: " + str(min(signatureCreation(shingles, a, b, 100, c)[1])))
