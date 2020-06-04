import re

def get_block_classes(block_name, text):
    blocks = [match.group(1).split() for match in re.finditer('<' + block_name + r'\s+class="([\w -]*)"', text)]
    allblocks = []
    for block in blocks:
        allblocks.extend(block)
    return allblocks

if __name__ == "__main__":
    file_name = 'text.html'

    with open(file_name, 'r') as _file:
        text = _file.read()

    # подзадание 1
    print('все виды классов:')
    for class_name in set(get_block_classes('\w+', text)):
        print(class_name, end =' ')

    print()

    # подзадание 2
    print('все виды классов в ol:')
    for class_name in set(get_block_classes('ol', text)):
        print(class_name, end =' ')

    print()
    
    # подзадание 3
    print('все виды классов в ul:')
    for class_name in set(get_block_classes('ul', text)):
        print(class_name, end =' ')

    print()
