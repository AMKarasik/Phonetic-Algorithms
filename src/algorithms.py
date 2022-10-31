import re


def soundex_generator(word):
    # Convert the word to upper case for uniformity
    word = word.upper()

    soundex = ""

    # Retain the first letter
    soundex += word[0]

    # Create a dictionary which maps letters to respective soundex codes. Vowels & 'H, W, Y' will be represented by '.'
    dictionary = {"BFPV": "1", "CGJKQSXZ": "2", "DT": "3", "L": "4", "MN": "5", "R": "6", "AEIOUHWY": ""}

    for char in word[1:]:
        for key in dictionary.keys():
            if char in key:
                code = dictionary[key]
                if code != '':
                    if code != soundex[-1]:
                        soundex += code

    # Trim or pad to make SoundEx a 4-character code
    soundex = soundex[:4].ljust(4, "0")

    return soundex


_vowels = 'AEIOU'


def replace_at(text, position, fromlist, tolist):
    for f, t in zip(fromlist, tolist):
        if text[position:].startswith(f):
            return ''.join([text[:position],
                            t,
                            text[position+len(f):]])
    return text


def replace_end(text, fromlist, tolist):
    for f, t in zip(fromlist, tolist):
        if text.endswith(f):
            return text[:-len(f)] + t
    return text


def nysiis(name):
    name = re.sub(r'\W', '', name).upper()
    name = replace_at(name, 0, ['MAC', 'KN', 'K', 'PH', 'PF', 'SCH'],
                               ['MCC', 'N',  'C', 'FF', 'FF', 'SSS'])
    name = replace_end(name, ['EE', 'IE', 'DT', 'RT', 'RD', 'NT', 'ND'],
                             ['Y',  'Y',  'D',  'D',  'D',  'D',  'D'])
    key, key1 = name[0], ''
    i = 1
    while i < len(name):
        n_1, n = name[i-1], name[i]
        n1_ = name[i+1] if i+1 < len(name) else ''
        name = replace_at(name, i, ['EV'] + list(_vowels), ['AF'] + ['A']*5)
        name = replace_at(name, i, 'QZM', 'GSN')
        name = replace_at(name, i, ['KN', 'K'], ['N', 'C'])
        name = replace_at(name, i, ['SCH', 'PH'], ['SSS', 'FF'])
        if n == 'H' and (n_1 not in _vowels or n1_ not in _vowels):
            name = ''.join([name[:i], n_1, name[i+1:]])
        if n == 'W' and n_1 in _vowels:
            name = ''.join([name[:i], 'A', name[i+1:]])
        if key and key[-1] != name[i]:
            key += name[i]
        i += 1
    key = replace_end(key, ['S', 'AY', 'A'], ['', 'Y', ''])
    return key1 + key


def lev_dist(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, \
                                  current_row[j - 1] + 1, \
                                  previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


if __name__ == '__main__':
    # print(nysiis('Archipcev'), nysiis('Archipychev'), nysiis('Archipkov'))
    # print(soundex_generator('Archipcev'), soundex_generator('Archipychev'), soundex_generator('Archipkov'))
    print(lev_dist('ATCAAGGGACC', 'ATCGCAATAGC'))
