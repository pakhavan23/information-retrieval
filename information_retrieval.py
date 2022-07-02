from nltk.corpus import stopwords
import random


print("Information Retrieval Methods:\n")

#reading sample text files from storage
#storing each file as a string in "documents" array
#"documents" is what we process in the next algorithms

documents = []
for i in range(3):
    path = f"../input/inputs/sample{i+1}.txt"
    file_line = ""
    file = open(path,"r")
    for line in file.readlines():
        file_line += line.strip()
    documents.append(file_line)
    file.close()
    

#First Algorithm: Tokenizing, removing stop words and puncuations, creating posting lists and inverted index

def inverted_index(docs):
    vocab = []
    postings = {}
    for i,doc in enumerate(docs):

        punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~''';

        words = doc.split(" ")
        words = [word for word in words if word not in stopwords.words()]
        for word in words:
            for character in word:
                if character in punc:
                    word = word.replace(character , "")
            if word != "":
                if word not in vocab:
                    vocab.append(word)
                wordId = vocab.index(word)
                if word not in postings:
                    postings[word] = [i]
                else:
                    if i not in postings[word]:
                        postings[word].append(i)

    return postings
    
print("Inverted Index:")
print(inverted_index(documents))

       


#Second Algorithm: The Merge Algorithm (Intersection between postings)
#The intersect function receives two postings and returns documents that have both of them.

value1 = "film"
value2 = "promotions"

def intersect(first_posting, second_posting):

    count1 = 0
    count2 = 0
    answer = []

    while count1 < len(first_posting) and count2 < len(second_posting):
        if first_posting[count1] == second_posting[count2]:
            answer.append(first_posting[count1])
            count1 +=1
            count2 +=1
        elif first_posting[count1] > second_posting[count2]:
            count2 += 1
        else:
            count1 += 1
    return answer

print("\nIntersection of two posting lists:")
print(f"\nInput values: {value1} , {value2}")
print(intersect(inverted_index(documents)[value1],inverted_index(documents)[value2]))


#Third Algorithm: Posting List with skip pointers
#This algorithm does the same job as the previous one, but uses skip pointers to avoid processing unnecessary comparisons
#between postings.

answer = {}
def intersect_with_skips(p1,p2):
    count1 = 0
    count2 = 0
    answer = []
#     random.seed(101)
    
#     skip = random.random()
    skip = 2

    while count1 < len(p1) and count2 < len(p2):
        if p1[count1] == p2[count2]:
            answer.append(p1[count1])
            count1 +=1
            count2 +=1
        elif p1[count1] < p2[count2]:
            if count1 + skip < len(p1) and p1[count1 + skip] < p2[count2]:
                count1 += skip
            else:
                count1 += 1
        else:
            if count2 + skip < len(p2) and p2[count2 + skip] < p1[count1]:
                count2 += skip
            else:
                count2 += 1

    return answer

print("\nIntersection of two posting lists with skip pointers:")
print(f"\nInput values: {value1} , {value2}")
      
print(intersect_with_skips(inverted_index(documents)[value1],inverted_index(documents)[value2]))

#Fourth Algorithm: Positional Index
#for each term, returns: [docID , frequency, [positions]] 
    
def positional_index(docs) :
    vocab = []
    postings = {}
    for i,doc in enumerate(docs):
        # if using files for Docs this is 
        # where we read the text 

        punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~''';

        words = doc.split(" ")
        for position,word in enumerate(words):
            for character in word:
                if character in punc:
                    word = word.replace(character , "")
            if word != "" and word not in stopwords.words():
                if word not in vocab:
                    vocab.append(word)
                wordId = vocab.index(word)
                if word not in postings:
                    postings[word] = [[i, 1 , [position]]]
                else:
                    for list in postings[word]:
                        if list[0] == i:
                            list[1] +=1
                            list[2].append(position)
                        else:
                            postings[word].append([i, 1 , [position]])
                            break;
    
    return postings

print("\nPositional Indexing:")
print(positional_index(documents))


#Function for finding positional intersection of two terms: recieves the terms and the maximum distance between them
#and returns docID and their positions: [[docID , position of term1 , position of term2]]

def docID(plist):
        return plist[0]

def position(plist):
        return plist[2]
    
def pos_intersect(p1,p2,k):
        answer = []                                                                     # answer <- ()
        len1 = len(p1)
        len2 = len(p2)
        i = j = 0 
        while i != len1 and j != len2:                                                  # while (p1 != nil and p2 != nil)
                if docID(p1[i]) == docID(p2[j]):
                        l = []                                                          # l <- ()
                        pp1 = position(p1[i])                                           # pp1 <- positions(p1)
                        pp2 = position(p2[j])                                           # pp2 <- positions(p2)
    
                        plen1 = len(pp1)
                        plen2 = len(pp2)
                        ii = jj = 0 
                        while ii != plen1:                                              # while (pp1 != nil)
                                while jj != plen2:                                      # while (pp2 != nil)
                                        if abs(pp1[ii] - pp2[jj]) <= k:                 # if (|pos(pp1) - pos(pp2)| <= k)
                                                l.append(pp2[jj])                       # l.add(pos(pp2))
                                        elif pp2[jj] > pp1[ii]:                         # else if (pos(pp2) > pos(pp1))
                                                break    
                                        jj+=1                                           # pp2 <- next(pp2)      
                                                                               
                                while l != [] and abs(l[0] - pp1[ii]) > k :             # while (l != () and |l(0) - pos(pp1)| > k)
                                        l.remove(l[0])                                  # delete(l[0])
                                for ps in l:                                            # for each ps in l
                                        answer.append([ docID(p1[i]), pp1[ii], ps ])    # add answer(docID(p1), pos(pp1), ps)
                                ii+=1                                                   # pp1 <- next(pp1)
                        i+=1                                                            # p1 <- next(p1)
                        j+=1                                                            # p2 <- next(p2)
                elif docID(p1[i]) < docID(p2[j]):                                       # else if (docID(p1) < docID(p2))
                        i+=1                                                            # p1 <- next(p1)                                                        
                else:
                        j+=1                                                            # p2 <- next(p2)
        return answer
    
print("\nPositional Intersection:")
print(f"\nInput values: {value1} , {value2}")
pos_intersect(positional_index(documents)[value1],positional_index(documents)[value2],9)
