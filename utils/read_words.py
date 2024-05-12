import os
import random


def read_words():
    words = []
    current_directory = os.path.dirname(__file__)
    with open(os.path.join(current_directory, '../resource/wordsBase.txt'), 'r', encoding='utf-8') as file:
        content = file.read()
        new_content = content.replace("、", "").replace(",", "").replace(" ", "").replace("，", "").replace("\n", "")
        length = new_content.__len__() // 4
        # print(new_content)
        for i in range(0, length):
            words.append(new_content[i * 4: i * 4 + 4])
    return words


def random_words(x):
    words = read_words()
    length = words.__len__()
    result = []
    i = 0
    while i < x:
        j = random.randint(0, length)
        if words[j] not in result:
            result.append(words[j])
            i = i + 1
    return result


if __name__ == '__main__':
    res = random_words(10)
    print(res)
