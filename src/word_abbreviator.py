import re

pattern = r'\W'

def load_file(filename):
### Load file lines into a dictonary ###

    wordList = []
    infile = open(filename + '.txt', 'r')

    for line in infile:
        wordList.append(line.strip())

    return wordList
        
def split_words(dict):
    
    splitWordList = []
    
    for word in dict:

        # 
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

for x in splitWordsList:
    print(x)
