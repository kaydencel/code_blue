'''
filename: codeblue_parsers.py
'''

import re
from collections import Counter

def script_parser(filename, greys=False, scrubs=False, mindy=False, resident=False, stopwords=None):
    '''parser for scripts, creates a nested dictionary where the key is the character and the values are their lines'''
    dialogues = {}
    words = []
    character = None
    remove_block = False

    with open(filename, 'r') as infile:
        script = infile.read()

    # remove 'GREY'S ANATOMY' (non-dialogue); replace "MERDITH" with "MEREDITH" into one character; typo in script
    if greys:
        script = re.sub(r'GREY\'S ANATOMY.*', '', script)
        script = script.replace('MERDITH', 'MEREDITH')
    # remove words after 'SCRUBS' (non-dialogue); replace "MS PRATI" with "MS PRATT" into one character; typo in script
    if scrubs:
        script = re.sub(r'SCRUBS.*', '', script)
        script = script.replace('MS PRATI', 'MS PRATT')
    # remove 'Untitled' (non-dialogue)
    if mindy:
        script = re.sub(r'Untitled.*', '', script)
    # remove 'Kings County' (non-dialogue)
    if resident:
        script = re.sub(r'Kings County.*', '', script)

    # remove text in parentheses and curly brackets; remove special characters
    script = re.sub(r'[\(\[\{].*?[\)\]\}]', '', script)
    script = re.sub(r'[^\w\s]', '', script)

    # list of words to remove lines that are stage directions, settings, descriptions, and other non-dialogue lines
    remove = ['CONTINUED', 'CONTINUOUS', 'OMITTED', 'MOVED', 'INT', 'EXT', 'ACT', 'ON', 'MONTAGE',
              'CLOSE', 'OPEN', 'AND', 'CUT', 'FADE', 'ENTERS', 'EXITS', 'FRAME', 'BEGINS', 'ENDS', 'CLOSE']

    lines = script.split('\n')

    for line in lines:
        # remove non-dialogue lines
        if any(word in line.split() for word in remove):
            remove_block = True
            continue

        # find characters
        if line.isupper():
            if remove_block:
                remove_block = False

            character = line.strip()
            character = ' '.join(character.split())

            # find characters that already exists with different whitespace (JD character in SCRUBS)
            existing_character = list(dialogues.keys())
            similar_character = [existing_char for existing_char in existing_character if
                                  existing_char.replace(" ", "") == character.replace(" ", "")]

            if similar_character:
                character = similar_character[0]

        elif character and not remove_block:
            # add new characters to dictionary
            if character not in dialogues:
                dialogues[character] = []

            # add lines to the character and skip empty lines
            if line.strip():
                dialogues[character].append(line.strip().lower())
                words.extend(line.strip().lower().split())

    # calculate word counts
    if stopwords:
        words = [word for word in words if word.lower() not in stopwords]
    word_count = Counter(words)

    return {'dialogues': dialogues,
            'word_count': word_count}

def house_parser(filename, stopwords=None):
    '''custom parser for house scripts, creates a nested dictionary where the key is the character and the value are
    their lines'''
    dialogues = {}
    words = []

    with open(filename, 'r') as infile:
        for line in infile:
            line = line.strip()

            # get characters and their lines
            if line and '[' not in line and ':' in line:
                character, dialogue = map(str.strip, line.split(':', 1))
                curr_character = character.strip()

                # add new character to dictionary
                if curr_character not in dialogues:
                    dialogues[curr_character] = []

                # add lines to the character
                dialogue = re.sub(r'[^\w\s]', '', dialogue)
                dialogues[character].append(dialogue.strip().lower())
                words.extend(dialogue.strip().lower().split())

    # calculate word counts
    if stopwords:
        words = [word for word in words if word.lower() not in stopwords]
    word_count = Counter(words)

    return {'dialogues': dialogues,
            'word_count': word_count}