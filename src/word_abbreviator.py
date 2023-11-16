import re
import os

script_directory = os.path.dirname(os.path.abspath(__file__))



def load_char_values():
    """Load char value dictionary from a file."""

    path = os.path.join(script_directory, 'values')
    
    char_value = {}
    
    with open(path + '.txt', 'r') as in_file:
        for line in in_file:
            
            # Get key value pairs
            char, value = line.split()
            
            char_value[char] = int(value)

    return char_value

def handle_user_input():
    """Prompt user for a filename and checks if it exists.
    
    Returns:
        str: Name of a existing file.
    """
    user_input = input("Enter input filename: ")
    
    # While the file dose not exist
    while not check_if_file_exists(user_input):
        
        # Ask for re-input
        print('File {} dose not exist'.format(user_input))
        user_input = input("Enter input filename: ")
    
    return user_input

def check_if_file_exists(filename):
    """Check if file exists in script directory.

    Args:
        filename (str): Name of a file.

    Returns:
        bool: Whether file exists or not.
    """
    
    path = os.path.join(script_directory, filename) + ".txt"
    
    return os.path.exists(path)
    
def load_file(filename):
    """Load a file of strings.

    Args:
        filename (str): Name of a file we read from.

    Returns:
        List[str]: A list of strings in the file.
    """
    # Path to file
    path = os.path.join(script_directory, filename)

    word_list = []
    with open(path + '.txt', 'r') as in_file:
        
        word_list = [line.strip() for line in in_file if line.strip()]

    return word_list

def split_string(word):
    """Split word to make it suitable for abbreviation.

    Args:
        word (str_type_): String to split.

    Returns:
        List[str]: A split string.
    """
    
    word = word.upper()

    # Ignore some special characters
    word = re.sub(r"'|`", "", word)
    
    # Split at special characters
    split_word = re.split(r'\W', word)

    # Remove empty strings in list        
    split_word = list(filter(None, split_word))
    
    return split_word

def split_words(word_list):
    """Split a list of words.

    Args:
        word_list (List[str]): A list of words.

    Returns:
        List[List[str]]: A list of split words.
    """
    
    split_words = []
    
    for word in word_list:

        split_word = split_string(word)
        split_words.append(split_word)
        
    return split_words

def find_all_abbreviations(split_words):
    """Find all 3 letter abbreviations for each word.

    Args:
        split_words (List[List[str]]): A list of split words.

    Returns:
        List[List[abbr]]: A list of abbr for each split word.
        List[List[()]]: A tuple of pos types of each abbr char for each split word.
    """
    
    abbr_lists = []
    pos_type_lists = []
    
    for words in split_words:
        
        # Find all 3 letter abbreviations for word
        # Find position type for each letter in the abbreviation.
        abbr_list, pos_type_list = find_abbreviations(words)
                
        abbr_lists.append(abbr_list)
        pos_type_lists.append(pos_type_list)
        
    return abbr_lists, pos_type_lists
    
def find_abbreviations(words):
    """Find all 3 letter abbreviations for a list of word.

    Args:
        words (List[str]): Words to find abbreviations for.

    Returns:
        List[str]: A list of abbreviations.
        List(()): A list of pos type tuples for each char in abbr.
    """
    
    # Convert words into a single word for easier manipulation
    chars = '#'.join(words)
    abbr_list = []
    pos_type_list = []
    
    # Find all 3 letter abbreviations
    for i in range(1, len(chars) - 1):
        for j in range(i + 1, len(chars)):
            
            # Create abbr
            abbr = chars[0] + chars[i] + chars[j]
            
            # Ignore abbr if invalid
            if '#' in abbr:
                continue
            
            abbr_list.append(abbr)
            
            # Save pos of each char in abbr
            pos = (0, i, j)
            
            # Determine pos type
            pos_types = determine_position_type(pos, chars)
            
            pos_type_list.append(pos_types)
    
    return abbr_list, pos_type_list
    
def determine_position_type(positions, chars):
    """Determine position types for characters in an abbreviation.

    Args:
        positions ((int,int,int)): Positions of abbreviation characters.
        chars (str): A str abbreviation was made from.

    Returns:
        (str,str): Tuple of position types.
    """
     
    pos_types = []
    
    
    for x in positions:
        
        i = int(x)
        
        if i == 0:
            pos_types.append('first')
            continue
        
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
        
def remove_duplicate_abbreviations(scored_abbr_lists):
    """Remove duplicate abbreviations when present in other lists.

    Args:
        scored_abbr_lists (List[List[str]]): A list of abbreviations.

    Returns:
        List[List[(abbr, score)]]: A list of unique abbreviations.
    """
    
    duplicates = set()
    new_abbr_lists = []
    
    abbr_lists = [[y[0] for y in x] for x in scored_abbr_lists]
    
    # Find all duplicate abbreviations
    for i,x in enumerate(abbr_lists):
        for j,y in enumerate(abbr_lists):
            
            if i == j:
                continue
            
            # Add duplicates
            duplicates |= set(x) & set(y)
            
    # Remove duplicate abbreviations from abbr list and their related pos types.
    for i, abbr_list in enumerate(scored_abbr_lists):
        
        # Find indexes of duplicates present in the list
        duplicate_indexes = [i for i,v in enumerate(abbr_list) if v[0] in duplicates]
        
        # Remove duplicates form both lists based on the index
        unique_abbr_list = [v for i,v in enumerate(abbr_list) if i not in duplicate_indexes]

        new_abbr_lists.append(unique_abbr_list)
        
    return new_abbr_lists

