import re
import pytils.translit
from jellyfish import hamming_distance


def check_validity_name(name: list):
    if len(name) == 2:
        if len(name[0]) > 1 and len(name[1]) > 1:
            return True
    else:
        return False


def prepare_string(value: str):
    bad_symbols = ("-", "_", "(", ")", "$", "#", "@", "^", "&", "%", "*", "+", "=", "/")
    for x in bad_symbols:
        if x in value:
            value = value.replace(x, "")
    return value


def is_cyrillic(text):
    return len(text) == len(re.findall('[\u0400-\u04FF]', text))


def convert_to_cyrillic(name_and_surname_list):
    for item, value in enumerate(name_and_surname_list):
        transliterared_word = pytils.translit.detranslify(value)
        name_and_surname_list[item] = transliterared_word
    return name_and_surname_list


def get_name_val(name_and_surname: str) -> tuple:
    cur_name = name_and_surname
    name_and_surname = name_and_surname.strip().lower()
    name_and_surname_list = name_and_surname.split()
    name_and_surname_list = [prepare_string(value) for value in name_and_surname_list]

    is_valid_name = check_validity_name(name_and_surname_list)
    if not is_valid_name:
        return (cur_name, False)

    cyryllic = all(map(is_cyrillic, name_and_surname_list))
    if cyryllic:
        return ((cur_name, name_and_surname_list), True)
    else:
        name_and_surname_list = convert_to_cyrillic(name_and_surname_list)
        return ((cur_name, name_and_surname_list), True)


def check_addable(nickname: list, good_name: str):

    good_name = good_name.lower()
    combination = " ".join(list(reversed(nickname)))
    nickname = " ".join(nickname)

    res1 = hamming_distance(nickname, good_name)
    res2 = hamming_distance(combination, good_name)
    dist = 4
    return any((res1 < dist, res2 < dist))
