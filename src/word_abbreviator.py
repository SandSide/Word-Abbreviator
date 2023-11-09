import re

pattern = r'\W'

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

def cleanup_abbreviations(abbreviationLists):
    
    cleanedAbbreviationLists = []
    
    for abbreviations in abbreviationLists:
        
        cleanedAbbreviations = set()
        
        # Remove abbreviations with empty spaces
        # Removes duplicates since we add to a set
        for abbr in abbreviations:
            if ' ' not in abbr:
                cleanedAbbreviations.add(abbr)
                
        cleanedAbbreviationLists.append(list(cleanedAbbreviations))
        
    return cleanedAbbreviationLists

def score_abbreviations(abbreviationLists):
    v = 1
    
words = load_file('test')
splitWords = split_words(words)
abbreviations = find_abbreviations(splitWords)
abbreviations = cleanup_abbreviations(abbreviations)
# print(abbreviations)
for x in abbreviations:
    print(x)
