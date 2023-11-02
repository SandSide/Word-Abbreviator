

def load_file(filename):
### Load file lines into a dictonary ###

    word_list = []
    infile = open(filename + '.txt', 'r')

    for line in infile:
        word_list.append(line.strip())

    return word_list
        
def convert_to_correct_format(dict):
    correct_format_dict = []
    
    for word in dict:
        # Split string by empty space
        temp_dict = word.split()
        
        # for word_part in temp_dict:
            
        # print(temp_dict)
    

words = load_file('test')
convert_to_correct_format(words)
