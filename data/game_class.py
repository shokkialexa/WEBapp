from data.players_class import Players
from data.const.codes import CODES
from random import choice
from datetime import datetime
import threading


class Game:
    def __init__(self):
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

    def add(self, names_list, card_num):
        code = self.choose_url()
        cards_in_hand = card_num[1]
        cards_in_deck = card_num[0]
        self.games_map[code] = Players(cards_in_hand, cards_in_deck)
        self.is_everybody_choose[code] = False
        self.is_everybody_vote[code] = True
        self.is_self_vote[code] = {}
        self.is_self_choose[code] = {}
        self.created_time[code] = datetime.now()
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
        code = choice(CODES)
        while code in self.used_urls:
            code = choice(CODES)
        self.used_urls.append(code)
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
            self.count_places(code)
            self.assotiation[code] = None

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
        if self.is_win(code):
            return None
        return self.games_places[code][name]

    def count_places(self, code):
        progress = list(self.games_map[code].get_points().items())
        progress.sort(key=lambda x: x[1])
        places = {}
        for elem in progress:
            places[elem[0]] = len(progress) + 1
        for i in range(len(progress)):
            for j in range(i):
                if progress[i][1] == progress[j][1] and places[progress[i][0]] > j + 1:
                    places[progress[i][0]] = j + 1
        self.games_places[code] = places

    def is_win(self, code):
        progress = self.games_map[code].get_points()
        winners = []
        for name in progress.keys():
            if progress[name] >= 30:
                winners.append(name)
        if winners:
            self.delete_game(code)
            return winners
        return False

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
        self.assotiation[code] = assotiation

    def get_assotiation(self, code):
        return self.assotiation[code]

    def control_game(self, code):
        if (datetime.now() - self.created_time[code]).total_seconds() >= 7200:
            self.delete_game(code)
            return
        self.timers[code] = threading.Timer(900, self.control_game, args=(code,)).start()

    def delete_game(self, code):
        self.used_urls.remove(code)
        del self.games_map[code]
        del self.is_everybody_choose[code]
        del self.is_everybody_vote[code]
        del self.is_self_vote[code]
        del self.is_self_choose[code]
        del self.games_places[code]
        del self.assotiation[code]
        del self.created_time[code]
