# if index < len(list_sportsmen): убрать этот тупняк не нужный 262 строка и рядом выше/ниже
# упразднить среднюю скорость в группах, она вроде как не нужна, для подсчета места в группе используется инфа из общей
# статистики по спортсменам. Убрать из бд в группах AvgSpeed и здесь все запросы поправить и в php

import eel
import os
import datetime
import copy
# import re
import regex
import configparser
import pymysql
from bs4 import BeautifulSoup
from combination import combi


@eel.expose
def read_doc(address):
    file_date = str(address)[0:4] + "-" + str(address)[4:6] + "-" + str(address)[6:8]
    """ считываем полученный файл протокола соревнований для парсинга"""
    with open(address, "r", encoding='utf-8') as f:
        try:
            soup = f.read()
            content = BeautifulSoup(soup, 'lxml')
            # определяем ужный скрипт с помощью регулярных выражений re по части нужного текста
            # script = content.find("script", text=re.compile('var race')).contents
            script = content.find_all("script")
            a = str(script[1].contents)  # берем второй тег скрипт и переводим его в текстовый формат
            a = a[a.find("var race"):a.find("}};") - 1]  # обрезаем скрипт, где хранятся все данные протокола
            # функция парсинга, если успешная то 1, если 2 то файл уже был ранее закачен, если 3 то ошибка файла
            return parsing(a)
        finally:
            f.close()


@eel.expose
def connect_db(h, u, p, d):
    db_data.append(h)
    db_data.append(u)
    db_data.append(p)
    db_data.append(d)
    """ Connect to MySQL database """
    try:
        con = pymysql.connect(host=h,
                              user=u,
                              password=p,
                              db=d)
        if con.cursor().connection.open:
            return True

    except pymysql.Error as e:
        print(e)
        return False

    finally:
        con.close()


