import re
import urllib.request
from collections import Counter
import os

# структура таблицы insert into Tages values ("id", "Name", "Text", *"id текста")

def opening():
    f = open('output_texts/rouge.txt', 'r', encoding = 'utf-8')
    pip = f.read()
    f.close()
    a1 = pip.split('\t')
    return a1

def searching(a1):
    d = {} # {id : {surname}}
    for i in a1:
        if i != '':
            sent = i.split(' ')
            a3 = sent[1].split('{')
            name = a3[0].lower()
            for index in range(len(sent)):
                if index != 0:
                    if sent[index] != sent[-1]:
                        if name + '=S' in sent[index]:
                            if '=S' in sent[index+1]:
                                continue
                            else:
                                if sent[0] in d:
                                    d[sent[0]].add(name)
                                else:
                                    d[sent[0]] = set()
                                    d[sent[0]].add(name)
    return d

## структура таблицы insert into Tages values ("id", "id Text", "Name")
## 'insert into Tages values ("' + str(idd) + '", "' + l + '", "' + i + '")' + '\n'

def inserts(d):
    values = []
    num = 0
    number = 1
    for i in d:
        num += len(d[i])
    f = open('Inserts_Names.txt', 'a', encoding = 'utf-8')
    while number <= num:
        for key in d:
            for value in d[key]:
                values.append(value)
                f.write("insert into Tages values ('%d', '%s', '%s')" % (number, key, value) + '\n')
                number += 1     
    f.close()
    return values

def numbers(values): # - специальная фунцкция для частотности
    f = open('Частотность_фамилий.txt', 'a', encoding = 'utf-8')
    numbers = Counter(values)
    for i in dict(numbers):
       f.write(i + ': ' + str(numbers[i]) + '\n')
    f.close()
    return 

def final():
    a1 = opening()
    a3 = searching(a1)
    a4 = inserts(a3)
    a5 = numbers(a4)
    return

if __name__=='__main__':
    final()


