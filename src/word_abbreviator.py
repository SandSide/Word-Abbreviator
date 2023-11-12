import re
import os

script_directory = os.path.dirname(os.path.abspath(__file__))

char_value = {}

def load_char_values():
    """Load char value dictionary from a file.
    """

    path = os.path.join(script_directory, 'values')
    
    with open(path + '.txt', 'r') as in_file:
        for line in in_file:
            
            # Get key value pairs
            char, value = line.split()
            
            char_value[char] = int(value)

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

def find_all_min_score_abbr(abbr_lists, pos_type_lists):
    """Finds all abbreviations which have min score for each abbr list.

    Args:
        abbr_lists (list of lists): A list of abbr lists.
        pos_type_lists (list of lists): A list of position type lists corresponding to each abbr list.

    Returns:
        list of lists: A list containing abbreviations with lowest score for ach abbr list.
    """
    
    min_score_abbrs_list = []
    
    # For each list
    for abbr_list, pos_type_list in zip(abbr_lists, pos_type_lists):
        
        # Ignore empty abbr list
        if len(abbr_list) == 0:
            min_score_abbrs_list.append([])
            continue
        
        abbr_scores = []
        
        # Find score for each abbr in list
        for abbr, pos_types in zip(abbr_list, pos_type_list):

            # Score abbr
            abbr_score = score_abbr(abbr, pos_types)  
                    
            abbr_scores.append((abbr, abbr_score))
            
        # Find lowest score
        min_score = min(abbr_scores, key = lambda x: x[1])

        # Find all abbreviations containing min score
        min_scores = [abbr_score[0] for abbr_score in abbr_scores if abbr_score[1] == min_score[1]]
        
        min_score_abbrs_list.append(min_scores)

    return min_score_abbrs_list
                    
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

def save_abbr(filename, abbr_lists, words):
    """Save words and their abbreviations to a file.

    Args:
        filename (string): filename used as input file.
        abbr_lists (list of lists): A list containing lists of abbreviations.
        words (string list): a list of words which each abbr is an abbreviation of.
    """
    
    filename = 'jakubek_' + filename + '_abbrevs.txt'
    path = os.path.join(script_directory, filename)
    
    with open(path + '.txt', 'w') as out_file:
    
        # Save word and their abbreviations
        for abbr_list, word in zip(abbr_lists, words):    
            
            abbrs = " ".join(abbr_list)
            out_file.write('{}\n{}\n'.format(word, abbrs))
    
def main():
    
    load_char_values()
    
    filename = handle_user_input()

    words = load_file(filename)
    split_words_lists = split_words(words)

    abbr_lists, abbr_pos__type_lists = find_all_abbreviations(split_words_lists)
    unique_abbr_lists, unique_pos_lists = remove_duplicates(abbr_lists, abbr_pos__type_lists)

    min_score_abbr_lists = find_all_min_score_abbr(unique_abbr_lists, unique_pos_lists)
    
    # min_score_abbr_lists.append([''])
    # words.append('empty abbr list')
    
    # min_score_abbr_lists.append(['CLD', 'CLO', 'CPO'])
    # words.append('test')
    
    save_abbr(filename, min_score_abbr_lists, words)
    

if __name__ == "__main__":
    main()