def parsing(a):
    flag_ident = False  # флаг идентичности, если файл уже с подобными данными загружался выдаем ошибку
    girl_name = girlName()  # получаем из файла список женских имен
    # имена как женские так и мужские, для доп проверки. пишем с маленькой чтобы привести к общему виду
    name_werewolf = ("саша", "женя", "вася", "слава", "валя")  # может Никиту проверить?хотя таких женских имен унас нет
    name_bad = ("ада", "аля", "настя", "аня", "тоня", "лера", "варя", "вика", "галя", "гуля", "даша", "дуня", "дуся",
                "катя", "лена", "лиза", "зина", "ира", "ксюша", "лара", "люба", "люда", "рита", "маша", "надя",
                "наташа", "оля", "поля", "рая", "света", "соня", "тася", "таня", "тома", "уля", "эля", "юля")
    name_group = ["Ветераны М", "Ветераны Ж", "Взрослые Ж", "Взрослые М", "Дети Ж", "Дети М", "Подростки Ж",
                  "Подростки М", "Элита Ж", "Элита М"]
    statistics_starts = {}  # статистика старта для передачи в бд
    count_finished = 0  # количество участвующих в старте
    list_sportsmen = []  # список всех спортсменов в нем лежат dict_sportsmen
    dict_sportsmen = {}  # словарь с данными спорстмена на стартах и его результатами
    length_segment = []  # словарь с длинами перегонов всех дистанциий для определения самого короткого и длинного\
    speed_null = 0  # количество участников не прошедших ни одного перегона (для подсчета средней скорости на старте)
    avg_speed = 0  # для подсчета скоростей всех участников
    list_split = []  # список всех сплитов по id
    split_best = [9999999999, 0]
    split_first_best = [9999999999, 0]
    first_split = []
    list_var = [a[a.find("courses") - 1:a.find("data") - 1].split('\"Course\"'),  # Дистанции
                # разделяем по слову Course, т.к. не знаем кол-во частей последнюю часть при будущем чтении не берем
                a[a.find("data") - 1:a.find("groups") - 1],  # данные события
                a[a.find("groups") - 1:a.find("organizations") - 1].split("start_interval"),  # характеристики группы
                a[a.find("persons") - 1:a.find("results") - 1].split("}"),  # личные данные спортсменов заявленных
                a[a.find("results") - 1:a.find("settings") - 1].split("system_type")]  # результаты спортсменов

    # собираем все длины перегонов старта для статистики самого короткого и длинного перегона
    for i in list_var[0]:
        xz = i.split('\"CourseControl\"')  # делим дстанцию на отрезки с перегонами
        for jndex, j in enumerate(xz):
            if jndex < len(xz) - 1:
                ls = int(j[j.find("length") + 9: j.find("object") - 3])  #длина одного перегона
                if ls > 0:  # если 0, то дистанция корявая или может быть был выбор и так составили дистанцию
                    length_segment.append(ls)  # добавляем длину перегона в общий список
    length_segment.sort()
    statistics_starts["small_length_segment"] = length_segment[0]
    statistics_starts["large_length_segment"] = length_segment[-1]

    # Записываем title в словарь, заменяем экранированные символы для декодирования,
    # сначала кодируем в юникод, задем раскодируем с применением escape-последовательности

    if regex.search(r'\p{IsCyrillic}', list_var[1][list_var[1].find("title") + 9:list_var[1].find("url") - 4]):
        title = list_var[1][list_var[1].find("title") + 9:list_var[1].find("url") - 4]
    else:
        title = list_var[1][list_var[1].find("title") +
                            9:list_var[1].find("url") - 4].replace('\\\\', '\\').encode("utf-8").decode(
            "unicode-escape")

    if title != "":
        # statistics_starts["title"] = u"{}".format(title)
        statistics_starts["title"] = title
    else:
        statistics_starts["title"] = "Нет названия"

    # Записываем дату в словарь
    date = list_var[1][list_var[1].find("start_datetime") + 18:list_var[1].find("title") - 3]
    if date != "null":
        statistics_starts["date"] = date[0:10]
    else:
        statistics_starts["date"] = file_date

    # Записываем количество спортсменов во всех группах участвующих по группам(для подсчета очков) и общее значение
    for index, i in enumerate(list_var[2]):
        if index >= len(list_var[2]) - 1:
            statistics_starts["count_finished"] = count_finished
            break
        id = i[i.find("\"id\"") + 7:i.find("is_any_course") - 4]  # id группы
        statistics_starts[id] = int(i[i.find("count_finished") + 17:i.find("count_person") - 3])  # кол-во уч. в группе
        count_finished += statistics_starts[id]  # кол-во всех финишировавших пополняем

    # записываем названия и длины дистанций в словарь
    for index, i in enumerate(list_var[0]):
        if index < len(list_var[0]) - 1:
            length = int(i[i.find("id") + 66:i.find("name") - 3])
            # name = i[i.find("name") + 8:i.rfind("object") - 4]  # rfind() ищет последнее вхождение слова
            name = i[i.find("name") + 8:i.find("name") + 9]  # второй вариант для масстартов и прочего когда для группы несколько вариантов дистанций (А, А1) и берем только первую букву дистанции
            if name in 'ABCD':  # Проверка правильности написания дистанций
                statistics_starts[name] = length
            # else:
            #     return 2  # "Ошибка названия дистанций"

    # создаем данные финишировавших из результатов
    # + записываем сплиты в один большой список list_split
    for index, i in enumerate(list_var[4]):
        if index < len(list_var[4]) - 1:
            dict_sportsmen["person_id"] = i[i.find("person_id") + 13:i.find("place") - 4]
            dict_sportsmen["result"] = int(i[i.find("result_msec") + 14:i.find("result_relay") - 3])
            dict_sportsmen["place"] = int(i[i.find("place") + 8:i.find("\"result\"") - 2])
            dict_sportsmen["point"] = float(i[i.find("\"scores\"") + 10:i.find("speed") - 3])

            # работа со сплитами, считаем сплиты в ручную потому что после 60 минут на километр обнуляется и по новой считает минуты без часа
            xt = i[i.find("splits"):].split("\"time\"")  # разбитие результата спортсмена на сплиты
            for jndex, j in enumerate(xt):
                if jndex < len(xt) - 1:
                    # проверяем правильность взятия кп, если false то отметка на кп неправильная, скорость не записываем
                    if j[j.find("is_correct") + 13:j.find("leg_place") - 3] == "true":
                        g = int(j[j.find("leg_time") + 11:j.find("length_leg") - 3])  # время перегона
                        b = int(j[j.find("length_leg") + 13:j.find("object") - 3])  # длина перегона
                        if g == 0:  # случай когда участник восстановлен и у него неправильная отметка на сплите, но указано в файле что отметка true
                            continue
                        else:
                            z = (1000 / b) * g / 60000
                            # xt = (1000 / length) * time / 60000 ищем минуты на км
                            # y = (xt % 1) * 100 дробная часть от xt, сотые переводив в целые десятки
                            # z = 6 * y / 10 пропорционально высчитываем секунды 100/y = 60 секунд / z секунды
                            speed_split = int(z) * 60 + int(6 * ((z % 1) * 100) / 10)
                            # speed_split = int(j[j.find("speed") + 9:j.find("speed") + 11]) * 60 + \
                            #     int(j[j.find("speed") + 12:j.find("speed") + 14])  # время сплита
                            list_split.append(speed_split)

            if dict_sportsmen["place"] > 0:
                dict_sportsmen["speed"] = int(i[i.find("speed") + 9:i.find("splits") - 10]) * 60 + \
                                          int(i[i.find("speed") + 12:i.find("splits") - 7])
            else:  # берем скорость даже если снятие у участника, но только тех перегонов которые до снятия, если с первого перегона снялся (отметил не тот, а дальше все норм) он без скорости останется
                if len(i[i.find("\"result\"") + 11: i.find("result_msec") - 4]) != 8:  # Если не число(время), то значит сошел участник
                    if "count_dsq" in statistics_starts:  # Если еще ключ в словаре уже заведен добавляем +1
                        statistics_starts["count_dsq"] += 1  # кол-во сошедших участников
                    else:
                        statistics_starts["count_dsq"] = 1
                if len(list_split) > 0:
                    dict_sportsmen["speed"] = int(sum(list_split) / len(list_split))

                else:  # если нет сплитов ставим скорость 0
                    dict_sportsmen["speed"] = 0
                    speed_null += 1

            avg_speed += dict_sportsmen["speed"]

            if len(list_split) > 0:
                m = list_split[0]  # первый перегон сохраняем отдельно
                list_split = sorted(list_split)
                dict_sportsmen["splits"] = [m, list_split[0], list_split[-1]]  # первый перегон, самый быстрый и медленный сплит участника
                # dict_sportsmen["splits"] = copy.deepcopy(list_split)  # если нужны всесплиты, то расскоментировать
                list_split.clear()
            else:
                dict_sportsmen["splits"] = [-1, -1, -1]  # если сплитов нет ставим всем -1

            b = copy.deepcopy(dict_sportsmen)
            list_sportsmen.append(b)

    # добавляем данные финишировавших спортсменов из заявки
    # dict_sportsmen.clear()  # очищаем словарь чтобы новый не объявлять
    for index, i in enumerate(list_var[3]):
        if index < len(list_var[3]) - 1:
            for jndex, j in enumerate(list_sportsmen):
                if j["person_id"] == i[i.find("\"id\"") + 7:i.find("is_out") - 4]:

                    j["group_id"] = i[i.find("group_id") + 12:i.find("\"id\"") - 3]
                    if regex.search(r'\p{IsCyrillic}', i[i.find("name") + 8:i.find("national_code") - 4]):
                        j["name"] = i[i.find("name") + 8:i.find("national_code") - 4]
                    else:
                        j["name"] = i[i.find("name") + 8:i.find("national_code") - 4].replace('\\\\', '\\').encode(
                            "utf-8").decode(
                            "unicode-escape")
                    if j["name"].lower() in name_bad:
                        return 4  # найдено сокращенное имя
                    if regex.search(r'\p{IsCyrillic}', i[i.find("surname") + 11:i.find("world_code") - 4]):
                        j["surname"] = i[i.find("surname") + 11:i.find("world_code") - 4]
                    else:
                        j["surname"] = i[i.find("surname") + 11:i.find("world_code") - 4].replace('\\\\',
                                                                                                  '\\').encode(
                            "utf-8").decode(
                            "unicode-escape")

                    # записываем участник в вне конкурса или в конкурсе
                    # j["out_comp"] = i[i.find("is_out") + 24:i.find("is_paid") - 3]

                    # определяем пол спортсмена по его имени из файла и из кортежа женско-мужских имен
                    j["sex"] = 'М'
                    if j["name"].lower() in name_werewolf:
                        # if j["surname"][-1:] == "а":  # если последняя буква фамилии "а" то эта женщина
                        j["sex"] = 'Н'  # пол неопределен. будем выяснять позже
                        return 4  # траблы с именем
                    else:
                        if j["name"].lower() in girl_name:
                            j["sex"] = 'Ж'
                            if "count_women" in statistics_starts:
                                statistics_starts["count_women"] += 1
                            else:
                                statistics_starts["count_women"] = 1
                    year = i[i.find("birth_date") + 14:i.find("card_number") - 10]
                    if year == "":
                        j["year"] = 0
                    else:
                        j["year"] = int(year)
                    j["bib"] = i[i.find("bib") + 6:i.find("birth_date") - 3]  # номер участника. нужен для того чтобы при нестандартной ситуации с дистанциями под каждого участника по номеру определить какую дистанцию он бежал (название дистанции совпадет с его номером)

                    # c = statistics_starts[i[i.find("group_id") + 12:i.find("\"id\"") - 3]]
                    # если спортсмен не добежал/снялся у него в скрипте -1 и тогда считаем ему очков 0
                    # Так же есть те кто не стартовал. их надо удалять из протокола
                    # if j["place"] == -1:
                    #     j["point"] = 0
                    # else:
                    #     round - округление. округляем до двух знаков после запятой
                    #     j["point"] = round(100 - ((j["place"] - 1) * 100) / c, 2)

                    # проверяем участник в вне конкурса или в конкурсе, если вне конкурса удаляем его из зачета группы
                    if i[i.find("is_out") + 24:i.find("is_paid") - 3] == 'true':
                        del list_sportsmen[jndex]
                        if "out_of_comp" in statistics_starts:
                            statistics_starts["out_of_comp"] += 1
                        else:
                            statistics_starts["out_of_comp"] = 1
                    else:
                        if "out_of_comp" not in statistics_starts:
                            statistics_starts["out_of_comp"] = 0

    # добавляем id дистанции чтобы определить длину и название группы для выгрузки в бд
    for index, i in enumerate(list_var[2]):
        if index < len(list_var[2]) - 1:
            for j in list_sportsmen:
                if j["group_id"] == i[i.find("\"id\"") + 7:i.find("is_any_course") - 4]:
                    course_id = i[i.find("course_id") + 13:i.find("first_number") - 4]
                    if len(course_id) < 5:  # если айди дистанции короткий значит ситуация не стандартная с дистанциями под каждого участника, будем по номеру определять какую дистанцию он бежал (название дистанции совпадет с его номером)
                        j["course_id"] = j["bib"]
                    else:
                        j["course_id"] = course_id
                    if regex.search(r'\p{IsCyrillic}', i[i.find("\"name\"") + 9:i.find("object") - 4]):
                        j["group_name"] = i[i.find("\"name\"") + 9:i.find("object") - 4]
                    else:
                        j["group_name"] = i[i.find("\"name\"") + 9:i.find("object") - 4].replace('\\\\', '\\').encode(
                            "utf-8").decode(
                            "unicode-escape")
                    if j["group_name"] not in name_group:
                        return 5

    # добавляем к данным спортсменов их название длину дистанции
    for index, i in enumerate(list_var[0]):
        if index < len(list_var[0]) - 1:
            for j in list_sportsmen: # rfind() ищет последнее вхождение слова
                xm = i[i.find("\"id\"") + 7:i.rfind("length") - 4]  # айди данной дистанции
                xn = i[i.find("name") + 8:i.rfind("object") - 4]  # сохраняем название дистанции(номер участника), если дистанции были построены под каждого участника по его номеру
                if j["course_id"] == xm or j["course_id"] == xn:  # если по айди находим записываем по айди (стандартная ситуация заданки из 4 дистанция), если по названию нашли значит ситуация с дистанциями под участника
                    # j["distance_name"] = i[i.find("name") + 8:i.rfind(
                    #     "object") - 4]  # rfind() ищет последнее вхождение слова
                    j["length"] = int(i[i.find("id") + 66:i.find("name") - 3])

    """ Connect to MySQL database """
    con = pymysql.connect(host=db_data[0],
                          user=db_data[1],
                          password=db_data[2],
                          db=db_data[3])
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM statisticsstarts")
        rows = cur.fetchall()
        # datetime.date.fromisoformat() изменяет str формат на datetime
        for row in rows:
            if (statistics_starts["title"] in row) and \
                    (statistics_starts["date"] in row) and \
                    (statistics_starts["count_finished"] in row):
                flag_ident = True
                break

        # присваиваем id для спортсменов из бд
        cur.execute("SELECT * FROM sportsmen")
        sportsmen_id = cur.fetchone()
        if sportsmen_id is None:
            for index, i in enumerate(list_sportsmen):
                if index < len(list_sportsmen):
                    list_sportsmen[index]["sportsmen_id"] = index + 1
        else:
            cur.execute("SELECT * FROM sportsmen")
            rows = cur.fetchall()
            cur.execute("SELECT max(sportsmenId) FROM sportsmen")
            last_id = int(cur.fetchone()[0]) + 1  # последний id спортсмена в бд + 1 добавляем для следующего id
            for index, i in enumerate(list_sportsmen):
                if index < len(list_sportsmen):
                    for jndex, row in enumerate(rows):
                        if (list_sportsmen[index]["name"] in row) and \
                                (list_sportsmen[index]["surname"] in row) and \
                                (list_sportsmen[index]["year"] in row):
                            list_sportsmen[index]["sportsmen_id"] = int(row[0])
                            break

                        if jndex == len(rows) - 1:
                            list_sportsmen[index]["sportsmen_id"] = last_id
                            last_id += 1

        # Добавляем в статистику среднюю скорость на старте, лучшую скорость на перегоне, лучший первый перегон
        for i in list_sportsmen:  # вычисляем лучший перегон
            s = i.get("splits")
            if s[1] is not None and 0 < s[1] < split_best[0]:
                split_best[0] = s[1]
                split_best[1] = i["sportsmen_id"]
            if s[1] is not None and 0 < s[0] < split_first_best[0]:
                split_first_best[0] = s[0]
                split_first_best[1] = i["sportsmen_id"]

        statistics_starts["split_best"] = "{} {}".format(split_best[1], split_best[0])
        statistics_starts["split_first_best"] = "{} {}".format(split_first_best[1], split_first_best[0])

        # int_r функция округления по мат правилам в большую или меньшую сторону
        # мы считали все средние скорости всех участников даже у кого средняя 0 из-за снятия, но этих участников мы записывали в speed_null, в итоге скорость средняя всех кто имеет сплиты
        statistics_starts["avg_speed"] = int_r(avg_speed / (len(list_sportsmen) - speed_null))

        # Если файл не был ранее загружен выполняем загрузку
        if flag_ident is not True:
            cur.execute("SELECT max(startId) FROM statisticsstarts")
            start_id = cur.fetchone()
            if start_id[0] is not None:
                statistics_starts["start_id"] = int(start_id[0]) + 1
            else:
                statistics_starts["start_id"] = 1001

            # заполняем в таблицу бд statisticsstarts статистику стартов
            sql_statistics_starts = "INSERT INTO statisticsstarts (StartId, Title, Date, CountSportsmen, CountMen, CountWomen, CountDSQ, OutOfComp," \
                                    "LengthA, LengthB, LengthC, LengthD, small_length_segment, large_length_segment, avg_speed," \
                                    "split_best, split_first_best) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql_statistics_starts, (statistics_starts["start_id"], statistics_starts["title"],
                                                statistics_starts["date"], statistics_starts["count_finished"],
                                                statistics_starts["count_finished"] - statistics_starts["count_women"], statistics_starts["count_women"],
                                                statistics_starts["count_dsq"], statistics_starts["out_of_comp"], statistics_starts["A"],
                                                statistics_starts["B"], statistics_starts["C"], statistics_starts["D"],
                                                statistics_starts["small_length_segment"],
                                                statistics_starts["large_length_segment"], statistics_starts["avg_speed"],
                                                statistics_starts["split_best"], statistics_starts["split_first_best"]))

            # запросы на добавление новых строк спортсменов в соответствующих таблицах
            sql_sportsmen = "INSERT INTO sportsmen (SportsmenId, Surname, Name, Sex," \
                            "Year) VALUES (%s, %s, %s, %s, %s)"
            sql_statistics_sportsmen = "INSERT INTO statisticssportsmen (SportsmenId, AllCountStarts," \
                                       "AllCountStartsF, AllCountStartsZeroSpeed, AllTime, " \
                                       "LengthAll, AvgSpeed, BestSpeedFirst, BestSpeed, BadSpeed ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql_elite = "INSERT INTO a_elite (SportsmenId, CountStarts, CountStartsFinished, CountStartsZeroSpeed, AllTime, LengthAll," \
                        "AvgSpeed, Points, PointsBad1, PointsBad2, PointsBad3, PointsBad4, PointsBad5, PlaceOld, PlaceChange) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql_adult = "INSERT INTO b_adult (SportsmenId, CountStarts, CountStartsFinished, CountStartsZeroSpeed, AllTime, LengthAll," \
                       "AvgSpeed, Points, PointsBad1, PointsBad2, PointsBad3, PointsBad4, PointsBad5, PlaceOld, PlaceChange) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql_teenager = "INSERT INTO b_teenager (SportsmenId, CountStarts, CountStartsFinished, CountStartsZeroSpeed, AllTime, LengthAll," \
                          "AvgSpeed, Points, PointsBad1, PointsBad2, PointsBad3, PointsBad4, PointsBad5, PlaceOld, PlaceChange) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql_veteran = "INSERT INTO b_veteran (SportsmenId, CountStarts, CountStartsFinished, CountStartsZeroSpeed, AllTime, LengthAll," \
                          "AvgSpeed, Points, PointsBad1, PointsBad2, PointsBad3, PointsBad4, PointsBad5, PlaceOld, PlaceChange) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql_kid = "INSERT INTO c_kid (SportsmenId, CountStarts, CountStartsFinished, CountStartsZeroSpeed, AllTime, LengthAll," \
                      "AvgSpeed, Points, PointsBad1, PointsBad2, PointsBad3, PointsBad4, PointsBad5, PlaceOld, PlaceChange) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # запросы на обновление уже имющихся спортсменов в таблциах
            # sql_sportsmen_update = "UPDATE sportsmen (SportsmenId, Surname, Name, Sex," \
            #                 "Year) VALUES (%s, %s, %s, %s, %s)"
            sql_statistics_sportsmen_update = "UPDATE statisticssportsmen SET AllCountStarts = %s , " \
                                              "AllCountStartsF = %s, AllCountStartsZeroSpeed = %s, AllTime = %s, " \
                                              "LengthAll = %s, AvgSpeed = %s, BestSpeedFirst = %s, BestSpeed = %s, " \
                                              "BadSpeed = %s WHERE SportsmenId = %s"
            sql_elite_update = "UPDATE a_elite SET CountStarts = %s, CountStartsFinished = %s, CountStartsZeroSpeed = %s, AllTime = %s, " \
                               "LengthAll = %s, AvgSpeed = %s, Points = %s, PointsBad1 = %s, PointsBad2 = %s, " \
                               " PointsBad3 = %s, PointsBad4 = %s, PointsBad5 = %s WHERE SportsmenId = %s"
            sql_adult_update = "UPDATE b_adult SET CountStarts = %s, CountStartsFinished = %s, CountStartsZeroSpeed = %s, AllTime = %s, " \
                               "LengthAll = %s, AvgSpeed = %s, Points = %s, PointsBad1 = %s, PointsBad2 = %s, " \
                               " PointsBad3 = %s, PointsBad4 = %s, PointsBad5 = %s WHERE SportsmenId = %s"
            sql_teenager_update = "UPDATE b_teenager SET CountStarts = %s, CountStartsFinished = %s, CountStartsZeroSpeed = %s, AllTime = %s, " \
                                  "LengthAll = %s, AvgSpeed = %s, Points = %s, PointsBad1 = %s, PointsBad2 = %s, " \
                                  " PointsBad3 = %s, PointsBad4 = %s, PointsBad5 = %s WHERE SportsmenId = %s"
            sql_veteran_update = "UPDATE b_veteran SET CountStarts = %s, CountStartsFinished = %s, CountStartsZeroSpeed = %s, AllTime = %s, " \
                                 "LengthAll = %s, AvgSpeed = %s, Points = %s, PointsBad1 = %s, PointsBad2 = %s, " \
                                 "PointsBad3 = %s, PointsBad4 = %s, PointsBad5 = %s WHERE SportsmenId = %s"
            sql_kid_update = "UPDATE c_kid SET CountStarts = %s, CountStartsFinished = %s, CountStartsZeroSpeed = %s, AllTime = %s, " \
                             "LengthAll = %s, AvgSpeed = %s, Points = %s, PointsBad1 = %s, PointsBad2 = %s, " \
                             "PointsBad3 = %s, PointsBad4 = %s, PointsBad5 = %s WHERE SportsmenId = %s"

            # запросы о существующих данных в таблицах бд
            cur.execute("SELECT * FROM statisticsstarts")
            bd_statistics_start = cur.fetchall()

            cur.execute("SELECT * FROM statisticssportsmen")
            bd_statistics_sportsmen = list(cur.fetchall())

            cur.execute("SELECT * FROM sportsmen")
            bd_sportsmen = cur.fetchall()


            # выборка всей таблицы с сортировкой сначаа все Ж по очкам вниз, потом сразу все м по очкам вниз
            cur.execute("SELECT * FROM a_elite LEFT JOIN sportsmen ON a_elite.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, a_elite.Points   DESC, sportsmen.Surname DESC ")
            bd_elite = list(cur.fetchall())

            cur.execute("SELECT * FROM b_adult LEFT JOIN sportsmen ON b_adult.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, b_adult.Points DESC, sportsmen.Surname DESC ")
            bd_adult = list(cur.fetchall())

            cur.execute("SELECT * FROM b_teenager LEFT JOIN sportsmen ON b_teenager.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, b_teenager.Points DESC, sportsmen.Surname DESC")
            bd_teenager = list(cur.fetchall())

            cur.execute("SELECT * FROM b_veteran LEFT JOIN sportsmen ON b_veteran.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, b_veteran.Points DESC, sportsmen.Surname DESC")
            bd_veteran = list(cur.fetchall())

            cur.execute("SELECT * FROM c_kid LEFT JOIN sportsmen ON c_kid.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, c_kid.Points DESC, sportsmen.Surname DESC")
            bd_kid = list(cur.fetchall())


            # записываем спарсенные данные в бд добавляем новых спорстменов если они есть
            for i in list_sportsmen:
                if len(bd_sportsmen) == 0:
                    cur.execute(sql_sportsmen, (i["sportsmen_id"], i["surname"], i["name"], i["sex"], i["year"]))
                for jndex, j in enumerate(bd_sportsmen):
                    if (i["name"] in j) and (i["surname"] in j) and (i["year"] in j):
                        break
                    elif jndex == len(bd_sportsmen) - 1:
                        cur.execute(sql_sportsmen, (i["sportsmen_id"], i["surname"], i["name"], i["sex"], i["year"]))

            # записываем спарсенные данные в бд обновляем личную статистику спортсменов
            for i in list_sportsmen:
                if i["place"] > 0:
                    cx = 1  # счетчик удачного старта
                else:
                    cx = 0  # счетчик неудачного старта
                if len(bd_statistics_sportsmen) == 0:  # если список спортсменов пустой. первый раз загружаем данные
                    cur.execute(sql_statistics_sportsmen,
                                (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"],
                                 i["speed"], i["splits"][0], i["splits"][1], i["splits"][2]))
                for jndex, j in enumerate(bd_statistics_sportsmen):
                    if i["sportsmen_id"] == j[0]:  # Обновляем статистику спортсмена
                        z1 = j[7]  # лучший первый сплит текущий
                        x1 = j[8]  # лучший сплит текущий
                        y1 = j[9]  # худший сплит текущий
                        if j[7] == -1 or j[7] > i["splits"][0] > 0:  # сплиты текущий и с очередного старта, обновляем если быстрее
                            z1 = i["splits"][0]
                        if j[8] == -1 or j[8] > i["splits"][1] > 0:  # сплиты текущий и с очередного старта, обновляем если быстрее
                            x1 = i["splits"][1]
                        if j[9] < i["splits"][2]:  # обновляем худший сплит
                            y1 = i["splits"][2]

                        try:
                            if i["speed"] == 0:
                                k = j[6]  # если скорость нулевая, значит не было ни одного правильного сплита, значит и скорость средняя не поменялась
                            else:  # int_r функция округления по мат правилам в большую или меньшую сторону
                                k = int_r((j[6] * (j[1] - j[3]) + i["speed"]) / (j[1] + 1 - j[3]))  #j[3] вычитаем все старты где снялись сразу с 1го перегона. на таких стартах скорость была 0, поэтому нельзя этот старт считать при вычислении средней скорости
                        except ZeroDivisionError:
                            k = 0
                        cur.execute(sql_statistics_sportsmen_update,
                                    (j[1] + 1, j[2] + cx, j[3] + 1 if i["speed"] == 0 else j[3], j[4] + i["result"],
                                     j[5] + i["length"], k, z1, x1, y1, i["sportsmen_id"]))

                        bd_statistics_sportsmen.pop(jndex)
                        break
                    elif jndex == len(bd_statistics_sportsmen) - 1:  # если спортсмена нет добавляем его данные в 1 раз
                        cur.execute(sql_statistics_sportsmen,
                                    (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"],
                                     i["speed"], i["splits"][0], i["splits"][1], i["splits"][2]))


            # Сортируем список спортсменов по именам группы (Элита М-Ж, Подростки М-Ж, Дети М-Ж, Взрослые М-Ж, Ветераны М-Ж)
            # Затем по очкам и в последнюю очередь по фамилии, реверс по убыванию
            list_sportsmen = sorted(list_sportsmen, key=lambda x: (x["group_name"], x["point"], x["surname"]), reverse=True)

            group_name = ""  # служит как флаг для определения изменения мест, какая группа сейчас в цикле работает
            # записываем спарсенные данные в бд для Дистанций
            while len(list_sportsmen) != 0:
            # for i in list_sportsmen:
                i = list_sportsmen[0]
                if i["place"] > 0:
                    cx = 1
                else:
                    cx = 0
                count_sportsmen_group = 0
                if "Ветераны" in i["group_name"]:
                    if len(bd_veteran) == 0:  # добавляем новых участников в таблицу с текущими начальными очками если еще группа пустая
                        if i["place"] == 1 and i["group_name"] != group_name:  # ищем от первого отсортированного участника последнего сошедшего или из другой группы, при повторяющихся первых местах проверяем группу чтобы не было повторного определения мест после удаления спортсмена из массива list_sportsmen в конце цикла
                            group_name = i["group_name"]  # пзапоминаем имя рабочей группы при присвоении в ней мест
                            for index, dict_ in enumerate(list_sportsmen):
                                if (dict_["place"] == 1 and i["sportsmen_id"] != dict_["sportsmen_id"]) and dict_["group_name"] != group_name:  # Если мы нашли следующую группу , то запоминаем индекс
                                    kkk = index
                                    break
                                elif dict_["place"] == -1 or index == len(list_sportsmen) - 1:  # Если мы нашли первого сошедшего участника в группе или последней человек в списке
                                    kkk = index + 1
                                    break
                        if i["place"] != -1:  # проверяем место участника, если он не снялся присваиваем место из протокола
                            place_change = kkk - i["place"]
                            place_old = i["place"]
                        else:
                            place_change = 0  # всем снятым 0 изменение в позициях
                            place_old = kkk

                        cur.execute(sql_veteran,
                                    (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"], i["speed"], i["point"],
                                     -1, -1, -1, -1, i["point"], place_old, place_change))
                        list_sportsmen.pop(0)
                        continue

                    for jndex, j in enumerate(bd_veteran):
                        if i["sportsmen_id"] == j[0]:

                            # создаем массив с худшими очками участника, добавляем в него очки с текущего старта,
                            # потом сортируем (по возрастанию) и удаляем самые большие очки
                            point_array = [j[8], j[9], j[10], j[11], j[12], i["point"]]
                            point_array = sorted(point_array)
                            if j[8] != -1:  # если самые маленькие очки не -1 то удаляем последнее значение из массива
                                point_array.pop()
                            else:  # если первое значение -1 то скорее всего еще не набрано стартов и удаяем первое чтоб сместить
                                point_array.pop(0)

                            try:
                                if i["speed"] == 0:
                                    k = j[6]  # если скорость нулевая, значит не было ни одного правильного сплита, значит и скорость средняя не поменялась
                                else:
                                    k = int_r((j[6] * (j[1] - j[3]) + i["speed"]) / (j[1] + 1 - j[3]))  #j[3] вычитаем все старты где снялись сразу с 1го перегона. на таких стартах скорость была 0, поэтому нельзя этот старт считать при вычислении средней скорости
                            except ZeroDivisionError:
                                k = 0

                            cur.execute(sql_veteran_update,
                                        (j[1] + 1, j[2] + cx, j[3] + 1 if i["speed"] == 0 else j[3], j[4] + i["result"], j[5] + i["length"],
                                         k, j[7] + i["point"], point_array[0], point_array[1],
                                         point_array[2], point_array[3], point_array[4],
                                         i["sportsmen_id"]))
                            # bd_veteran.pop(jndex)  # удаляем из списка найденные айди чтобы уменьшить кол-во будущих итераций
                            list_sportsmen.pop(0)
                            break
                        elif jndex == len(bd_veteran) - 1:  # добавляем нового участника в таблицу с текущими начальными очками если не нашли его в базе
                            cur.execute(sql_veteran,
                                        (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"], i["speed"], i["point"],
                                         -1, -1, -1, -1, i["point"], 0, 0))  # столбцу PlaceChange присвоим пока 0, после коммита сделаем еще один инсерт с текущим place-change
                            list_sportsmen.pop(0)

                elif "Взрослые" in i["group_name"]:
                    if len(bd_adult) == 0:  # добавляем новых участников в таблицу с текущими начальными очками если еще группа пустая
                        if i["place"] == 1 and i["group_name"] != group_name:  # ищем от первого отсортированного участника последнего сошедшего или из другой группы, при повторяющихся первых местах проверяем группу чтобы не было повторного определения мест после удаления спортсмена из массива list_sportsmen в конце цикла
                            group_name = i["group_name"]  # пзапоминаем имя рабочей группы при присвоении в ней мест
                            for index, dict_ in enumerate(list_sportsmen):
                                if (dict_["place"] == 1 and i["sportsmen_id"] != dict_["sportsmen_id"]) and dict_["group_name"] != group_name:  # Если мы нашли следующую группу , то запоминаем индекс
                                    kkk = index
                                    break
                                elif dict_["place"] == -1 or index == len(list_sportsmen) - 1:  # Если мы нашли первого сошедшего участника в группе или последней человек в списке
                                    kkk = index + 1
                                    break
                        if i["place"] != -1:  # проверяем место участника, если он не снялся присваиваем место из протокола
                            place_change = kkk - i["place"]
                            place_old = i["place"]
                        else:
                            place_change = 0  # всем снятым 0 изменение в позициях
                            place_old = kkk

                        cur.execute(sql_adult,
                                    (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"], i["speed"], i["point"],
                                     -1, -1, -1, -1, i["point"], place_old, place_change))
                        list_sportsmen.pop(0)
                        continue

                    for jndex, j in enumerate(bd_adult):
                        if i["sportsmen_id"] == j[0]:

                            point_array = [j[8], j[9], j[10], j[11], j[12], i["point"]]
                            point_array = sorted(point_array)
                            if j[8] != -1:  # если самые маленькие очки не -1 то удаляем послледнее значение из массива
                                point_array.pop()
                            else:  # если первое значение -1 то скорее всего еще не набрано стартов и удаяем первое чтоб сместить
                                point_array.pop(0)

                            try:
                                if i["speed"] == 0:
                                    k = j[6]
                                else:
                                    k = int_r((j[6] * (j[1] - j[3]) + i["speed"]) / (j[1] + 1 - j[3]))  #j[3] вычитаем все старты где снялись сразу с 1го перегона. на таких стартах скорость была 0, поэтому нельзя этот старт считать при вычислении средней скорости
                            except ZeroDivisionError:
                                k = 0

                            cur.execute(sql_adult_update, (j[1] + 1, j[2] + cx, j[3] + 1 if i["speed"] == 0 else j[3], j[4] + i["result"], j[5] + i["length"],
                                                           k, j[7] + i["point"], point_array[0], point_array[1],
                                                           point_array[2], point_array[3], point_array[4],
                                                           i["sportsmen_id"]))
                            # bd_adult.pop(jndex)  # удаляем из списка найденные айди чтобы уменьшить кол-во будущих итераций
                            list_sportsmen.pop(0)
                            break
                        elif jndex == len(bd_adult) - 1:  # добавляем нового участника в таблицу с текущими начальными очками если не нашли его в базе
                            cur.execute(sql_adult,
                                        (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"], i["speed"], i["point"],
                                         -1, -1, -1, -1, i["point"], 0, 0))  # столбцу PlaceChange присвоим пока 0, после коммита сделаем еще один инсерт с текущим place-change
                            list_sportsmen.pop(0)

                elif "Дети" in i["group_name"]:
                    if len(bd_kid) == 0:  # добавляем новых участников в таблицу с текущими начальными очками если еще группа пустая
                        if i["place"] == 1 and i["group_name"] != group_name:  # ищем от первого отсортированного участника последнего сошедшего или из другой группы, при повторяющихся первых местах проверяем группу чтобы не было повторного определения мест после удаления спортсмена из массива list_sportsmen в конце цикла
                            group_name = i["group_name"]  # пзапоминаем имя рабочей группы при присвоении в ней мест
                            for index, dict_ in enumerate(list_sportsmen):
                                if (dict_["place"] == 1 and i["sportsmen_id"] != dict_["sportsmen_id"]) and dict_["group_name"] != group_name:  # Если мы нашли следующую группу , то запоминаем индекс
                                    kkk = index
                                    break
                                elif dict_["place"] == -1 or index == len(list_sportsmen) - 1:  # Если мы нашли первого сошедшего участника в группе или последней человек в списке
                                    kkk = index + 1
                                    break
                        if i["place"] != -1:  # проверяем место участника, если он не снялся присваиваем место из протокола
                            place_change = kkk - i["place"]
                            place_old = i["place"]
                        else:
                            place_change = 0  # всем снятым 0 изменение в позициях
                            place_old = kkk

                        cur.execute(sql_kid,
                                    (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"], i["speed"], i["point"],
                                     -1, -1, -1, -1, i["point"], place_old, place_change))
                        list_sportsmen.pop(0)
                        continue

                    for jndex, j in enumerate(bd_kid):
                        if i["sportsmen_id"] == j[0]:

                            point_array = [j[8], j[9], j[10], j[11], j[12], i["point"]]
                            point_array = sorted(point_array)
                            if j[8] != -1:  # если самые маленькие очки не -1 то удаляем послледнее значение из массива
                                point_array.pop()
                            else:  # если первое значение -1 то скорее всего еще не набрано стартов и удаяем первое чтоб сместить
                                point_array.pop(0)

                            try:
                                if i["speed"] == 0:
                                    k = j[6]
                                else:
                                    k = int_r((j[6] * (j[1] - j[3]) + i["speed"]) / (j[1] + 1 - j[3]))  #j[3] вычитаем все старты где снялись сразу с 1го перегона. на таких стартах скорость была 0, поэтому нельзя этот старт считать при вычислении средней скорости
                            except ZeroDivisionError:
                                k = 0

                            cur.execute(sql_kid_update, (j[1] + 1, j[2] + cx, j[3] + 1 if i["speed"] == 0 else j[3], j[4] + i["result"], j[5] + i["length"],
                                                         k, j[7] + i["point"], point_array[0], point_array[1],
                                                         point_array[2], point_array[3], point_array[4],
                                                         i["sportsmen_id"]))
                            # bd_kid.pop(jndex)  # удаляем из списка найденные айди чтобы уменьшить кол-во будущих итераций
                            list_sportsmen.pop(0)
                            break
                        elif jndex == len(bd_kid) - 1:  # добавляем нового участника в таблицу с текущими начальными очками если не нашли его в базе
                            cur.execute(sql_kid,
                                        (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"], i["speed"], i["point"],
                                         -1, -1, -1, -1, i["point"], 0, 0))  # столбцу PlaceChange присвоим пока 0, после коммита сделаем еще один инсерт с текущим place-change
                            list_sportsmen.pop(0)

                elif "Подростки" in i["group_name"]:
                    if len(bd_teenager) == 0:  # добавляем новых участников в таблицу с текущими начальными очками если еще группа пустая
                        if i["place"] == 1 and i["group_name"] != group_name:  # ищем от первого отсортированного участника последнего сошедшего или из другой группы, при повторяющихся первых местах проверяем группу чтобы не было повторного определения мест после удаления спортсмена из массива list_sportsmen в конце цикла
                            group_name = i["group_name"]  # пзапоминаем имя рабочей группы при присвоении в ней мест
                            for index, dict_ in enumerate(list_sportsmen):
                                if (dict_["place"] == 1 and i["sportsmen_id"] != dict_["sportsmen_id"]) and dict_["group_name"] != group_name:  # Если мы нашли следующую группу , то запоминаем индекс
                                    kkk = index
                                    break
                                elif dict_["place"] == -1 or index == len(list_sportsmen) - 1:  # Если мы нашли первого сошедшего участника в группе или последней человек в списке
                                    kkk = index + 1
                                    break
                        if i["place"] != -1:  # проверяем место участника, если он не снялся присваиваем место из протокола
                            place_change = kkk - i["place"]
                            place_old = i["place"]
                        else:
                            place_change = 0  # всем снятым 0 изменение в позициях
                            place_old = kkk

                        cur.execute(sql_teenager,
                                    (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"], i["speed"], i["point"],
                                     -1, -1, -1, -1, i["point"], place_old, place_change))
                        list_sportsmen.pop(0)
                        continue

                    for jndex, j in enumerate(bd_teenager):
                        if i["sportsmen_id"] == j[0]:

                            point_array = [j[8], j[9], j[10], j[11], j[12], i["point"]]
                            point_array = sorted(point_array)
                            if j[8] != -1:  # если самые маленькие очки не -1 то удаляем послледнее значение из массива
                                point_array.pop()
                            else:  # если первое значение -1 то скорее всего еще не набрано стартов и удаяем первое чтоб сместить
                                point_array.pop(0)

                            try:
                                if i["speed"] == 0:
                                    k = j[6]
                                else:
                                    k = int_r((j[6] * (j[1] - j[3]) + i["speed"]) / (j[1] + 1 - j[3]))  #j[3] вычитаем все старты где снялись сразу с 1го перегона. на таких стартах скорость была 0, поэтому нельзя этот старт считать при вычислении средней скорости
                            except ZeroDivisionError:
                                k = 0

                            cur.execute(sql_teenager_update,
                                        (j[1] + 1, j[2] + cx, j[3] + 1 if i["speed"] == 0 else j[3], j[4] + i["result"], j[5] + i["length"],
                                         k, j[7] + i["point"], point_array[0], point_array[1],
                                         point_array[2], point_array[3], point_array[4],
                                         i["sportsmen_id"]))
                            # bd_teenager.pop(jndex)  # удаляем из списка найденные айди чтобы уменьшить кол-во будущих итераций
                            list_sportsmen.pop(0)
                            break
                        elif jndex == len(bd_teenager) - 1:  # добавляем нового участника в таблицу с текущими начальными очками если не нашли его в базе
                            cur.execute(sql_teenager,
                                        (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"], i["speed"], i["point"],
                                         -1, -1, -1, -1, i["point"], 0, 0))  # столбцу PlaceChange присвоим пока 0, после коммита сделаем еще один инсерт с текущим place-change
                            list_sportsmen.pop(0)

                elif "Элита" in i["group_name"]:
                    if len(bd_elite) == 0:  # добавляем новых участников в таблицу с текущими начальными очками если еще группа пустая
                        if i["place"] == 1 and i["group_name"] != group_name:  # ищем от первого отсортированного участника последнего сошедшего или из другой группы, при повторяющихся первых местах проверяем группу чтобы не было повторного определения мест после удаления спортсмена из массива list_sportsmen в конце цикла
                            group_name = i["group_name"]  # пзапоминаем имя рабочей группы при присвоении в ней мест
                            for index, dict_ in enumerate(list_sportsmen):
                                if (dict_["place"] == 1 and i["sportsmen_id"] != dict_["sportsmen_id"]) and dict_["group_name"] != group_name:  # Если мы нашли следующую группу , то запоминаем индекс
                                    kkk = index
                                    break
                                elif dict_["place"] == -1 or index == len(list_sportsmen) - 1:  # Если мы нашли первого сошедшего участника в группе или последней человек в списке
                                    kkk = index + 1
                                    break
                        if i["place"] != -1:  # проверяем место участника, если он не снялся присваиваем место из протокола
                            place_change = kkk - i["place"]
                            place_old = i["place"]
                        else:
                            place_change = 0  # всем снятым 0 изменение в позициях
                            place_old = kkk

                        cur.execute(sql_elite,
                                    (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"], i["speed"], i["point"],
                                     -1, -1, -1, -1, i["point"], place_old, place_change))
                        list_sportsmen.pop(0)
                        continue

                    for jndex, j in enumerate(bd_elite):
                        if i["sportsmen_id"] == j[0]:

                            point_array = [j[8], j[9], j[10], j[11], j[12], i["point"]]
                            point_array = sorted(point_array)
                            if j[8] != -1:  # если самые маленькие очки не -1 то удаляем послледнее значение из массива
                                point_array.pop()
                            else:  # если первое значение -1 то скорее всего еще не набрано стартов и удаяем первое чтоб сместить
                                point_array.pop(0)

                            try:
                                if i["speed"] == 0:
                                    k = j[6]
                                else:
                                    k = int_r((j[6] * (j[1] - j[3]) + i["speed"]) / (j[1] + 1 - j[3]))  #j[3] вычитаем все старты где снялись сразу с 1го перегона. на таких стартах скорость была 0, поэтому нельзя этот старт считать при вычислении средней скорости
                            except ZeroDivisionError:
                                k = 0

                            cur.execute(sql_elite_update, (j[1] + 1, j[2] + cx, j[3] + 1 if i["speed"] == 0 else j[3], j[4] + i["result"], j[5] + i["length"],
                                                           k, j[7] + i["point"], point_array[0], point_array[1],
                                                           point_array[2], point_array[3], point_array[4],
                                                           i["sportsmen_id"]))
                            # bd_elite.pop(jndex)  # удаляем из списка найденные айди чтобы уменьшить кол-во будущих итераций
                            list_sportsmen.pop(0)
                            break
                        elif jndex == len(bd_elite) - 1:  # добавляем нового участника в таблицу с текущими начальными очками если не нашли его в базе
                            cur.execute(sql_elite,
                                        (i["sportsmen_id"], 1, cx, 1 if i["speed"] == 0 else 0, i["result"], i["length"], i["speed"], i["point"],
                                         -1, -1, -1, -1, i["point"], 0, 0))  # столбцу PlaceChange присвоим пока 0, после коммита сделаем еще один инсерт с текущим place-change
                            list_sportsmen.pop(0)

            con.commit()

            list_bd_group = [[0] * 3 for i in range(5)]

            cur.execute("SELECT a_elite.SportsmenId, a_elite.PlaceOld, sportsmen.Sex FROM a_elite LEFT JOIN sportsmen ON a_elite.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, a_elite.PlaceOld, sportsmen.Surname DESC")
            list_bd_group[0][0] = list(cur.fetchall())
            cur.execute("SELECT a_elite.SportsmenId, a_elite.Points, sportsmen.Sex FROM a_elite LEFT JOIN sportsmen ON a_elite.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, a_elite.Points DESC, sportsmen.Surname DESC")
            list_bd_group[0][1] = list(cur.fetchall())

            cur.execute("SELECT b_adult.SportsmenId, b_adult.PlaceOld, sportsmen.Sex FROM b_adult LEFT JOIN sportsmen ON b_adult.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, b_adult.PlaceOld, sportsmen.Surname DESC")
            list_bd_group[1][0] = list(cur.fetchall())
            cur.execute("SELECT b_adult.SportsmenId, b_adult.Points, sportsmen.Sex FROM b_adult LEFT JOIN sportsmen ON b_adult.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, b_adult.Points DESC, sportsmen.Surname DESC")
            list_bd_group[1][1] = list(cur.fetchall())

            cur.execute("SELECT b_teenager.SportsmenId, b_teenager.PlaceOld, sportsmen.Sex FROM b_teenager LEFT JOIN sportsmen ON b_teenager.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, b_teenager.PlaceOld, sportsmen.Surname DESC")
            list_bd_group[2][0] = list(cur.fetchall())
            cur.execute("SELECT b_teenager.SportsmenId, b_teenager.Points, sportsmen.Sex FROM b_teenager LEFT JOIN sportsmen ON b_teenager.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, b_teenager.Points DESC, sportsmen.Surname DESC")
            list_bd_group[2][1] = list(cur.fetchall())

            cur.execute("SELECT b_veteran.SportsmenId, b_veteran.PlaceOld, sportsmen.Sex FROM b_veteran LEFT JOIN sportsmen ON b_veteran.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, b_veteran.PlaceOld, sportsmen.Surname DESC")
            list_bd_group[3][0] = list(cur.fetchall())
            cur.execute("SELECT b_veteran.SportsmenId, b_veteran.Points, sportsmen.Sex FROM b_veteran LEFT JOIN sportsmen ON b_veteran.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, b_veteran.Points DESC, sportsmen.Surname DESC")
            list_bd_group[3][1] = list(cur.fetchall())

            cur.execute("SELECT c_kid.SportsmenId, c_kid.PlaceOld, sportsmen.Sex FROM c_kid LEFT JOIN sportsmen ON c_kid.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, c_kid.PlaceOld, sportsmen.Surname DESC")
            list_bd_group[4][0] = list(cur.fetchall())
            cur.execute("SELECT c_kid.SportsmenId, c_kid.Points, sportsmen.Sex FROM c_kid LEFT JOIN sportsmen ON c_kid.SportsmenId = sportsmen.SportsmenId ORDER BY sportsmen.Sex, c_kid.Points DESC, sportsmen.Surname DESC")
            list_bd_group[4][1] = list(cur.fetchall())

            list_sql_group = []
            list_sql_group.append("UPDATE a_elite SET PlaceOld = %s, PlaceChange = %s WHERE SportsmenId = %s")
            list_sql_group.append("UPDATE b_adult SET PlaceOld = %s, PlaceChange = %s WHERE SportsmenId = %s")
            list_sql_group.append("UPDATE b_teenager SET PlaceOld = %s, PlaceChange = %s WHERE SportsmenId = %s")
            list_sql_group.append("UPDATE b_veteran SET PlaceOld = %s, PlaceChange = %s WHERE SportsmenId = %s")
            list_sql_group.append("UPDATE c_kid SET PlaceOld = %s, PlaceChange = %s WHERE SportsmenId = %s")

            if statistics_starts["start_id"] != 1001:
                for jndex, bd_group in enumerate(list_bd_group):
                    dist = []
                    j = 0
                    i = 0
                    placeF = 1
                    placeM = 1
                    for index in bd_group[1]:
                        if index[2] == 'Ж':
                            if j == 0:
                                dist.append([placeF, index[1], index[0]])  # dist[место, кол-во очков, id спортсммена]
                            else:
                                dist.append([placeF, index[1], index[0]])  # ставим предыдущее место и проверяем такли оно, если не так меняем
                                if dist[j][1] != dist[j-1][1]:  # сравниваем очки нынешнеего и предыдущего участника
                                    placeF = j + 1  # если место не дублируется присваиваем ему значение итерации
                                    dist[j][0] = placeF
                        else:
                            if i == 0:
                                dist.append([placeM, index[1], index[0]])
                            else:
                                dist.append([placeM, index[1], index[0]])  # ставим предыдущее место и проверяем такли оно, если не так меняем
                                if dist[j][1] != dist[j-1][1]:  # сравниваем очки нынешнеего и предыдущего участника
                                    placeM = i + 1  # если место не дублируется присваиваем ему значение итерации
                                    dist[j][0] = placeM
                            i += 1
                        j += 1

                    for n in dist:  # записываем изменение места с предыдущим стартом и переписываем PlaceOld для следующих протоколов
                        for index, m in enumerate(bd_group[0]):
                            if n[2] == m[0]:
                                if m[1] == 0:  # если у спортсмена PlaceOld = 0 значит он только что добавлен, ставим ему последнее место из сейчашних
                                    if m[2] == 'Ж':
                                        cur.execute(list_sql_group[jndex], (n[0], (n[0] - placeF) * (-1), n[2]))
                                    else:
                                        cur.execute(list_sql_group[jndex], (n[0], (n[0] - placeM) * (-1), n[2]))
                                    break
                                else:
                                    cur.execute(list_sql_group[jndex], (n[0], (n[0] - m[1])*(-1), n[2]))
                                    break

                con.commit()

        else:
            return 3  # файл уже был закачен
    return 1  # файл успешно закачен в бд


