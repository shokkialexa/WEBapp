from data.players_class import Players
from data.const.codes import CODES
from random import choice


class Game:
    def __init__(self):
        self.games_map = {}
        self.is_everybody_choose = {}
        self.is_everybody_vote = {}
        self.is_self_vote = {}
        self.is_self_choose = {}
        self.games_places = {}
        self.assotiation = None

    def add(self, names_list, card_num):
        code = choice(CODES)
        cards_in_hand = card_num[1]
        cards_in_deck = card_num[0]
        self.games_map[code] = Players(cards_in_hand, cards_in_deck)
        self.is_everybody_choose[code] = False
        self.is_everybody_vote[code] = True
        self.is_self_vote[code] = {}
        self.is_self_choose[code] = {}
        for i in range(len(names_list)):
            if i + 1 != len(names_list):
                self.games_map[code].add(names_list[i])
            else:
                self.games_map[code].add(names_list[i], end=True)
            self.is_self_choose[code][names_list[i]] = False
            self.is_self_vote[code][names_list[i]] = True
        return code

    def who_is_directing(self, code):
        return self.games_map[code].who_is_directing()

    def get_points(self, code):
        return self.games_map[code].get_points()

    def get_names(self, code):
        return self.games_map[code].get_names()

    def somebody_vote(self, code, name, number):
        self.is_everybody_vote[code] = self.games_map[code].somebody_answer(name, number)
        self.is_self_vote[code][name] = True
        if self.is_everybody_vote[code]:
            self.is_everybody_choose[code] = False
            for name in self.games_map[code].get_names():
                self.is_self_choose[code][name] = False

    def somebody_choose(self, code, name, number):
        self.is_everybody_choose[code] = self.games_map[code].somebody_choose(name, number)
        self.is_self_choose[code][name] = True
        if self.is_everybody_choose[code]:
            self.is_everybody_vote[code] = False
            for name in self.games_map[code].get_names():
                self.is_self_vote[code][name] = False

    def is_choosing(self, code):
        return not self.is_everybody_choose[code]

    def is_choose(self, code, name):
        return self.is_self_choose[code][name]

    def is_voting(self, code):
        return not self.is_everybody_vote[code]

    def is_vote(self, code, name):
        return self.is_self_vote[code][name]

    def games_number(self):
        return len(self.games_map)

    def cards(self, code, name):
        return self.games_map[code].cards(name)

    def get_choices(self, code):
        return self.games_map[code].get_choices()

    def choosen_images(self, code):
        return self.games_map[code].image_choices()

    def players_progress(self, code):
        return self.games_map[code].get_points()

    def player_place(self, code, name):
        progress = list(self.games_map[code].get_points().items())
        progress.sort(key=lambda x: x[1])
        progress = [x[0] for x in progress]
        return progress.index(name) + 1

    def max_number_of_cards(self, code, name):
        if self.is_voting(code):
            return len(self.games_map[code].get_points())
        else:
            return len(self.games_map[code].cards(name))

    def is_valid_code(self, code):
        if self.games_map.get(code, False):
            return True
        return False

    def set_assotiation(self, code, assotiation):
        self.assotiation = assotiation

    def get_assotiation(self, code):
        return self.assotiation
