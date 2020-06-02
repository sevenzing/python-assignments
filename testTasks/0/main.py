import re
from typing import List
from functools import reduce 


def get_div_blocks_names(text: str) -> List[str]:
    """
    Returns list with names of div clasess in `text`
    """
    return [match.group(1) for match in re.finditer(r'<div class="([\w ]*)"', text)]



def get_style_block_attributes(text: str):
    blocks = [set(match.group(1).split(';')) 
                for match in re.finditer(r'style="(.*)"', text)]
    
    return list(map(lambda name: concat_to(name, ':').strip(),  
                    reduce(lambda dct, x: dct | x, blocks)))


def concat_to(string: str, symbol: str) -> str:
    return string[:string.find(symbol)]

if __name__ == "__main__":
    html_file_name = 'data.html'
    with open(html_file_name, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
        
        # SUBTASK 1
        names = get_div_blocks_names(html_content)
        # only unique names
        names = list(set(names))
        print(sorted(names))

        # SUBTASK 2
        attrs = get_style_block_attributes(html_content)
        # only unique names
        attrs = list(set(attrs))
        print(attrs)
        
        
