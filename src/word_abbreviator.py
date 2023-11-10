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

    word_list = []
    in_file = open(filename + '.txt', 'r')

    for line in in_file:
        word_list.append(line.strip())
        
    if word_list[-1] == '':
        word_list.pop()

    return word_list
        
def split_words(word_list):
    
    split_words = []
    
    for word in word_list:

        word = word.upper()

        # Ignore some special characters
        word = re.sub(r"'|`", "", word)
        
        # Split at special characters
        split_word = re.split(r'\W', word)

        # Remove empty strings in list        
        split_word = list(filter(None, split_word))
        
        split_words.append(split_word)
        
    return split_words

def find_abbreviations(split_words):
    
    abbr_lists = []
    abbr_pos_type_lists = []
    
    for words in split_words:
        
        chars = '#'.join(words)
        abbr_list = []
        pos_type_list = []
        
        # Find all 3 letter abbreviations
        for i in range(1, len(chars) - 1):
            for j in range(i + 1, len(chars)):
                
                # Create abbr
                abbr = chars[0] + chars[i] + chars[j]
                
                # Ignore abbr
                if '#' in abbr:
                    continue
                
                abbr_list.append(abbr)
                
                # Determine what type of char each char is
                pos = (0, i, j)
                pos_types = determine_abbr_pos_type(pos, chars)
                pos_type_list.append(pos_types)
                
        abbr_lists.append(abbr_list)
        abbr_pos_type_lists.append(pos_type_list)
        
    return abbr_lists, abbr_pos_type_lists
        
def determine_abbr_pos_type(pos_list, chars):
     
    pos_types = []
    
    for x in pos_list[1:3]:
        
        i = int(x)
        
        if i - 1 < 0 or chars[i - 1] == '#':
            pos_types.append('first')
        elif i + 1 >= len(chars) or chars[i + 1] == '#':
            pos_types.append('last')
        elif i - 2 < 0 or chars[i - 2] == '#':
            pos_types.append('second')
        elif i - 3 < 0 or chars[i - 3] == '#':
            pos_types.append('third')
        else:
            pos_types.append('middle')

    return pos_types
        
def remove_duplicates(abbr_lists, pos_lists):
    
    duplicates = set()
    new_abbr_lists = []
    new_pos_lists = []

    for i,x in enumerate(abbr_lists):
        for j,y in enumerate(abbr_lists):
            
            if i == j:
                continue
            
            # Find all duplicates
            duplicates |= set(x) & set(y)
            
    for i, (abbr_list, pos_list) in enumerate(zip(abbr_lists, pos_lists)):
        
        duplicate_indexes = [i for i,v in enumerate(abbr_list) if v in duplicates]
        temp_abbr_list = [v for i,v in enumerate(abbr_list) if i not in duplicate_indexes]
        temp_pos_list = [v for i,v in enumerate(pos_list) if i not in duplicate_indexes]
        
        print(temp_abbr_list)
        
        new_abbr_lists.append(temp_abbr_list)
        new_pos_lists.append(temp_pos_list)
        
    return new_abbr_lists, new_pos_lists

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
split_words_lists = split_words(words)

abbr_lists, abbr_pos__type_lists = find_abbreviations(split_words_lists)
unique_abbr_lists, unique_pos_lists = remove_duplicates(abbr_lists, abbr_pos__type_lists)

temp = unique_abbr_lists
temp_2 = unique_pos_lists

# pos_type_lists = determine_abbr_pos_type(abbr_pos_lists, split_words_lists)

# print(abbr_lists)


# print(len())

# for x in abbr_pos__type_lists:
#     print(x)
    
# for x,y in zip(abbr_lists, abbr_pos__type_lists):
#     print(len(x) == len(y))

# abbrLists = cleanup_abbreviations(abbrLists)
# scores = score_abbreviations(abbrLists, splitWords) 

# print(abbrLists)

# for x in abbrLists:
#     print(x)

# for x in abbreviations:
#     print(x)cd 
