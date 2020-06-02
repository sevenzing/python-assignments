from json import loads 
import csv

def normalize_word(word: str) -> str:
    """
    Remove all non-alhpa symbols
    """
    return ''.join(list(filter(str.isalpha, word)))

if __name__ == "__main__":
    jsons_file_name = 'hw_3_twitter.json'    
    file_out_name = 'sample.tsv'

    with open(jsons_file_name, 'r') as jsons_file:
        twitts = list(filter(lambda item: item != '',
                        map(lambda json: '' if 'text' not in json else json['text'],
                            map(lambda line: loads(line), jsons_file.readlines()))))
        
    frequency_list = {}
    
    for twitt in twitts:
        words = filter(lambda word: word != '',
                    map(lambda word: word.lower().strip(), 
                        map(normalize_word, twitt.split())))
        for word in words:
            frequency_list.setdefault(word, 0)
            frequency_list[word] += 1
    
    with open(file_out_name, 'wt') as file_out:
        tsv_writer = csv.writer(file_out, delimiter='\t')
        tsv_writer.writerow(["Word", "Frequency"])
        for word in sorted(frequency_list, key=lambda key: -frequency_list[key]):
            tsv_writer.writerow([word, str(frequency_list[word])])
