"""Модуль с классом игр"""

from classes.players_class import Players
from classes.const.codes import CODES
from random import choice
from datetime import datetime
import threading


class Game:
    """Класс, содержащий в себе все идущие в данный момент игры, и обрабатывающий взаимодействие игроков,
     предоставляющий параметры для отображения на web-странице"""
    def __init__(self):
        """Инициализация класса"""
        self.games_map = {}
        self.used_urls = []
        self.is_everybody_choose = {}
        self.is_everybody_vote = {}
        self.is_self_vote = {}
        self.is_self_choose = {}
        self.games_places = {}
        self.assotiation = {}
        self.created_time = {}
        self.timers = {}
        self.win_points = {}

    def add(self, names_list, card_num, quick_game=False):
        """Добавление игры
        names_list - список имен игроков
        card_num - кортеж количества карт в руке и в колоде
        quick_game - индикатор быстрая игра(15 очков для победы) или нет(30 очков для победы)"""
        code = self.choose_url()
        cards_in_hand = card_num[1]
        cards_in_deck = card_num[0]
        self.games_map[code] = Players(cards_in_hand, cards_in_deck)
        self.is_everybody_choose[code] = False
        self.is_everybody_vote[code] = True
        self.is_self_vote[code] = {}
        self.is_self_choose[code] = {}
        self.created_time[code] = datetime.now()
        self.win_points[code] = 30
        if quick_game:
            self.win_points[code] = 15
        self.timers[code] = threading.Timer(900, self.control_game, args=(code,)).start()
        self.games_places[code] = {}
        for name in names_list:
            self.games_places[code][name] = 1
        self.assotiation[code] = None
        for i in range(len(names_list)):
            if i + 1 != len(names_list):
                self.games_map[code].add(names_list[i])
            else:
                self.games_map[code].add(names_list[i], end=True)
            self.is_self_choose[code][names_list[i]] = False
            self.is_self_vote[code][names_list[i]] = True
        return code

    def choose_url(self):
        """Выбор уникального кода из списка кодов
            возвращает выбранный код"""
        if len(self.used_urls) == len(CODES):
            return None
        code = choice(CODES)
        while code in self.used_urls:
            code = choice(CODES)
        self.used_urls.append(code)
        return code

    def who_is_directing(self, code):
        """Возвращение имени ведущего
                code - код игры"""
        return self.games_map[code].who_is_directing()

    def get_points(self, code):
        """Возвращение очков игроков
                code - код игры"""
        return self.games_map[code].get_points()

    def get_names(self, code):
        """Возвращение имен игроков этой игры
                code - код игры"""
        return self.games_map[code].get_names()

    def somebody_vote(self, code, name, number):
        """Обработка голосования игроков за карты
        code - код игры
        name - имя проголосовавшего
        number - номер карты, за которую проголосовал игрок"""
        self.is_everybody_vote[code] = self.games_map[code].somebody_answer(name, number)
        self.is_self_vote[code][name] = True
        if self.is_everybody_vote[code]:
            self.is_everybody_choose[code] = False
            for name in self.games_map[code].get_names():
                self.is_self_choose[code][name] = False
            self.count_places(code)
            self.assotiation[code] = None

    def somebody_choose(self, code, name, number):
        """Обработка выбора игроками карт
        code - код игры
        name - имя выбравшего
        number - номер карты, которую выбрал игрок"""
        self.is_everybody_choose[code] = self.games_map[code].somebody_choose(name, number)
        self.is_self_choose[code][name] = True
        if self.is_everybody_choose[code]:
            self.is_everybody_vote[code] = False
            for name in self.games_map[code].get_names():
                self.is_self_vote[code][name] = False

    def is_choosing(self, code):
        """Возвращение логического значения все ли игроки выбрали карты или нет
                code - код игры"""
        return not self.is_everybody_choose[code]

    def is_choose(self, code, name):
        """Возвращение логического значения выбрал игрок карту или нет
                code - код игры
                name - имя игрока"""
        return self.is_self_choose[code][name]

    def is_voting(self, code):
        """Возвращение логического значения все ли игроки проголосовали или нет
                code - код игры"""
        return not self.is_everybody_vote[code]

    def is_vote(self, code, name):
        """Возвращение логического значения проголосовал игрок или нет
                code - код игры
                name - имя игрока"""
        return self.is_self_vote[code][name]

    def games_number(self):
        """Возвращение количество игр в данный момент"""
        return len(self.games_map)

    def cards(self, code, name):
        """Возвращение карт для этой игры и игрока
                code - код игры
                name - имя игрока"""
        return self.games_map[code].cards(name)

    def get_choices(self, code):
        """Возвращение выборов игроков для этой игры
                code - код игры"""
        return self.games_map[code].get_choices()

    def choosen_images(self, code):
        """Возвращение выбранных игроками карт для этой игры
                code - код игры"""
        return self.games_map[code].image_choices()

    def players_progress(self, code):
        """Возвращение удобного для отображения на web-странице вида очков игроков
                code - код игры"""
        progress = dict()
        p = self.games_map[code].get_points().items()
        for name, points in p:
            progress[name] = points / self.win_points[code] * 100
        return progress

    def player_place(self, code, name):
        """Возвращение места игрока
            code - код игры
            name - имя"""
        if self.is_win(code):
            return None
        return self.games_places[code][name]

    def count_places(self, code):
        """Подсчет мест игроков
                code - код игры"""
        progress = list(self.games_map[code].get_points().items())
        progress.sort(key=lambda x: x[1], reverse=True)
        places = {}
        for elem in progress:
            places[elem[0]] = progress.index(elem) + 1
        for i in range(len(progress)):
            for j in range(i):
                if progress[i][1] == progress[j][1] and places[progress[i][0]] > j + 1:
                    places[progress[i][0]] = j + 1
                    for nm in range(i + 1, len(progress)):
                        places[progress[nm][0]] -= 1
        self.games_places[code] = places

    def is_win(self, code):
        """Проверка на конец игры - и в случае выигрыша возвращение списка выигравших
            code - код игры"""
        if not self.is_everybody_vote[code] and self.games_map[code].any_cards():
            return False
        progress = self.games_map[code].get_points()
        winners = []
        is_win = False
        for name in progress.keys():
            if progress[name] >= self.win_points[code]:
                is_win = True
        for name in self.games_places[code].keys():
            if self.games_places[code][name] == 1:
                winners.append(name)
        if is_win or not self.games_map[code].any_cards():
            return winners
        return False

    def max_number_of_cards(self, code, name):
        """Возвращение максимально возможного номера карты для выбора
                code - код игры
                name - имя игрока"""
        if self.is_voting(code):
            return len(self.games_map[code].get_points())
        else:
            return len(self.games_map[code].cards(name))

    def is_valid_code(self, code):
        """Проверка на существование игры с таким кодом
                code - код игры"""
        if self.games_map.get(code, False):
            return True
        return False

    def set_assotiation(self, code, assotiation):
        """Создание ассоциации для этой игры
                code - код игры"""
        self.assotiation[code] = assotiation

    def get_assotiation(self, code):
        """Возвращение ассоциации для этой игры
                code - код игры"""
        return self.assotiation[code]

    def control_game(self, code):
        """Контролирование игры - удаление при времени ее течения больше часа
                    code - код игры"""
        if code not in self.created_time.keys():
            return
        if (datetime.now() - self.created_time[code]).total_seconds() >= 7200:
            self.delete_game(code)
            return
        self.timers[code] = threading.Timer(900, self.control_game, args=(code,)).start()

    def delete_game(self, code):
        """Удаление игры с данным кодом
                code - код игры"""
        self.used_urls.remove(code)
        del self.games_map[code]
        del self.is_everybody_choose[code]
        del self.is_everybody_vote[code]
        del self.is_self_vote[code]
        del self.is_self_choose[code]
        del self.games_places[code]
        del self.assotiation[code]
        del self.created_time[code]

    def get_time(self, code):
        """Возвращение времени с начала создания игры
                code - код игры"""
        return round(120 - (datetime.now() - self.created_time[code]).total_seconds() / 60)
