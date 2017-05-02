# пытаюсь создать нормальный список фамилий

import urllib.request
import re

def new_file(list_smth, filename): # - запись в файл
    f = open(filename + '.txt', 'a', encoding = 'utf-8')
    for i in list_smth:
        f.write(i + '\t')
    f.close()
    return

def reg_for_person(html): # - достаю фамилии 
    reg = '<td align="center"><a href=".*?" title="(.*?), .*?">.*?</a></td>'
    a1 = re.findall(reg, html)
    mnoj_person1 = set()
    for i in a1:
        a2 = i.split(' ')
        if ':' in a2[0]:
            break
        else:
            mnoj_person1.add(a2[0])
    return mnoj_person1

def reg_for_person2(html):
    reg = '<strong>(.*?)(?:\\n.*?)?' + '</strong>'
    a1 = re.findall(reg, html)
    mnoj_person2 = set()
    for i in a1:
        surname = re.sub('\r', '', i)
        if surname != 'f.':
            if surname!= '':
                mnoj_person2.add(surname)
    return mnoj_person2


##def reg_for_person3(html):
##    reg = ';">(.*?)</div>'
##    a1 = re.findall(reg, html)
##    mnoj_person3 = set()
##    for name in a1:
##        if name == 'Другие красочные эпитеты':
##            continue
##        else:
##            mnoj_person3.add(name)
##    mnoj_person3.add('Джугашвили')
##    mnoj_person3.add('Иосиф Виссарионович')
##    return mnoj_person3

def all_surnames(mnoj_person1, mnoj_person2):
    surnames = set()
    for i in mnoj_person1:
        surnames.add(i)
    for l in mnoj_person2:
        surnames.add(l)
    return surnames
    
def separate(surnames):
    normal = []  # - изменение по падежам нормальное(прибавление к основе окончания)
 #   speсial = [] # - изменение по падежам особенное 
    alf1 = 'нтрсглдцмвкфшбжзпхч'
    for name in surnames:
        for i in alf1:
            if name.endswith(i):
                normal.append(name)
            else:
                continue
    for l in normal:
        surnames.discard(l)
    a1 = new_file(normal, 'list_persons_normal')
    a2 = new_file(surnames, 'list_persons_special')
    return

def load_person1(): # - скачиваю страницы со списком персоналий
    req = urllib.request.Request('https://ru.wikipedia.org/wiki/100_%D1%81%D0%B0%D0%BC%D1%8B%D1%85_%D0%B2%D0%BB%D0%B8%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9_%D0%B2_%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        a2 = reg_for_person(html)
    return a2

def load_person2(): # -  деятели СССР
    links = ['http://www.examen.ru/add/manual/school-subjects/social-sciences/history/istoricheskie-deyateli/istoricheskie-deyateli-rossii/voennyie-deyateli-perioda-grazhdanskoj-i-velikoj-otechestvennoj-vojn', 'http://www.examen.ru/add/manual/school-subjects/social-sciences/history/istoricheskie-deyateli/istoricheskie-deyateli-rossii/politicheskie-i-gosudarstvennyie-deyateli-sssr']
    for link in links:
        req = urllib.request.Request(link)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            a2 = reg_for_person2(html)
    return a2

def open_nicknames():
    nicks = ['Nicknames_Stalin.txt', 'Nicknames_Lenin.txt', 'Nicknames_Hitler.txt']
    for i in nicks:
        f = open(i, 'r', encoding = 'utf-8')
        strings = f.read()
        pip = re.findall('(.*?)\t', strings)
        a0 =set()
        for i in pip:
            a0.add(i)
        a1 = separate(a0)
    return

##def load_person3():
##    links = ['https://rg.ru/2013/09/24/imena-site.html'] #  - клички Сталина 
##    req = urllib.request.Request(link)
##    with urllib.request.urlopen(req) as response:
##        html = response.read().decode('utf-8')
##        a2 = reg_for_person3(html)
##    return a2

## names = ['Владимир Ильич', 'Ульянов', 'Вождь мирового пролетариата']
def final():
    a0 = load_person1()
    a1 = load_person2()
    s0 = all_surnames(a0, a1)
    s1 = separate(s0)
    s2 = open_nicknames()
    return

if __name__=='__main__':
    final()
    
