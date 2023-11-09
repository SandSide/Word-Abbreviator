import re

charScore = {
    'A': 25,
    'B': 8,
    'C': 8,
    'D': 9,
    'E': 35,
    'F': 7,
    'G': 9,
    'H': 7,
    'I': 25,
    'J': 3,
    'K': 6,
    'L': 15,
    'M': 8,
    'N': 15,
    'O': 20,
    'P': 8,
    'Q': 1,
    'R': 15,
    'S': 15,
    'T': 15,
    'U': 20,
    'V': 7,
    'W': 7,
    'X': 3,
    'Y': 7,
    'Z': 1
}


def load_file(filename):
### Load file lines into a list ###

    wordList = []
    infile = open(filename + '.txt', 'r')

    for line in infile:
        wordList.append(line.strip())
        
    if wordList[-1] == '':
        wordList.pop()

    return wordList
        
def split_words(wordLists):
    
    splitWordList = []
    
    for word in wordLists:

        word = word.upper()

        # Ignore some special characters
        word = re.sub(r"'|`", "", word)
        
        # Split at special characters
        splitWord = re.split(r'\W', word)

        # Remove empty strings in list        
        splitWord = list(filter(None, splitWord))
        
        splitWordList.append(splitWord)
        
    return splitWordList

def find_abbreviations(wordsList):
    
    wordAbbreviationsList = []
    
    for words in wordsList:
        
        charList = []
        
        for word in words:
            
            for c in word:
                charList.append(c)
                
            charList.append(' ')
            
        charList.pop()
        
        abbreviations = []
        
        for i in range(1, len(charList) - 1):
            for j in range(i + 1, len(charList)):
                abbreviations.append(charList[0] + charList[i] + charList[j])

        wordAbbreviationsList.append(abbreviations)
        # print(abbreviations)

    return wordAbbreviationsList

def cleanup_abbreviations(abbrLists):
    
    cleanedAbbrLists = []
    uniqueAbbrList = []
    
    for abbreviations in abbrLists:
        cleanedAbbrLists.append([abbr for abbr in abbreviations if ' ' not in abbr])
        uniqueAbbrList.append([abbr for abbr in abbreviations if ' ' not in abbr])
        
    return remove_duplicates(cleanedAbbrLists, uniqueAbbrList)
        
def remove_duplicates(abbrLists, uniqueAbbrLists):
    
    duplicates = set()
    
    for i,x in enumerate(abbrLists):
        for j,y in enumerate(uniqueAbbrLists):
            
            if i == j:
                continue
            
            # Find all duplicates
            duplicates |= set(x) & set(y)
              
    return [list(set(x) - duplicates) for x in abbrLists]

def score_abbreviations(abbrLists, wordLists):
    
    for abbreviations, words in zip(abbrLists,wordLists):
        
        scores = []
        
        print(words)
        
        for abbr in abbreviations:
            print(determine_abbr_positions(abbr, words))    

            
                
            
def determine_abbr_positions(abbr, words):
                       
    abbrPos = []
    currChar = abbr[1]
    currPos = 0
    currWordIndex = 0
    currWord = words[currWordIndex]
    
    print(abbr)
    
    while(True):
        if currWordIndex == len(words):
            break
        
        currWord = words[currWordIndex]
        
        if currPos == len(currWord):
            currWordIndex += 1
            currPos = 0
            continue  
        elif currChar == currWord[currPos]:
            abbrPos.append((currChar, currPos))
            
            currChar = abbr[2]
            currPos += 1           
        else:
            currPos += 1 
            
    return abbrPos 
                
                        # firstChar = [x[0] for x in words]
            # lastChar = [x[-1] for x in words]
                                            
            # for c in abbr:
                


            #     while(True):
            #         if currPos == len(currWord):
            #             print('End at {}'.format(currPos))
            #             currWordIndex += 1
            #             currWord = words[currWordIndex]
            #             currPos = 0
            #             break
            #         elif c == currWord[currPos]:
            #             print('{} found at {}'.format(c,currPos))
            #             currPos += 1
            #             break
                        
            #         else:
            #             currPos += 1

            #     continue
                
                # while(True):
                #     if currPos == len(currWord):
                #         currWordIndex += 1
                #         currPos = 0
                #         print(currWordIndex)
                #         currWord = words[currWordIndex]
                    
                #     elif c == currWord[currPos]:
                #         print(currPos)
                #         currPos += 1
                #         break
                    
                #     else:
                #         currPos += 1
                    
                    
                
            
            
            
            # Find all positions, posiiton is sequencial
            
            # pos = [[words.find(char) for char in abbr]]
        
            # print(pos)
            
            
            # positions = [(c,i) for ]
            
            
            # print('{}.....{}'.format(firstChar,lastChar))
            
            #score = 0
            
            # for c in abbr:
                
            #     if c == abbr[0]:
            #         continue
                          
            #     if c == firstChar:
            #         score += 0
            #     elif c == lastChar:
            #         score += 20 if c == 'E' else 5
            #     else:
            #         # Commonality score
            #         score += charScore[c]
                    
                    # 2,3,4
                    
                    
                    
                    # Position score
                    
                      

        #     scores.append((abbr, score))
         
        # for x in scores:
        #     print(x)   
    
    
words = load_file('test')
splitWords = split_words(words)
abbrLists = find_abbreviations(splitWords)
abbrLists = cleanup_abbreviations(abbrLists)
scores = score_abbreviations(abbrLists, splitWords) 

# for x in abbreviations:
#     print(x)
