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

                        Creating_list_of_persons.py

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


Фунуция load() скачивает страницы перечисленных статей и с помощью регулярных выражений достает фамилии. Для каждого сайта написаны индивидуальные регулярные выражения, за которые отвечают соотвествующие функции: reg_for_person1, reg_for_person2, reg_for_person3. Сслыки сайтов хранятся в массиве, функция по очереди берет одну из них и в соответсвии с порядковым номером подбирает регулярное выражение. 

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

Все полученные фамилии записываются во множество, чтобы избежать повторений, и записываются в файл с помощью функции new_file, которая на вход получает будущее название файла и содержание файла(В данном случае это множество фамилий). Клички, которые ранее были записаны в файлы (название файла соответсвует настоящей фамилии личности), так же добавляются к общему списку. 

                
                        Names_code.py
Данная часть кода создает регулярное выражение и ищет все совпадения с ним в текстах.
С помощью регулярного выражения программа достает все записи из файла, который был заранее выкачен из базы данных Прожито. Каждая запись записывается в словарь, где ключем является id текста, а значением сам текст (функция work_with_text).

Функиция  regex - далее из созданного файла из предыдущей части кода достаются фамилии и для каждой из них с помощью pymorphy2 генерируются формы слова (функция form) и соединяются в единое регулярное выражение (line). Регулярное выражение  состоит из частей, которые создаются по отдельности, а потом соединяются в одну строчку. Каждая часть представляет собой фамилию с набором окончаний для всех существующих для нее форм и специального разделителя «|», который отделяет одну фамилию от другой. 
Чтобы не перечислять через разделитель все словоформы, фамилия делится на две части «основу» и «окончание» (функция ending). Основой считается первые три буквы слова, а окончанием - оставшиеся. Так как pymorphy2 автоматически приводит все слова к нижнему регистру, то программа восстанавливает заглавную букву, в том случае, если слово с таковой писалось (функция capital).  Если слово  состоит из нескольких частей, например, кличка Иосифа Сталина «Дядя Джо», то разбор производится для каждой составляющей по отдельности, а потом соединяются во едино и добавляется к общему регулярному выражению (функция special_ending). Pymorphy2 не всегда верно определяет формы слов, поэтому для некоторых из них окончания были прописаны вручную (функция normal_ending). 

{
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "from pymystem3 import Mystem\n",
    "import pymorphy2"
   ]
  }
...
special = ['Рыков', 'Кампрад', 'Рудзутак', 'Брэнсон', 'Брин', 'Каменев', 'Теллер', 'Фридан', 'Горбачёв', 'Найт', 'Дьюар', 'Бик', 'Клаузевиц', 'Бах', 'Булгаиин', 'Белл', 'Делл', 'Баффетт', 'Лютер', 'Зворыкин', 'Бентам', 'Диор', 'Эттингер']
...
"if name in specials:\n"
"     line = normal_ending(name, line, names)\n"
 ...
 
 
def normal_ending(normal, surname, massiv_surnames_normal):
	if normal.endswith('народов'):
		a1 = normal.split(' ')
		name2 = a1[0][:2] + '(?:ец|ца|цу|цом|це|цы|цов|цах|цами|цам) ' + a1[1] + '\\b' + '|'
		surname = surname + name2
	elif normal.endswith('Виссарионович'):
		a1 = normal.split(' ')
        name2 = a1[0] + '(?:\\b|а|у|ом|е|ов|ы|ам|ами|ах) ' + a1[1] + '(?:\\b|а|у|ом|е|ов|ы|ам|ами|ах)' + '\\b' + '|'
        surname = surname + name2
    elif normal == massiv_surnames_normal[-1]:
        name2 = normal + '(?:\\b|а|у|ом|е|ов|ы|ам|ами|ах)' + '\\b'
        surname = surname + name2
    else:
        name2 = normal + '(?:\\b|а|у|ом|е|ов|ы|ам|ами|ах)' + '\\b' + '|'
        surname = surname + name2
    return surname
    
 Когда регулярное выражение готово, по очереди берется каждая запись из базы данных и с помощью регулярного выражения находятся совпадения (функция searching). На выходе для каждой такой записи получается массив, в котором перечислены найденные фамилии. Все эти вхождения могут быть в разных падежах и числах, что не подходит для записи в качестве тега.  Поэтому с помощью pymorphy2 восстанавливаются «нормальные формы», то есть к форме именительного падежа единственного числа, получившийся результат записывается во множество (функция actual).    
    
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
    
