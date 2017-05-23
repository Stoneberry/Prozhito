import re
import urllib.request
from collections import Counter
import os
import time
from Names_code import open_names
from memory_profiler import profile

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
        if word1[-2] in end:
            return 'End'
        else:
            return 'Not the end'

def startsent(word2):
    start = '(*«:;"-'
    if word2 =='':
        return 'Not the start'
    elif word2[0] in start:
        return 'Start'
    else:
        return 'Not the start'

def adding(sent, d, name1):
    name = name1[0].upper() + name1[1:]
    if sent[0] in d:
        d[sent[0]].add(name)
    else:
        d[sent[0]] = set()
        d[sent[0]].add(name)
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
    name1 = re.sub('\{.*?\}', '', sent[1])
    name = name1[0].upper() + name1[1:]
    if name in leni:
        if name == 'Ильич':
            if 'Ильич' in sent[index]:
                if 'имя' in sent[index-1]:
                    if 'Владимир' in sent[index-1]:
                        a1 = adding(sent, d, 'Ленин')
                else:
                    a1 = adding(sent, d, 'Ленин')
        elif name == 'Ульянов':
            if 'Ульянов' in sent[index]:
                if 'имя' in sent[index-1]:
                    if 'Владимир' in sent[index-1]:
                        a1 = adding(sent, d, 'Ленин')
                elif 'сокр' in sent[index-1]:
                    if 'В.' in sent[index-1]:
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
    prep = ['в', 'во', 'имени']
    if sent[index-1] in alf:
        a2 = proverkaNicks(sent, index, d)
        if a2 == 'Non':
            a1 = adding(sent, d, Name)
    elif endsent(sent[index-1]) == 'End':
        a2 = proverkaNicks(sent, index, d)
        if a2 == 'Non':
            a1 = adding(sent, d, Name)
##    elif 'имени' in sent[index-1]:
##        return 'nope'
    else:
        return 'Not'
    return d

def points(sent, index, alf, d, Name, s8):
    if sent[index+1] in alf:
        a2 = proverkaNicks(sent, index, d)
        if a2 == 'Non':
            a1 = adding(sent, d, Name)
    elif "=CONJ" in sent[index+1]:
        a2 = proverkaNicks(sent, index, d)
        if a2 == 'Non':
            a1 = adding(sent, d, Name)
    elif startsent(sent[index+1]) == 'Start':
        a2 = proverkaNicks(sent, index, d)
        if a2 == 'Non':
            a1 = adding(sent, d, Name)
    elif '=S,' in sent[index+1]:
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
    prep = ['в', 'во', 'имени', 'им.', 'ул', 'пл.', 'пр-т', 'орден', 'музей', 'пр.']
    if name in word1:
        if 'фам' in word1:
            if endsent(word1) == 'End':
                if sent[index-1].split('{')[0] in prep:
                    s8.append(sent)
                else:
                    a2 = proverkaNicks(sent, index, d)
                    if a2 == 'Non':
                       a1 = adding(sent, d, Name)
            elif index != len(sent)-1:
                if sent[index-1].split('{')[0] in prep:
                    s8.append(sent)
                else:
                    a0 = start(sent, index, alf, d, Name)
                    if a0 == 'Not':
                      a1 = points(sent, index, alf, d, Name, s8)                  
            elif '=S,' in sent[index+1]:
                if 'фам' in sent[index+1]:
                    a2 = proverkaNicks(sent, index, d)
                    if a2 == 'Non':
                        a1 = adding(sent, d, Name)
                else:
                    s8.append(sent) # - для ручной проверки
            else:
                a2 = proverkaNicks(sent, index, d)
                if a2 == 'Non':
                    a1 = adding(sent, d, Name)
    return d 
    
def context(a1):
    d = {} # {id : {surname}}
    s8 = []
    for i in a1:
        if i != '':
            i2 = re.sub('\xa0', ' ', i)
            sent = i2.split(' ')
            a3 = sent[1].split('{')
            a5 = re.findall('{' + a3[0] + '\??=S', i2)
            name = a3[0]
            if len(a5) == 1:
                s8.append(sent)
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
    return d

def final_test(d):
    names = open_names('list_persons')
    d2 = {}
    for idd in d:
        for name in d[idd]:
            if name in names:
                if idd in d2:
                   d2[idd].add(name)
                else:
                   d2[idd] = set()
                   d2[idd].add(name)
            else:
                continue
    return d2
    

## структура таблицы insert into Tages values ("id", "id Text", "Name")
## 'insert into Tages values ("' + str(idd) + '", "' + l + '", "' + i + '")' + '\n'

def inserts(d2):
    values = []
    num = 0
    number = 1
    for i in d2:
        num += len(d2[i])
    f = open('Inserts_Names.txt', 'a', encoding = 'utf-8')
    while number <= num:
        for key in d2:
            for value in d2[key]:
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

@profile
def final():
    a1 = opening()
    a3 = context(a1)
    s1 = final_test(a3)
    a4 = inserts(s1)
    a5 = numbers(a4)
    print(time.clock())
    return

if __name__=='__main__':
    final()
    tracemalloc.start() 
