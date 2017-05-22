# Prozhito

<b>"Прожито"</b> - это огромная база оцифрованных текстов из личных дневников, датированных XVIII - XX веками, в которой можно найти все записи за определённую дату. Темой курсовой является автоматическая разметка дневников проекта, а именно присваивание текстам тэгов с именами упоминаемых в них личностей.

Окончательный код программы лежит в папке "Новая версия". 

<b>Содежание папка:</b>
1) Код программы (Creating_list_of_persons.py, Names_code.py, Inserts_Names.py).
2) Список фамилий и кличек, по которым производился поиск (list_persons.txt, Nicknames_Hitler.txt, Nicknames_Stalin.txt, Nicknames_Lenin.txt).
3) Список инсертов для базы данных проекта (Inserts_Names.txt).
4) Частотность употребления фамилий (измеряется в кол-ве тектов, в которых фамилия встретилась)


<b>Код программы состоит из трех частей, каждая из который реализует одну из задач:</b>
1) Формирование списков - <b>Creating_list_of_persons.py</b>
2) Поиск фамилий в тексте - <b>Names_code.py</b>
3) Создание тегов для базы данных. - <b>Inserts_Names.py</b>

Рассмотрим каждый часть по отдельности: 

<b>Creating_list_of_persons.py</b>

Данная часть кода отвечает за автоматическое создание списков фамилий, по которым в дальнейшем будет осуществляться поиск. 
Информация бралась со следующих сайтов: 

1) Википедия -  100 самых влиятельных людей в истории
https://ru.wikipedia.org/wiki/100_%D1%81%D0%B0%D0%BC%D1%8B%D1%85_%D0%B2%D0%BB%D0%B8%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9_%D0%B2_%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8

2) Российский тестовый консорциум - ИСТОРИЯ РОССИИ: ДЕЯТЕЛИ НАУКИ И КУЛЬТУРЫ, ОБЩЕСТВЕННЫЕ ДЕЯТЕЛИ РОССИИ
http://testcons.ru/%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%B4%D0%B5%D1%8F%D1%82%D0%B5%D0%BB%D0%B8-%D0%BD%D0%B0%D1%83%D0%BA%D0%B8-%D0%B8-%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D1%83/

3) Экзамен.ru - Военные деятели периода Гражданской и Великой Отечественной войн
http://www.examen.ru/add/manual/school-subjects/social-sciences/history/istoricheskie-deyateli/istoricheskie-deyateli-rossii/voennyie-deyateli-perioda-grazhdanskoj-i-velikoj-otechestvennoj-vojn

4) Экзамен.ru - Политические и государственные деятели СССР
http://www.examen.ru/add/manual/school-subjects/social-sciences/history/istoricheskie-deyateli/istoricheskie-deyateli-rossii/politicheskie-i-gosudarstvennyie-deyateli-sssr


Фунуция load() скачивает страницы перечисленных статей и с помощью регулярных выражений достает фамилии. Для каждого сайта написаны индивидуальные регулярные выражения, за которые отвечают соотвествующие функции: reg_for_person1, reg_for_person2, reg_for_perso3. Сслыки сайтов хранятся в массиве, функция по очереди берет одну из них и в соответсвии с порядковым номером подбирает регулярное выражение. 

def load():
    links =['https://ru.wikipedia.org/wiki/100_%D1%81%D0%B0%D0%BC%D1%8B%D1%85_%D0%B2%D0%BB%D0%B8%D1%8F%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D1%85_%D0%BB%D1%8E%D0%B4%D0%B5%D0%B9_%D0%B2_%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D0%B8', 'http://testcons.ru/%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F-%D1%80%D0%BE%D1%81%D1%81%D0%B8%D0%B8-%D0%B4%D0%B5%D1%8F%D1%82%D0%B5%D0%BB%D0%B8-%D0%BD%D0%B0%D1%83%D0%BA%D0%B8-%D0%B8-%D0%BA%D1%83%D0%BB%D1%8C%D1%82%D1%83/', 'http://www.examen.ru/add/manual/school-subjects/social-sciences/history/istoricheskie-deyateli/istoricheskie-deyateli-rossii/voennyie-deyateli-perioda-grazhdanskoj-i-velikoj-otechestvennoj-vojn', 'http://www.examen.ru/add/manual/school-subjects/social-sciences/history/istoricheskie-deyateli/istoricheskie-deyateli-rossii/politicheskie-i-gosudarstvennyie-deyateli-sssr']
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

Все полученные фамилии записываются во множество, чтобы избежать повторений, и записываются в файл с помощью функции new_file, которая на вход получает будущее название файла и содержание файла(В данном случае это множество фамилий).






