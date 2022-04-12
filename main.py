import copy
from typing import List


def calc_all_combination(list_max_index: List[int]):
    '''
    Выводит кол-во всех комбинаций
    '''
    res = 1
    for x in list_max_index:
        res *= x + 1
    return res


def give_nex_index(list_index: List[int], list_max_index: List[int], end: int = -1):
    '''
    Битовое сложение, только слегка сложнее, тк в i значении мб до list_max_index[i] значений
    :param list_index: Текущий массив индексов
    :param list_max_index: Максимально возможные индексы
    :param end: какой с конца меняем рекурсивно
    :return:
    '''
    if list_index[end] < list_max_index[end]:
        list_index[end] += 1
    elif list_index[end] == list_max_index[end]:
        list_index[end] = 0
        give_nex_index(list_index, list_max_index, end=end - 1)


def find_optimal(n: int, words: List[str]):
    '''
    Используем долгий полный перебор и по символьно закрашиваем в таблице, пока все слова не закрашутся (None)
    :param n: размер квадрата
    :return: Если по условию такие слова точно можно найти в таблице, то вернет решенную таблицу
    '''
    all_set = set()
    for x in range(1, n + 1):
        for y in range(1, n + 1):
            all_set.add((x, y))
    list_index = [0] * len(words)
    list_max_index = []
    for x in words:
        list_max_index.append(len(x) - 1)
    len_find = 0
    for word in words:
        len_find += len(word[0])
    all_q = calc_all_combination(list_max_index)
    for i in range(calc_all_combination(list_max_index)):
        flag = True
        info_i = copy.deepcopy(info)
        for index_word in range(len(list_index)):
            index = list_index[index_word]
            for x, y in words[index_word][index]:
                if info_i[x][y] is not None or info_i[x][y].isdigit():
                    info_i[x][y] = index_word
                else:
                    flag = False
                    break
        if flag:
            return info_i
        if i != all_q - 1:
            give_nex_index(list_index, list_max_index, end=-1)


def start_indexs(word: str):
    '''
    Поиск первых букв слова word
    :return:
    '''
    ans = []
    for i, line in enumerate(info):
        for j, el in enumerate(line):
            if el is not None and el == word[0]:
                ans.append([i, j])
    return ans


def start_find_words(words: List[str]):
    '''
    Для каждого слова, запустим рекурсивный поиск полного слова
    :param words: все слова
    :return:
    '''
    ans = []
    for i, word in enumerate(words):
        indexs_start = start_indexs(word)
        ans_i = []
        for i, j in indexs_start:
            find_word(word[1:], [i, j], ans_i)
        ans.append(ans_i.copy())
    return ans


def find_word(simvols_word: str, start_indexs: List[int, int], ans: List[List[int, int]],
              pref: List[List[int, int]] = None):
    '''
    Рекурсивный поиск в рамках одного слова.
    :param simvols_word: осталось найти такое слово
    :param start_indexs: поиск соседей по [i, j] индексу
    :param ans: ответ, куда заполняем результат
    :param pref: не забываем, что уже нашли
    :return: None, ответ в ans
    '''
    pref = pref or [start_indexs]
    i_start, j_start = start_indexs
    new_vars = []
    if len(simvols_word) == 0:
        ans.append(pref)
        return pref
    if info[i_start][j_start - 1] is not None and info[i_start][j_start - 1] == simvols_word[0]:
        new_vars.append([i_start, j_start - 1])
    if info[i_start][j_start + 1] is not None and info[i_start][j_start + 1] == simvols_word[0]:
        new_vars.append([i_start, j_start + 1])
    if info[i_start - 1][j_start] is not None and info[i_start - 1][j_start] == simvols_word[0]:
        new_vars.append([i_start - 1, j_start])
    if info[i_start + 1][j_start] is not None and info[i_start + 1][j_start] == simvols_word[0]:
        new_vars.append([i_start + 1, j_start])
    if not new_vars:
        return []
    for i, j in new_vars:
        new_simvols_word = simvols_word[1:]
        new_pref = pref + [[i, j]]
        find_word(new_simvols_word, [i, j], ans, new_pref.copy())
    return ans


if __name__ == '__main__':
    print("Найти слова по буквам в квадрате NxN")
    n = int(input("N = "))
    k = int(input("Всего слов K = "))
    print("Напишите в 1 строку содержание каждой строки")
    info = [[None for _ in range(n + 1)] for _ in range(n + 2)]
    for i in range(n):
        info[i + 1][1:-1] = [x for x in input()]
    print("Напишите слова которые нужно найти. Каждое слово в новой строке")
    words = [[x for x in input()] for x in range(k)]
    words = start_find_words(words)
    res = find_optimal(n, words)
    print("Решение:")
    print("Каждая цифра означает соответсвующее слово")
    for line in res[1:-1]:
        for el in line[1:-1]:
            print(el, end=" ")
        print("")
