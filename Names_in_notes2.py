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

def endsent(word1):
    end = '!?.),;:"*»…$'
    if word1[-1] in end:
        return 'End'
    else:
        return 'Not the end'

def startsent(word2):
    start = '(*«:;-'
    if word2 =='':
        return 'Not the start'
    elif word2[0] in start:
        return 'Start'
    else:
        return 'Not the start'

def adding(sent, d, name):
    if sent[0] in d:
        d[sent[0]].add(name)
    else:
        d[sent[0]] = set()
        d[sent[0]].add(name)
    return d

def proverka1(sent, d):
    if sent[1].startswith('Мендель'):
        a1 = adding(sent, d, 'Менделеев')
    for index in range(len(sent)):
        if index != 1:
            word1 = sent[index]
            if sent[1].startswith('Бубнов'):
                if 'бубнов' in word1:
                    a1 = adding(sent, d, 'Бубнов')
            elif sent[1].startswith('Бeнтам'):
                if 'бентам' in word1:
                    a1 = adding(sent, d, 'Бентам')
            elif sent[1].startswith('Подгорный'):
                if 'подгорное' in word1:
                    a1 = adding(sent, d, 'Подгоный')
            elif sent[1].startswith('Луначарский'):
                if 'луначарская' in word1:
                    a1 = adding(sent, d, 'Луначарский')
            elif sent[1].startswith('Дзержинский'):
                if 'дзержинское' in word1:
                    a1 = adding(sent, d, 'Дзержинский')
            else:
                continue
        else:
            continue
    return d

def Lenin():
    f = open('Nicknames_Lenin.txt', 'r', encoding = 'utf-8')
    strings = f.read()
    lenin = re.findall('(.*?)\t', strings)
    return lenin

def Stalin():
    f = open('Nicknames_Stalin.txt', 'r', encoding = 'utf-8')
    strings = f.read()
    stalin = re.findall('(.*?)\t', strings)
    return stalin

def Hitler():
    f = open('Nicknames_Hitler.txt', 'r', encoding = 'utf-8')
    strings = f.read()
    hitler = re.findall('(.*?)\t', strings)
    return hitler

def proverkaNicks(sent, index, d):
    leni = Lenin()
    hitl = Hitler()
    stal = Stalin()
    name = re.sub('\{.*?\}', '', sent[1])
    if name in leni:
        if name == 'Ильич':
            if 'Ильич' in sent[index]:
                if 'имя' in sent[index-1]:
                    if 'Владимир' in sent[index-1]:
                        a1 = adding(sent, d, 'Ленин')
                else:
                    a1 = adding(sent, d, 'Ленин')
        else:
            a1 = adding(sent, d, 'Ленин')
    elif name in hitl:
        a1 = adding(sent, d, 'Гитлер')
    elif name in stal:
        a1 = adding(sent, d, 'Сталин')
    else:
        return "Non"
    return d

def start(sent, index, alf, d, Name):
    if sent[index-1] in alf:
        a2 = proverkaNicks(sent, index, d)
        if a2 == 'Non':
            a1 = adding(sent, d, Name)
    elif endsent(sent[index-1]) == 'End':
        a2 = proverkaNicks(sent, index, d)
        if a2 == 'Non':
            a1 = adding(sent, d, Name)
    return d

def points(sent, index, alf, d, Name, s8):
    if sent[index+1] in alf:
        a2 = proverkaNicks(sent, index, d)
        if a2 == 'Non':
            a1 = adding(sent, d, Name)
    elif startsent(sent[index+1]) == 'Start':
        a2 = proverkaNicks(sent, index, d)
        if a2 == 'Non':
            a1 = adding(sent, d, Name)
    if '=S,' in sent[index+1]:
        if 'фам' in sent[index+1]:
            a2 = proverkaNicks(sent, index, d)
            if a2 == 'Non':
                a1 = adding(sent, d, Name)
        else:
            s8.append(sent) # - для ручной проверки
    return d

def proverka2(name, sent, index, d, Name, s8):
    x = name + '=S'
    word1 = sent[index]
    alf = '!@#$%^&*()_+=-}{[]\|":/.,…<>;«»„“'
    if x in word1:
        if endsent(word1) == 'End':
            a2 = proverkaNicks(sent, index, d)
            if a2 == 'Non':
                a1 = adding(sent, d, Name)
        elif index == len(sent)-1:
            a1 = start(sent, index, alf, d, Name)
        elif index != len(sent)-1:
            a1 = points(sent, index, alf, d, Name, s8)
##        elif '=S,' in sent[index+1]:
##            if 'фам' in sent[index+1]:
##                a2 = proverkaNicks(sent, index, d)
##                if a2 == 'Non':
##                    a1 = adding(sent, d, Name)
##            else:
##                s8.append(sent) # - для ручной проверки
        else:
            a2 = proverkaNicks(sent, index, d)
            if a2 == 'Non':
                a1 = adding(sent, d, Name)
    return d 
    
def searching(a1):
    d = {} # {id : {surname}}
    s8 = [] 
    for i in a1:
        if i != '':
            i2 = re.sub('\xa0', ' ', i)
            sent = i2.split(' ')
            a3 = sent[1].split('{')
            name = a3[0].lower()
            a5 = re.findall(name, i2)
            if len(a5) == 1:
                a6 = proverka1(sent, d)
            elif len(a5) == 2:
                for index in range(len(sent)):
                   if index > 1:
                       a4 = proverka2(name, sent, index, d, a3[0], s8)
            else: # - если имя употребляется больше 1 раза в тексте, то скорее всего омонимии не будет
                for index in range(len(sent)):
                   if index > 1:
                       a2 = proverkaNicks(sent, index, d)
                       if a2 == 'Non':
                           a1 = adding(sent, d, a3[0])
##    f = open('not.txt', 'a', encoding = 'utf-8')
##    for po in s8:
##        f.write(str(po) + '\n\n')
##    f.close()
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
    for i in sorted(dict(numbers)):
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
