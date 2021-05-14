"""Модуль с классом игроков"""

from random import choice, shuffle, sample
from classes.const.urls import URLS


class Players:
    """Класс, содержащий в себе игроков одной игры, и обрабатывающий взаимодействие игроков,
         предоставляющий параметры для отображения на web-странице"""
    def __init__(self, cards_num=6, seq_num=72):
        """Инициализация класса"""
        self.players = {}
        self.players_choices = {}
        self.cards_number = cards_num
        self.cards_sequence = sample(URLS, seq_num - 1)
        self.used_cards = []
        self.people_who_choose = []
        self.people_who_vote = []
        self.directing = None
        self.who_was_directing = []
        self.answers = {}
        self.points = {}
        self.true_answers = {}
        self.images_numbers = []

    def add(self, name, end=False):
        """Добавление игрока
                name - имя игрока
                end - последний ли это игрок"""
        seq = []
        while len(seq) != self.cards_number:
            card = self.choose_card()
            if card:
                seq.append(card)
            else:
                break

        self.players[name] = seq
        self.points[name] = 0
        if end:
            self.directing = choice(list(self.players.keys()))
            self.who_was_directing.append(self.directing)

    def cards(self, name):
        """Возвращение карт игрока
            name - имя игрока"""
        return self.players[name]

    def get_names(self):
        """Возвращение имен игроков"""
        return self.players.keys()

    def choose_card(self):
        """Возвращение уникальной карты из колоды,и ничего если карты в колоде закончились"""
        if len(self.used_cards) == len(self.cards_sequence):
            return None
        card = choice(self.cards_sequence)
        while card in self.used_cards:
            card = choice(self.cards_sequence)
        self.used_cards.append(card)
        return card

    def somebody_choose(self, name, number):
        """Обработка выбора карты игроком, возвращает логическое значение все выбрали, или нет
            name - имя выбравшего
            number - номер карты, которую выбрал игрок"""
        self.players_choices[name] = self.players[name][number - 1]
        self.people_who_choose.append(name)
        self.players[name].pop(number - 1)
        card = self.choose_card()
        if card:
            self.players[name].append(card)
        if len(self.players) == len(self.people_who_choose):
            self.get_choices()
            self.people_who_choose = []
            return True
        return False

    def get_choices(self):
        """Обработка карт выбранных игроками"""
        answers = list(self.players_choices.keys())
        shuffle(answers)
        counter = 1
        for key in answers:
            self.true_answers[counter] = key
            counter += 1
        self.images_numbers = [self.players_choices[x] for x in answers]

    def image_choices(self):
        """Возвращение списка карт для вывода на игровое поле"""
        return self.images_numbers

    def somebody_answer(self, name, number):
        """Обработка голосования игрока, возвращает логическое значение все проголосовали, или нет
                    name - имя проголосовавшего
                    number - номер карты, которую выбрал игрок"""
        self.answers[name] = self.true_answers[number]
        self.people_who_vote.append(name)
        if len(self.people_who_vote) == len(self.players) - 1:
            self.count_points()
            self.people_who_vote = []
            self.directing = choice(list(self.players.keys()))
            while self.directing in self.who_was_directing:
                self.directing = choice(list(self.players.keys()))
            self.who_was_directing.append(self.directing)
            if len(self.who_was_directing) == len(self.players):
                self.who_was_directing = []
            self.images_numbers = []
            return True
        return False

    def who_is_directing(self):
        """Возвращение ведущего"""
        return self.directing

    def is_true(self, name):
        """Возвращение логического значения правильности ответа
                name - имя игрока"""
        return self.answers[name] == self.directing

    def count_points(self):
        """Подсчет очков"""
        number_of_true_answers = 0
        for key, value in self.answers.items():
            if value == self.directing:
                self.points[key] += 3
                number_of_true_answers += 1
            elif key != value:
                self.points[value] += 1
        if number_of_true_answers == len(self.players) - 1:
            for name in self.points.keys():
                if name != self.directing:
                    self.points[name] -= 1
                    if self.points[name] < 0:
                        self.points[name] = 0
        elif number_of_true_answers == 0:
            for name in self.points.keys():
                if name != self.directing:
                    self.points[name] += 2
        else:
            self.points[self.directing] += 3

    def get_points(self):
        """Возвращение очков игроков"""
        return self.points

    def is_choose(self, name):
        """Возвращение логического значения выбрал ли карту игрок или нет
                name - имя игрока"""
        if name in self.people_who_choose:
            return True
        return False

    def is_vote(self, name):
        """Возвращение логического значения проголосовал игрок или нет
                        name - имя игрока"""
        if name in self.people_who_vote:
            return True
        return False

    def any_cards(self):
        """Возвращение логического значения у всех ли игроков остались карты"""
        for cards in self.players.values():
            if not cards:
                return False
        return True
