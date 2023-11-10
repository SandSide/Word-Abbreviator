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
    
    minScores = []
    
    for abbreviations, words in zip(abbrLists, wordLists):
        
        scores = []  
              
        for abbr in abbreviations:
            
            abbrPos = determine_abbr_positions(abbr, words)
            
            score = 0
            
            for char, pos in zip(abbr[1:3], abbrPos):
                
                # print('{} {}'.format(char, pos))

                if pos[0] == 0: # First letter of a word
                    score += 0
                elif pos[1] == True: # Last Letter
                    score += 20 if char == 'E' else 5
                else:
                    
                    # Position Score
                    score += score_position(pos[0])
                    
                    # Commonality score
                    score += charScore[char]
                    
            scores.append((abbr, score))
            
        minScore = min(scores, key=lambda x: x[1])
        
        minScores.append(minScore) 
        
    return minScores
 
def score_position(pos):
    
    if pos == 1:
        return 1
    elif pos == 2:
        return 2
    elif pos >= 3:
        return 3
    
    return 0
    
def determine_abbr_positions(abbr, words):
                       
    abbrPos = []
    currChar = abbr[1]
    currPos = 0
    currWordIndex = 0
    currWord = words[currWordIndex]
    
    while(True):
        if currWordIndex == len(words):
            break
        
        currWord = words[currWordIndex]
        
        if currPos == len(currWord):
            currWordIndex += 1
            currPos = 0
            continue  
        elif currChar == currWord[currPos]:
            
            isLast = currPos + 1 == len(words[currWordIndex])
            abbrPos.append((currPos, isLast))
            
            currChar = abbr[2]
            currPos += 1           
        else:
            currPos += 1 
            
    return abbrPos 
    
words = load_file('test')
splitWords = split_words(words)
abbrLists = find_abbreviations(splitWords)
abbrLists = cleanup_abbreviations(abbrLists)
scores = score_abbreviations(abbrLists, splitWords) 

print(scores)

# for x in abbreviations:
#     print(x)cd 
