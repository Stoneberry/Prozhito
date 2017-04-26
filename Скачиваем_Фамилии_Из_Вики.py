# пытаюсь создать нормальный список фамилий

import urllib.request
import re

def new_file(list_smth, filename): # - запись в файл
    f = open(filename + '.txt', 'a', encoding = 'utf-8')
    for i in list_smth:
        f.write(i + ' ')
    f.close()
    return

def reg_for_person(html): # - достаю фамилии 
    reg = '<td align="center"><a href=".*?" title="(.*?), .*?">.*?</a></td>'
    a1 = re.findall(reg, html)
    mnoj_person = set()
    for i in a1:
        a2 = i.split(' ')
        if ':' in a2[0]:
            break
        else:
            mnoj_person.add(a2[0])
    return mnoj_person

def separate(mnoj_person):
    normal = []  # - изменение по падежам нормальное(прибавление к основе окончания)
    speсial = [] # - изменение по падежам особенное 
    alf1 = 'нтрсглдцмвкфшбжзпхч'
    for name in mnoj_person:
        for i in alf1:
            if name.endswith(i):
                normal.append(name)
            else:
                continue
    for l in normal:
        mnoj_person.discard(l)
    a1 = new_file(normal, 'list_persons_normal')
    a2 = new_file(mnoj_person, 'list_persons_special')
    return

def load_person(): # - скачиваю страницы со списком персоналий
    req = urllib.request.Request('https://ru.wikipedia.org/wiki/100_%D1%81%D0%B0%D0%BC%D1%8B%D1%85_%D0%B2%D0%BB%D0%B8%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9_%D0%B2_%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        a2 = reg_for_person(html)
        a3 = separate(a2)
    return

def final():
    a0 = load_person()
    return


if __name__=='__main__':
    final()
    
