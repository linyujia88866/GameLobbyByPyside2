import random


def gen_words(idioms):
    new_is = []

    for i in idioms:
        new_is.append(i[:2])
        new_is.append(i[2:])
    random.shuffle(new_is)
    return new_is


if __name__ == '__main__':
    words = gen_words(['1111', '2244', '6677'])
    print(words)
