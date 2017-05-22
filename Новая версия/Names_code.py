import urllib.request
import re
from collections import Counter
import os
import pymorphy2
import time
from memory_profiler import profile

# структура таблицы insert into Tages values ("id", "Name", "Text", *"id текста")

def newdirs1():
    z = ['input_texts', 'output_texts']
    for i in z:
        if os.path.exists(i):
            True
        else:
            os.makedirs(i)
    return

def finding_text(text): # - достаю текст и id
    reg = '"([0-9]+?)","[0-9]{1,3}","((:?.|\\n|\\t)+?)","[0-9]{4}-[0-1][0-9]-[0-3][0-9]","[0-9]{4}-[0-1][0-9]-[0-3][0-9]","[0-9]","[0-9]","[0-9]+?","[0-9]+?","[0-9]+?"'
    a0 = re.findall(reg, text)
    a1 = {}
    for i in a0:
        line = re.sub('\\n', ' ', i[1])
        a1[i[0]] = line
    return a1

def work_with_text(): # - открываю записи/ нахожу текст
    f = open('notes.csv', 'r', encoding = 'utf-8')
    string = f.read()
    f.close
    list_text = finding_text(string) # -  массив всех текстов
    return list_text


# Фамилии могут изменяться по падежам по-разному, поэтому должны быть разные регулярные выражения

def open_names(name): # - все фамилии 
    f = open(name + '.txt', 'r', encoding = 'utf-8')
    array = f.read()
    f.close()
    massiv = re.findall('(.*?)\t', array)
    return massiv

def ending(forms, line, name, notes):
    for i in forms:
        if i == forms[0]:
            if len(forms) == 1:
                line = line + i[:3] + '(?:' + i[3:] + ')\\b|'
            else:
                line = line + i[:3] + '(?:' + i[3:] + '|'
        elif i == forms[-1]:
            if name == notes[-1]:
                line = line + i[3:] + ')\\b'
            else:
                line = line + i[3:] + ')\\b' + '|'
        else:
            line = line + i[3:] + '|'
    return line

def capital(word):  # - проверяем пишется ли слово с заглавной буквы
    alf = 'ЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ'
    if word[0] in alf:
        return 'Cap'
    else:
        return 'Not cap'

def form(morph, name): 
    forms = []
    p = morph.parse(name)[0]
    for form in p.lexeme:
        y = capital(name)
        if y == 'Cap':
            form_cap = (form.word[0]).upper() + form.word[1:]
            if form_cap in forms:
                continue
            else:
                forms.append(form_cap)
        else:
            if form.word in forms:
                continue
            
            else:
                forms.append(form.word)
    return forms #  - формы одного слова 

def special_ending(word, words, forms, line, name, notes): # если слово состоит из 2 частей
    if word== words[0]:
        for i in forms:
            if i == forms[0]:
                if len(forms) == 1:
                    line = line + i[:3] + '(?:' + i[3:] + ')\\b|'
                else:
                    line = line + i[:3] + '(?:' + i[3:] + '|'
            elif i == forms[-1]:
                line = line + i[3:] + ') '
            else:
                line = line + i[3:] + '|'
    else:
        line = ending(forms, line, name, notes)
    return line


def regex(morph):
    names = open_names('list_persons')
    line = ''
    for name in names:
        if ' ' in name: # - проверяю, если слово состоит из двух частей
            line2 = ''
            words = name.split(' ')
            for word in words:
                frm = form(morph, word) #  - формы одного слова
                line2 = special_ending(word, words, frm, line2, name, names)
            line = line + line2
        else:
            frm = form(morph, name)
            line = ending(frm, line, name, names)
    return line


def actual(pip, morph): # - восстанавливаю первоначальную форму 
    all_names = set()
    for name in pip:
        p = morph.parse(name)[0]
        all_names.add(p.normal_form)
    return all_names


def searching(list_text, reg, morph): # - поиск в текстах
    f = open('input_texts/rouge.txt', 'a', encoding = 'utf-8')
    pattern = re.compile(reg)
    for idd in list_text:
        text = list_text[idd]
        pip = pattern.findall(text)
        if pip!=[]:
            find = actual(pip, morph) # = set
            for person in find:
                f.write('\t'+ idd + ' ' + person + ' ' + text)
        print('Done for 1')
    f.close()
    return

def mystem():
    inp = "input_texts"
    lst = os.listdir(inp)
    for fl in lst:
        os.system(r"/Users/Stoneberry/Desktop/курсач/mystem " + inp + os.sep + fl + " output_texts" + os.sep + fl + " -cid")
    return

@profile              
def final():
    s0 = newdirs1()
    a1 = work_with_text()
    morph = pymorphy2.MorphAnalyzer()
    a2 = regex(morph)
    a3 = searching(a1, a2, morph)
    s7 = mystem()
    print(time.clock())
    return

if __name__=='__main__':
    final()
    tracemalloc.start()
    
