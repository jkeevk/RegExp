import csv
import re


# функция получения списка строк из csv файла
def open_file(file):
    with open(file, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    return contacts_list


# функция структурирования ФИО
def structure_names(contacts_list):
    header = contacts_list.pop(0)
    result = [header]
    for row in contacts_list:
        full_name = " ".join(row[:3]).split()
        result.append([
            full_name[0], full_name[1], full_name[2] if len(full_name) > 2 else "",
            row[3], row[4], row[5], row[6]
        ])

    return result


# функция регулярных выражений для замены номера телефона
def structure_phones(result):
    pattern = r"(\+7|8)?\s*\(*(\d{3})\)*[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*\(*([доб\.]*)\s*(\d{4})?\)*"
    substr = r"+7(\2)\3-\4-\5 \6\7"
    pattern_comp = re.compile(pattern)

    for row in result:
        correct_phone = pattern_comp.sub(substr, row[5])
        row[5] = correct_phone.strip()

    return result


# функция группирования дубликатов
def structure_dublicates(result):
    result_list = []
    for i in range(len(result)):
        for s in range(len(result)):
            if result[i][0] == result[s][0] and result[i][1] == result[s][1]:
                result[i] = [x or y for x, y in zip(result[i], result[s])]
        if result[i] not in result_list:
            result_list.append(result[i])

    return result_list


# функция записи в файл csv
def write(file, result):
    with open(file, "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(result)


if __name__ == '__main__':
    contacts_list = open_file('phonebook_raw.csv')
    corrected_names = structure_names(contacts_list)
    corrected_phones = structure_phones(corrected_names)
    corrected_raws = structure_dublicates(corrected_phones)
    write('phonebook.csv', corrected_raws)