def find_all_min_score_abbreviations(scored_abbr_lists):
    """Finds all abbreviations which have min score for each abbreviations list.

    Args:
        scored_abbr_lists (List[List[(str, score]]): A list of abbreviation and their score lists.

    Returns:
        List[List[str]]: A list containing abbreviations with lowest score for each abbreviation list.
    """
    
    min_score_abbr_lists = []
    
    # For each list
    for abbr_list in scored_abbr_lists:
        
        min_scores = find_min_scoring_abbreviations(abbr_list)
        min_score_abbr_lists.append(min_scores)

    return min_score_abbr_lists

def find_min_scoring_abbreviations(scored_abbr_lists):
    """Finds all abbreviations which have the same min score.

    Args:
        scored_abbr_lists ([List[(str, score)]): A list of abbreviation lists.

    Returns:
        List[(str, score)]]: A list of min scoring abbreviation tuples containing abbr and its score.
    """
    
     # Ignore empty abbr list
    if len(scored_abbr_lists) == 0:
        return []

    # Find lowest score
    min_score = min(scored_abbr_lists, key = lambda x: x[1])

    # Find all abbreviations containing min score
    min_scores = [abbr_score[0] for abbr_score in scored_abbr_lists if abbr_score[1] == min_score[1]]
    
    return min_scores
   
def score_all_abbreviations(abbr_lists, pos_type_lists, char_values):
    """Score all abbreviations in a list of abbreviations.

    Args:
        abbr_lists (List[List[str]]): A list of abbreviation lists.
        pos_type_lists ((str, str, str)): A list of position type lists.
        char_values (dict): Dictionary mapping to char value.

    Returns:
        List[List(abbr, score)]: A list of lists containing abbreviation and their scores.
    """
     
    scored_abbr_lists = []
     
    for abbr_list, pos_type_list in zip(abbr_lists, pos_type_lists):  

        scored_abbr_list = []
        
        # Find score for each abbreviation in the list
        for abbr, pos_types in zip(abbr_list, pos_type_list):

            # Score abbreviation
            abbr_score = score_abbreviation(abbr, pos_types, char_values)  
                    
            # Add abbreviation and score to list
            scored_abbr_list.append((abbr, abbr_score))
            
        scored_abbr_lists.append(scored_abbr_list)
        
    return scored_abbr_lists
                          
def score_abbreviation(abbr, pos_types, char_values):
    """Score the abbreviation.

    Args:
        abbr (str): Abbreviation to score.
        pos_types ((str,str)): Position type for each relevant abbreviation char.
        char_values (Dict[char]: value): Dictionary with char as key and char value as value.

    Returns:
        int: Score of the abbreviation.
    """
    
    score = 0

    # Determine score for each char in abbreviation
    for char, pos_type in zip (abbr, pos_types):
        
        char_score = 0
                
        # Calculate char score
        if pos_type == 'first':
            char_score += 0
        elif pos_type == 'last':
            char_score += 20 if char == 'E' else 5
        else:
            char_score += score_position(pos_type)
            char_score += char_values[char]
    
        # Add char score to overall score
        score += char_score   
        
    return score  
 
def score_position(pos_type):
    """Score position type

    Args:
        pos_type (str): Type of position.

    Returns:
        int: Score
    """
    
    if pos_type == 'second':
        return 1
    elif pos_type == 'third':
        return 2
    elif pos_type == 'middle':
        return 3
    
    return 0

def save_abbreviation(filename, abbr_lists, words):
    """Save words and their abbreviations to a file.

    Args:
        filename (str): Filename of output file.
        abbr_lists (List[List[str]]): A list containing lists of abbreviations.
        words (List[str]): A list of words which each abbr is an abbreviation of.
    """
    
    # Determine outfile name 
    filename = 'jakubek_' + filename + '_abbrevs.txt'
    path = os.path.join(script_directory, filename)
    
    with open(path + '.txt', 'w') as out_file:
    
        # Save word and their abbreviations
        for abbr_list, word in zip(abbr_lists, words):    
            
            all_abbr = " ".join(abbr_list)
            out_file.write('{}\n{}\n'.format(word, all_abbr))
    
def main():
    """Find unique and lowest scoring abbreviations to a list of word. """
    
    # Init char values
    char_values = load_char_values()
    
    # Get filename
    filename = handle_user_input()

    # Read file
    words = load_file(filename)
    
    # Split words
    split_words_lists = split_words(words)

    # Find abbreviations
    abbr_lists, pos_type_lists = find_all_abbreviations(split_words_lists)
    
    # Score all abbreviations
    scored_abbr_lists = score_all_abbreviations(abbr_lists, pos_type_lists, char_values)
    
    # Remove duplicates
    unique_abbr_lists = remove_duplicate_abbreviations(scored_abbr_lists)
    
    # Find all min scoring abbreviations
    min_score_abbr_lists = find_all_min_score_abbreviations(unique_abbr_lists)

    # Save abbreviations
    save_abbreviation(filename, min_score_abbr_lists, words)
    

if __name__ == "__main__":
    main()