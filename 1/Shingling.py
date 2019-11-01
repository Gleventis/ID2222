import os
import binascii

#reading the content of the three documents
def readingDocs():
    files = {}
    for filename in os.listdir():
        if os.path.isfile(filename) and filename.endswith(".txt") and not filename in files:
            with open(filename, "r") as file:
                files[filename] = file.read()
    return files


#splitting the docs in list of words and assigning an integer as the key for the document
def splitting(files):
    docs = {}
    i = 0
    for key,value in files.items():
        lowerVal = value.lower().replace('\n', '')
        split = lowerVal.split(" ")
        i = i + 1
        docs[i] = split
    return docs



#Creating shingles from the documents of length k
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

files = readingDocs()

docs = splitting(files)

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

for i, j in shingles.items():
    print(j)
    print(i)


# TODO: Create an ordered list of hashes
