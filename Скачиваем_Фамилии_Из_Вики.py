import urllib.request
import re

def new_file(list_smth): # - запись в файл
    f = open('list_persons.txt', 'a', encoding = 'utf-8')
    for i in list_smth:
        f.write(i + ' ')
    f.close()
    return

def reg_for_person(html): # - достаю фамилии 
    reg = 'title="(.*?)">.*?</a></li>'
    a1 = re.findall(reg, html)
    mnoj_person = set()
    for i in a1:
        a2 = i.split(' ')
        if ':' in a2[0]:
            break
        else:
            mnoj_person.add(a2[0])
    return mnoj_person

def load_person(): # - скачиваю страницы со списком персоналий
    alf = "АБВГДЕЖЗИКЛМНЛОПРСТУФХЦЧШЩЭЮЯ"
    for i in alf:
        req = urllib.request.Request('https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%BB%D0%B8%D0%B8_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=' + urllib.request.quote(i))
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            a2 = reg_for_person(html)
            a3 = new_file(a2)
    return

if __name__=='__main__':
   load_person()