Каждое такое вхождение записывается в новый файл в следующем виде: сначала идет id записи, далее фамилия личности (предполагаемый тег) и сам текст записи.  Если в тексте встретилось несколько фамилий, то для каждой из них создается отдельная строка, по уже заданной модели. Этот файл помещается в заранее созданную папку (функция newdirs), из которой программа Mystem достает его и производит морфологический разбор, помещает результат в папку (функция mystem). На этом вторая часть кода завершает работу.



                       Inserts.py
Третья часть занимается решением проблемы омонимии и непосредственное создание тегов для базы данных. Основной идеей для решения такой проблемы было  посмотреть на контекст, в котором упоминается фамилия.

Функция opening достает из разобранного с помощью MyStem файла записи, в которых нашлись фамилии. Каждая такая запись в функции searching делится по пробелам на слова. Затем программа проверяет сколько раз встретилась фамилия, которая записана после id текста (включая саму эту фамилию, которую дальше будет именоваться как экземпляр). В зависимости от того, насколько часто встретилось слово в записи, применялись разные условия проверки.

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

Если фамилия встретилась всего один раз, это значит, что в самом разборе текста записи не встретилось точного соответствия заданному экземпляру. Проблема в том, что MyStem и pymorphy2 не всегда верно производят морфологический разбор для некоторых фамилий, поэтому данные случаи отсеиваются. 

Функция proverka2 - Если в разборе фамилия встретилась два раза - в тексте она была упомянута один раз. Как раз в таких предложениях могут возникнуть проблемы с омонимией. Так как в одной записи может быть несколько предложений, программа сначала проверяет, не является ли фамилия в нем последним словом, смотря на наличие или отсутствие знака препинания. Если слово удовлетворяет условию, то оно записывается в словарь, ключом в котором является id текста, а значением  - множество фамилий. Если же нет, то проверяем на наличие знаков в предыдущем за фамилией слове. В случае, когда первые условия оказались отрицательными, проверяем, есть ли существительное в следующем слове. Если следом идет фамилия, то скорее всего омонимии никакой не будет, поэтому добавляем в словарь, в обратном случае предложение добавляется в специальный массив, который при желании можно будет  распечатать и проверить каждую запись на наличие омонимии вручную. При этом в каждом таком условии экземпляр проверяется на соответствие какой-либо кличке или прозвищу, чтобы в качестве тега записать не саму кличку, а фамилию личности, которому она соответствует. Так же проверяется, если слово перед фамилией является одним из следующих слов: ['в', 'во', 'имени', 'им.', 'ул', 'пл.', 'пр-т', 'орден', 'музей', 'пр.'], чтобы избежать таких вхождений как "орден Ленина" или "завод имени Ленина". 

Упоминание фамилии более двух раз я посчитала достаточным условием для того, чтобы присвоить записи тег, так как частотность одной и той же словоформы в одном отрывке может свидетельствовать об употреблении нужного для нас значения.
	
При автоматическом определении форм слова нельзя исключать вероятность ошибки, поэтому в качестве финальной проверки программа смотрит на соответствие предполагаемых тегов реальным фамилиям людей из нашего списка. Если результат положительный, то формирование списка тегов считается законченным (функция final_test).
    
Для добавления получившейся информации в базу данных проекта, программа создает файл, в котором для каждого ключа словаря и для каждого его значения создается строчка, имеющая следующий вид «insert into Tages values ("id", "id Text", «Name»)», где id - id самого тега,  id Text - id текста, а Name - это название тега (функция inserts). Данный файл можно найти в папке "Новая версия". 

