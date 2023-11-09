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
        
def split_words(wordList):
    
    splitWordList = []
    
    for word in wordList:

        word = word.upper()

        # Ignore some special characters
        word = re.sub(r"'|`", "", word)
        
        # Split at special characters
        splitWord = re.split(r'\W', word)

        # Remove empty strings in list        
        splitWord = list(filter(None, splitWord))
        
        splitWordList.append(splitWord)
        
    return splitWordList

        
words = load_file('test')
splitWordsList = split_words(words)
print(splitWordsList)
# find_abbreviations(splitWordsList)
# for x in splitWordsList:
#     print(x)
