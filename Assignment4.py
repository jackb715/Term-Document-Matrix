#!/usr/bin/env python3

'''
1. Split sentence by spaces
2. Remove numbers and symbols() from words
3. Convert to lower case
5. remove stop words from dictionary
------------------------------------------------------------
6. perform stemming ie. computer-program -> computer program
7.
'''
def read_file(filename):
    f = open(filename)
    return f.readlines()

def remove_chars(line):
    special_chars = [',',';','.','"',')','(','1','2','3','4','5','6','7','8','9','\n']
    blank = ''
    words = line.split()
    fixed_word = ""
    new_words = []
    for w in words: #remove special characters
        new_word = w
        for c in special_chars:
            new_word = new_word.replace(c, blank)
        new_words.append(new_word)
    new_words2 = []
    for w in new_words: # remove blank words and make all words lower case
        if not w == "":
            new_words2.append(w.lower())
    return new_words2

def remove_stop_words(words):
    stop_f = open("stop_words.txt")
    sw = stop_f.read().replace('\n',' ')
    sw = sw.split()
    words2 = []
    is_sw = False
    for w in words:
        for s in sw:
            if w==s:
                is_sw = True
                break  # move to next word
        if not is_sw:
            words2.append(w)
        else:
            is_sw = False
    return words2

def main():
    lines = read_file("paragraphs.txt")
    new_f = open("edit.txt", 'w')

    edit = remove_stop_words(remove_chars(lines[0]))

    for w in edit:
        new_f.write(w + " ")



if __name__=='__main__':
    main()
