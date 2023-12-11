import os

script_directory = os.path.dirname(os.path.abspath(__file__))

def load_char_values():
    """Load character values as a dictionary from a file.

    Returns:
        Dict[char, int]: Dictionary mapping character to their score.
    """

    path = os.path.join(script_directory, 'values')
    
    char_value = {}
    
    with open(path + '.txt', 'r') as in_file:
        for line in in_file:
            
            # Get key value pairs
            char, value = line.split()
            
            char_value[char] = int(value)

    return char_value

def handle_user_input():
    """Prompt user for a filename as an input and validate it.
    
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
    """Load a file as a list of strings.

    Args:
        filename (str): Name of the file we read data from.

    Returns:
        List[str]: A list of strings in the file.
    """
    # Path to file
    path = os.path.join(script_directory, filename)

    word_list = []
    with open(path + '.txt', 'r') as in_file:
        
        word_list = [line.strip() for line in in_file if line.strip()]

    return word_list

def save_abbreviation(filename, abbr_lists, words):
    """Save words and their abbreviations to a file.

    Args:
        filename (str): Filename of the output file.
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