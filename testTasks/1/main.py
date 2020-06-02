# Unfortunately I still don't understand why 
# I need the file 'powerpoint.txt' and why 
# can't I solve the problem without it
#
# I hope I understood the problem correctly

ARROW = '->'

if __name__ == "__main__":
    pos_file_name = 'pos.txt'
    book_file_name = 'powerpoint.txt'

    with open(pos_file_name, 'r', encoding='utf-8') as pos_file:
        pos_text = pos_file.read().strip()

    with open(book_file_name, 'r', encoding='utf-8') as book_file:
        book_text = book_file.read().strip().lower()

    result = {'nouns': 0, 'verbs': 0}
    for line_number, line in enumerate(pos_text.split('\n')):
        assert ARROW in line, f"There is no {ARROW} in the line #{line_number + 1}"
        word, raw_grammemes = map(lambda x: x.strip(), line.split(ARROW))
        assert word.lower() in book_text, f"Word {word} not in the text"

        grammemes = list(map(lambda x: x.strip(), raw_grammemes.split(',')))
        
        if   'NOUN' in grammemes:
            result['nouns'] += 1
        elif 'VERB' in grammemes:
            result['verbs'] += 1
        else:
            # just skip it
            pass
        
    print(f"Nouns: {result['nouns']}, verbs: {result['verbs']}. "\
           'There are more ' + \
           'nouns than verbs' 
            if result['nouns'] > result['verbs']     
            else 'verbs than nouns')