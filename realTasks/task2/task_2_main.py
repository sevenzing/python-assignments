import json
import re

def normalize_word(word):
    """
    удаляет все небуквыенные символы кроме -
    """
    new_word = ''

    for symbol in word:
        if (symbol.isalpha() or symbol == '-'):
            new_word += symbol
    
    return new_word.lower()

def get_text_from_message(message):
    if isinstance(message['text'], str):
        return message['text']
    else:
        text = ''
        for token in message['text']:
            if isinstance(token, str):
                text += token
        
        return text


def get_urls_from_message(message):
    if not isinstance(message['text'], list):
        return []
    else:
        links = []
        for token in message['text']:
            if isinstance(token, dict):
                if token['type'] == 'link':
                    links.append(token['text'])
                if token['type'] == 'text_link':
                    links.append(token['href'])
        
        return links

def get_mentions_from_message(message):
    if not isinstance(message['text'], list):
        return []
    else:
        mentions = []
        for token in message['text']:
            if isinstance(token, dict):
                if token['type'] == 'mention':
                    mentions.append(token['text'])
        
        return mentions


def get_FQDN_from_url(url):
    return re.match(r'^(http)?s?(:\/\/)?(www.)?([\w\.]+).*$', url).group(4)

if __name__ == "__main__":
    json_file_name = 'result.json'

    chat = json.load(open(json_file_name))

    professors = [
        'Anna Klezovich', 'Nikita Sapunov', 'Oleg Serikov', 'Olga 𝓸𝓵𝓮𝓼𝓪𝓻 Lyashevskaya', 
        '@annaklezovich', '@sapunov', '@oserikov', '@olesar'
        ]
    assistants = [
        'Katya Taktasheva', 'Olga Pitchuzhkina', 'Anton Buzanov', 'Alina Rogulina',
        '@tak_ty', '@olgap981', '@Vantral', '@avrogulina'
    ]


    professors_phrases = {}
    assistants_phrases = {}
    student_phrases = {}

    unique_FQDNs = set()
    
    result_mentions = {'student': 0, 'other': 0}
    for message in chat['messages']:
        if 'from' not in message:
            # not text message
            continue

        name = message['from']
        
        text = get_text_from_message(message)
        
        words = text.split()
        for i in range(len(words)):
            words[i] = normalize_word(words[i])  
        
        # подзадачи 2-4
        for word in words:
            if word == '':
                continue
            if name in professors:
                # нашли профессор
                professors_phrases.setdefault(word, 0)
                professors_phrases[word] += 1
            
            elif name in assistants:
                # нашли ТА
                assistants_phrases.setdefault(word, 0)
                assistants_phrases[word] += 1
            else:
                # нашли студента
                student_phrases.setdefault(word, 0)
                student_phrases[word] += 1
        
        # подзадача 5
        links = get_urls_from_message(message)
        FQDNs = set()
        for link in links:
            FQDNs.add(get_FQDN_from_url(link))
        unique_FQDNs = unique_FQDNs | FQDNs

        # подзадача 6
        mentions = get_mentions_from_message(message)
        for mention in mentions:
            if mention in professors or mention in assistants:
                # если пинг на профессора или ассистента
                result_mentions['other'] += 1
            else:
                # если пинг на студента
                result_mentions['student'] += 1

    def _max_prof(key):
        return -professors_phrases[key]

    print('профессора:')
    for word in sorted(professors_phrases, key=_max_prof)[:10]:
        print(word, professors_phrases[word])
    print()

    def _max_assis(key):
        return -assistants_phrases[key]

    print('ассистенты:')
    for word in sorted(assistants_phrases, key=_max_assis)[:10]:
        print(word, assistants_phrases[word])
    print()

    def _max_stud(key):
        return -student_phrases[key]

    print('ассистенты:')
    for word in sorted(student_phrases, key=_max_stud)[:10]:
        print(word, student_phrases[word])
    
    print()
    print('уникальные ссылки: ' + str(unique_FQDNs))

    print()
    print('mentions: ' + str(result_mentions))
    print('Студентов пинговали меньше, чем других')

"""
Итог:

профессора:
в 375
и 309
не 272
на 221
если 165
я 164
что 154
то 125
будет 120
а 119

ассистенты:
в 78
не 68
за 52
и 46
оценки 46
дз 42
если 34
что 33
я 29
а 27

ассистенты:
в 236
а 169
не 118
спасибо 110
и 106
что 95
по 88
на 79
или 75
с 72

уникальные ссылки: {'colab.research.google.com', 'ummerofcode.withgoogle.com', 'stackoverflow.com', 'b.py', 'pip.pypa.io', 't.me', 'youtu.be', 'padlite.spline.de', 'docs.python.org', 'ria.ru', 'youtube.com', 'github.com', 'etherpad.net', 'regular', 'summerofcode.withgoogle.com', 'kaggle.com', 'interestinglife.ru', 'pythontutor.com', 'docs.google.com', 'doodle.com', 'us04web.zoom.us', 'file.read', 'pykili.github.io', 'zoom.us', 'forms.gle', 'google.com', 'reddit.com', 'pythonworld.ru', 'a.py', 'wiki.cs.hse.ru', 'jetbrains.com', 'gist.github.com', 'drive.google.com', 'letnyayashkola.org', 'online', 'bit.ly', 'classroom.github.com', 'regex101.com', 'tproger.ru'}

{'student': 6, 'other': 57}
Студентов пинговали меньше, чем других
"""