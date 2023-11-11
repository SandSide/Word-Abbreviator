import re
import os
from pathlib import Path

script_directory = os.path.dirname(os.path.abspath(__file__))

char_value = {
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

    path = os.path.join(script_directory, filename)

    word_list = []
    in_file = open(path + '.txt', 'r')

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

def find_all_abbreviations(split_words):
    
    abbr_lists = []
    abbr_pos_type_lists = []
    
    for words in split_words:
        
        abbr_list, pos_type_list = find_abbreviations(words)
                
        abbr_lists.append(abbr_list)
        abbr_pos_type_lists.append(pos_type_list)
        
    return abbr_lists, abbr_pos_type_lists
    
def find_abbreviations(words):
    
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
    
    return abbr_list, pos_type_list
    
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
        
        new_abbr_lists.append(temp_abbr_list)
        new_pos_lists.append(temp_pos_list)
        
    return new_abbr_lists, new_pos_lists

def find_all_min_scores(abbr_lists, pos_type_lists):
    
    score_lists = []
    
    for abbr_list, pos_type_list in zip(abbr_lists, pos_type_lists):
        
        scores = []
        
        for abbr, pos_types in zip(abbr_list, pos_type_list):

            abbr_score = score_abbr(abbr, pos_types)  
                    
            scores.append((abbr, abbr_score, pos_types))
            
        min_score = min(scores, key = lambda x: x[1])
         
        score_lists.append(min_score)

    return score_lists
                    
def score_abbr(abbr, pos_types):
    
    score = 0

    for char, pos_type in zip (abbr[1:3], pos_types):
        
        char_score = 0
                
        if pos_type == 'first':
            char_score += 0
        elif pos_type == 'last':
            char_score += 20 if char == 'E' else 5
        else:
            char_score += score_position(pos_type)
            char_score += char_value[char]
    
        score += char_score   
        
    return score  
 
def score_position(pos_type):
    
    if pos_type == 'second':
        return 1
    elif pos_type == 'third':
        return 2
    elif pos_type == 'middle':
        return 3
    
    return 0

def save_scores(filename, scores, words):
    
    filename = 'Jakubek_' + filename + '_abbrevs.txt'
    path = os.path.join(script_directory, filename)
    
    with open(path + '.txt', 'w') as out_file:
    
        for score, word in zip(scores, words):    
            out_file.write('{}\n{}\n'.format(word, score[0]))

def handle_user_input():
    """Waits to user input for a filename, checks to see if that file exists. 
    Returns filename if it exits, otherwise to ask the user to re-enter name

    Returns:
        string: name of a existing file
    """
    user_input = input("Enter input filename: ")
    
    path = os.path.join(script_directory, user_input) + ".txt"
    
    # While the file dose not exist
    while not os.path.exists(path):
        
        # Ask for re-input
        print('File {} dose not exist'.format(user_input))
        user_input = input("Enter input filename: ")
        path = os.path.join(script_directory, user_input) + ".txt"
    
    return user_input
    
filename = handle_user_input()

words = load_file(filename)
split_words_lists = split_words(words)

abbr_lists, abbr_pos__type_lists = find_all_abbreviations(split_words_lists)
unique_abbr_lists, unique_pos_lists = remove_duplicates(abbr_lists, abbr_pos__type_lists)

min_scores = find_all_min_scores(unique_abbr_lists, unique_pos_lists)
save_scores(filename, min_scores, words)