def girlName():
    """ считываем женские имена для определения пола"""
    with open("girl_name.txt", "r") as f:
        try:
            girl_name = f.readlines()
            for i in range(0, len(girl_name) - 1):
                girl_name[i] = girl_name[i][0:-1]  # убираем пробелы( ентыры)
        except FileNotFoundError:  # исключение при отсутствии файла имён
            girl_name = ""
        finally:
            f.close()
    return girl_name


# try:
#        with open("girl_name.txt", "r") as f:
#            girl_name = f.read()
#    except FileNotFoundError:  # исключение при отсутствии файла имён
#        girl_name = ""
#    return girl_name

def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num


def createConfig(path):
    """
    создаем config file если не существует
    """
    config = configparser.ConfigParser()
    config.add_section("o-party")
    config.set("o-party", "host", "localhost")
    config.set("o-party", "user", "admin")
    config.set("o-party", "password", "admin")
    config.set("o-party", "db", "result")

    with open(path, "w") as config_file:
        config.write(config_file)


@eel.expose
def crudConfig():
    """
    Чтение config файла
    """
    if not os.path.exists(path):
        createConfig(path)

    config = configparser.ConfigParser()
    config.read(path)

    # Читаем некоторые значения из конфиг. файла.
    host = config.get("o-party", "host")
    user = config.get("o-party", "user")
    password = config.get("o-party", "password")
    db = config.get("o-party", "db")

    return host, user, password, db

    # Меняем значения из конфиг. файла.
    # config.set("Settings", "font_size", "12")
    #
    # # Удаляем значение из конфиг. файла.
    # config.remove_option("Settings", "font_style")

    # Вносим изменения в конфиг. файл.
    # with open(path, "w") as config_file:
    #     config.write(config_file)


if __name__ == "__main__":
    path = "settings.ini"
    db_data = []  # сохраняем сюда введенные данные для подключения к бд
    file_date = ""  # сохраняем название файла как дату протокола, если в протоколе нет даты
    # crudConfig(path)
    eel.init("web")  # расположение папки с html
    eel.start("main.html", size=(320, 460))  # запускаем файл стартовый
