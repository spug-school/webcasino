from random import shuffle
import queue
from time import sleep


class TwentyOne:
    def __init__(self):

        # game options
        self.queue = queue.Queue()
        self.to_send = queue.Queue()
        self.twentyone = 21
        self.max_turns = 3
        self.ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
        self.suits = ("hearts", "diamonds", "cross", "spades")
        self.message = ""
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_turn = 0
        self.dealer_turn = 0
        self.player_total = 0
        self.dealer_total = 0
        self.ask_player_ace = False
        self.player_has_ace = False
        self.dealer_has_ace = False
        self.player_pass = False
        self.dealer_pass = False
        self.player_over = False
        self.dealer_over = False
        self.player_win = False
        self.data_dict = {"data":
                              {"dealer_hand": self.dealer_hand,
                              "player_hand": self.player_hand,
                               "message": self.message}
                          }

    def shuffle_deck(self):
        for i in range(len(self.suits)):
            for j in range(len(self.ranks)):
                value = j + 1
                if self.ranks[j] in ["J", "Q", "K"]:
                    value = 10
                self.deck.append({"suit": self.suits[i], "rank": self.ranks[j], "value": value})
        shuffle(self.deck)

    def score_calculation(self):
        self.player_total = 0
        self.dealer_total = 0
        if self.player_has_ace:
            self.player_total += 11
        if self.dealer_has_ace:
            self.dealer_total += 11
        for p_card in self.player_hand:
            self.player_total += p_card["value"]
        for d_card in self.dealer_hand:
            self.dealer_total += d_card["value"]

    def first_deal(self):
        self.shuffle_deck()
        for i in range(2):
            self.player_hand.append(self.deck[0])
            self.deck.remove(self.deck[0])
        for i in range(2):
            self.dealer_hand.append(self.deck[0])
            self.deck.remove(self.deck[0])
        self.score_calculation()
        for card in self.player_hand:
            if card["value"] == 1 and self.player_total + 11 <= self.twentyone and not self.player_has_ace:
                self.message = "You have an ace. Do you want it to ha a value of 11?"
                self.to_send.put(1)
                while self.queue.empty():
                    sleep(1)
                if self.queue.get() == 1:
                    self.player_has_ace = True
        for card in self.dealer_hand:
            if card["value"] == 1 and self.dealer_total + 11 <= self.twentyone and not self.dealer_has_ace:
                self.dealer_has_ace = True

    def over_check(self):
        if self.player_over:
            self.dealer_pass = True
        if not self.player_pass:
            if self.player_total > self.twentyone:
                self.player_pass = True
                self.player_over = True
        else:
            if self.dealer_total > self.twentyone:
                self.dealer_pass = True
                self.dealer_over = True
    
    def hit_me(self):
        if not self.player_pass:
            if self.player_turn < self.max_turns:
                self.message = "Do you want another card?"
                while self.queue.empty():
                    sleep(1)
                if self.queue.get() == 1:
                    self.player_hand.append(self.deck[0])
                    self.deck.remove(self.deck[0])
                    if self.player_hand[0]["value"] == 1 and not self.player_has_ace:
                        if self.player_total + 11 <= self.twentyone:
                            self.message = "You have an ace. Do you want it to ha a value of 11?"
                            self.to_send.put(1)
                            while self.queue.empty():
                                sleep(1)
                            if self.queue.get() == 1:
                                self.player_has_ace = True
                    self.player_turn += 1
                else:
                    self.player_pass = True
            else:
                self.player_pass = True
        else:
            if self.dealer_turn < self.max_turns and not self.player_over:
                if self.dealer_total < self.player_total:
                    self.dealer_hand.append(self.deck[0])
                    self.deck.remove(self.deck[0])
                    if self.dealer_hand[0]["value"] == 1 and not self.dealer_has_ace:
                        if self.dealer_total + 11 <= self.twentyone:
                            self.dealer_has_ace = True
                    self.dealer_turn += 1
                else:
                    self.dealer_pass = True
            else:
                self.dealer_pass = True

    def ai_logic(self):
        if not self.dealer_pass:
            if self.dealer_turn < self.max_turns:
                if self.player_over:
                    self.dealer_pass = True
                else:
                    if self.player_total <= self.dealer_total:
                        self.dealer_pass = True
                    else:
                        self.hit_me()
            else:
                self.dealer_pass = True

    def get_data(self):
        return self.data_dict

    def run(self):
        self.message = "Game has started"
        self.first_deal()
        self.score_calculation()
        print(self.data_dict)
        
        while not self.player_pass:
            self.score_calculation()
            self.over_check()
            self.hit_me()

        # dealers turn
        while not self.dealer_pass:
            self.score_calculation()
            self.over_check()
            self.ai_logic()