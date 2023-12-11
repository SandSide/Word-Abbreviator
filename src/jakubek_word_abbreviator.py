import re
import os
import jakubek_utility as utility


def split_string(word):
    """Split word into a suitable format for abbreviation.

    Args:
        word (str): String to split.

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
    """Find all 3 letter abbreviations for each word in the list.

    Args:
        split_words (List[List[str]]): A list of split words.

    Returns:
        List[List[abbr]]: A list of abbreviations for each split word.
        List[List[Tuple(str,str,str)]]: A tuple of position types for each abbreviations character for each split word.
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
    """Find all 3 letter abbreviations for a string made out of a list of words.

    Args:
        words (List[str]): String of words to find an abbreviations for.

    Returns:
        List[str]: A list of abbreviations.
        List(Tuple(str,str,str)): A list of position type tuples for each character in abbreviation.
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
        positions (Tuple(int,int,int)): Positions of abbreviation characters.
        chars (str): A string the abbreviation was made from.

    Returns:
        Tuple(str,str,str): Tuple of position types.
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
        scored_abbr_lists (List[List[Tuple(str, int)]]): A list of scored abbreviations.

    Returns:
        List[List[Tuple(str, int)]]: A list of unique scored abbreviations.
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
        
        # Remove duplicates from list based on the index
        unique_abbr_list = [v for i,v in enumerate(abbr_list) if i not in duplicate_indexes]

        new_abbr_lists.append(unique_abbr_list)
        
    return new_abbr_lists

def find_all_min_score_abbreviations(scored_abbr_lists):
    """Finds all abbreviations which have min score for each abbreviations list.

    Args:
        scored_abbr_lists (List[List[Tuple(str, score]]): A list of abbreviation and their score lists.

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
        scored_abbr_lists ([List[Tuple(str, score)]): A list of abbreviation lists.

    Returns:
        List[Tuple(str, score)]]: A list of min scoring abbreviation tuples containing abbr and its score.
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
        pos_type_lists (Tuple(str, str, str)): A list of position type lists.
        char_values (Dict[char,int]): Dictionary mapping to char value.

    Returns:
        List[List[Tuple(abbr, score)]]: A list of lists containing abbreviation and their scores.
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
        pos_types (Tuple(str,str,str)): Position type for each relevant abbreviation char.
        char_values (Dict[char,int]): Dictionary with char as key and char value as value.

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

def main():
    """Find unique and lowest scoring abbreviations to a list of word. """
    
    # Init char values
    char_values = utility.load_char_values()
    
    # Get filename
    filename = utility.handle_user_input()

    # Read file
    words = utility.load_file(filename)
    
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
    utility.save_abbreviation(filename, min_score_abbr_lists, words)
    
    print('Script Finished')
    

if __name__ == "__main__":
    main()