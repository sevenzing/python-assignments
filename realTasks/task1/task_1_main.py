def normalize_word(word):
    """
    удаляет все небуквыенные символы кроме -
    """
    new_word = ''

    for symbol in word:
        if (symbol.isalpha() or symbol == '-'):
            new_word += symbol
    
    return new_word

if __name__ == "__main__":
    pos_file_name = 'pos.txt'
    book_file_name = 'powerpoint.txt'

    with open(pos_file_name, 'r', encoding='utf-8') as pos_file:
        pos_text = pos_file.read().strip()

    with open(book_file_name, 'r', encoding='utf-8') as book_file:
        book_text = book_file.read().strip().lower()

    # для подзадачи 1
    # словарь, где ключ - слово, значение - список граммем
    dictionary = {}

    # для подзадачи 2
    tags_with_nouns = {}

    for line in pos_text.split('\n'):
        word, raw_grammemes = line.split('->')
        
        # удаляю ненужные пробелы в начале и в конце, убираем заглавные буквы для удобства
        word = word.strip().lower()
        raw_grammemes = raw_grammemes.strip()
        
        # разделяем по запятым
        grammemes = raw_grammemes.split(',')

        # на всякий случай убираем лишние пробелы        
        for i in range(len(grammemes)):
            grammemes[i] = grammemes[i].strip()
        
        # для подзадачи 2
        if 'NOUN' in grammemes:
            for grammeme in grammemes:
                if grammeme != 'NOUN':
                    tags_with_nouns.setdefault(grammeme, 0)
                    tags_with_nouns[grammeme] += 1

        dictionary[word] = grammemes

    nouns = 0
    for word in book_text.split():
        word = normalize_word(word.strip().lower())

        if word not in dictionary:
            # такого слова нет в словаре
            continue 
        
        if 'NOUN' in dictionary[word]: 
            # мы нашли сущесвительное
            nouns = nouns + 1
    

    print('всего существительных: ' + str(nouns))

    def _max(key):
        return tags_with_nouns[key]
    
    tag = str(max(tags_with_nouns, key=_max))
    print('самый частый тэг с существительным: ' + tag + ': '  + str(tags_with_nouns[tag]))