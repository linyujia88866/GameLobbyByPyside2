import random


# # 将每个成语分割成单个词语，并组合成16组
# word_groups = []
# for idiom in selected_idioms:
#     word_groups.extend(list(idiom))
#
# # 打乱词语列表
# random.shuffle(word_groups)
#
# # 输出结果
# print(word_groups)

def gen_words(idioms):
    # 成语列表
    # idioms = readWords.read_words()[0:8]
    new_is = []
    # # 随机选择8个成语
    # selected_idioms = random.sample(idioms, 8)
    # print(selected_idioms)
    for i in idioms:
        new_is.append(i[:2])
        new_is.append(i[2:])
    random.shuffle(new_is)
    return new_is

if __name__ == '__main__':
    words = gen_words(['1111', '2244', '6677'])
    print(words)