def load_file(filename):
### Load file lines into a dictonary ###

    word_list = []
    infile = open(filename + '.txt', 'r')

    for line in infile:
        word_list.append(line.strip())

    return word_list
        
        
words = load_file('test')
