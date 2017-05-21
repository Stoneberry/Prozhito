# пытаюсь создать нормальный список фамилий

import urllib.request
import re
import time
from memory_profiler import profile

def new_file(filename, list_smth,): # - запись в файл
    f = open(filename + '.txt', 'a', encoding = 'utf-8')
    for i in list_smth:
        f.write(i + '\t')
    f.close()
    return

def reg_for_person1(html, mnoj_person): # - достаю фамилии 
    reg = '<td align="center"><a href=".*?" title="(.*?), .*?">.*?</a></td>'
    a1 = re.findall(reg, html)
    for i in a1:
        a2 = i.split(' ')
        if ':' in a2[0]:
            break
        else:
            mnoj_person.add(a2[0])
    return mnoj_person

def reg_for_person2(html, mnoj_person):
    reg = '<strong>(.*?)(?:\\n.*?)?' + '</strong>'
    a1 = re.findall(reg, html)
    for i in a1:
        surname = re.sub('\r', '', i)
        if surname != 'f.':
            if surname!= '':
                mnoj_person.add(surname)
    return mnoj_person

def reg_for_person3(html, mnoj_person):
    reg = '<p><b>(.*?)</b>'
    a1 = re.findall(reg, html)
    for name in a1:
        nm = name.split(' ')
        mnoj_person.add(nm[0])
    return mnoj_person

##def reg_for_person4():
##    req = urllib.request.Request('http://www.hi-edu.ru/e-books/xbook144/01/part-008.htm')
##    with urllib.request.urlopen(req) as response:
##        html = response.read().decode('utf-8')
##        reg = 'alt="(.*?)" /></a>'
##        a1 = re.findall(reg, html)
##        for i in a1:
##            print(i)
##    return

##def all_surnames(mnoj_person1, mnoj_person2):
##    surnames = set()
##    for i in mnoj_person1:
##        surnames.add(i)
##    for l in mnoj_person2:
##        surnames.add(l)
##    return surnames
##    
def load():
    links = ['https://ru.wikipedia.org/wiki/100_%D1%81%D0%B0%D0%BC%D1%8B%D1%85_%D0%B2%D0%BB%D0%B8%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9_%D0%B2_%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8', 'http://testcons.ru/%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%B4%D0%B5%D1%8F%D1%82%D0%B5%D0%BB%D0%B8-%D0%BD%D0%B0%D1%83%D0%BA%D0%B8-%D0%B8-%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D1%83/', 'http://www.examen.ru/add/manual/school-subjects/social-sciences/history/istoricheskie-deyateli/istoricheskie-deyateli-rossii/voennyie-deyateli-perioda-grazhdanskoj-i-velikoj-otechestvennoj-vojn', 'http://www.examen.ru/add/manual/school-subjects/social-sciences/history/istoricheskie-deyateli/istoricheskie-deyateli-rossii/politicheskie-i-gosudarstvennyie-deyateli-sssr']
    mnoj_person = set()
    for link in links:
        req = urllib.request.Request(link)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            if link == links[0]:
                mnoj = reg_for_person1(html, mnoj_person)
            elif link == links[1]:
                mnoj = reg_for_person3(html, mnoj_person)
            else:
                mnoj = reg_for_person2(html, mnoj_person)
    return mnoj_person

def open_nicknames():
    nicks = ['Nicknames_Stalin.txt', 'Nicknames_Lenin.txt', 'Nicknames_Hitler.txt']
    for i in nicks:
        f = open(i, 'r', encoding = 'utf-8')
        strings = f.read()
        pip = re.findall('(.*?)\t', strings)
        s1 = new_file('list_persons', pip)
    return

@profile
def final():
    a0 = load()
    s1 = new_file('list_persons', a0)
    s2 = open_nicknames()
    print(time.clock())
    return

if __name__=='__main__':
    final()
    
    
