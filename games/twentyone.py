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
        self.messages = []
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_turn = 0
        self.dealer_turn = 0
        self.player_total = 0
        self.dealer_total = 0
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
                               "player_pass": str(self.player_pass).lower(),
                               "message": self.messages}
                          }
        self.state_check = {"player_p": self.player_pass,
                            "dealer_p": self.dealer_pass,
                            "player_win": self.player_win,
                            "player_over": self.player_over,
                            "dealer_over": self.dealer_over}

    def shuffle_deck(self):
        for i in range(len(self.suits)):
            for j in range(len(self.ranks)):
                value = j + 1
                if self.ranks[j] in ["J", "Q", "K"]:
                    value = 10
                self.deck.append({"suit": self.suits[i], "rank": self.ranks[j], "value": value})
        shuffle(self.deck)

    def game_reset(self):
        self.messages = []
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_turn = 0
        self.dealer_turn = 0
        self.player_total = 0
        self.dealer_total = 0
        self.player_has_ace = False
        self.dealer_has_ace = False
        self.player_pass = False
        self.dealer_pass = False
        self.player_over = False
        self.dealer_over = False
        self.player_win = False


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
                self.message_manager("You have an ace. Do you want it to be 21?")
                while self.queue.empty():
                    sleep(1)
                answer = self.queue.get()
                if answer == 1:
                    self.player_has_ace = True
        for card in self.dealer_hand:
            if card["value"] == 1 and self.dealer_total + 11 <= self.twentyone and not self.dealer_has_ace:
                self.dealer_has_ace = True

    def over_check(self):
        if self.player_over:
            self.dealer_pass = True
        if not self.player_pass:
            if self.player_total > self.twentyone:
                self.message_manager("Player went over 21.")
                self.player_pass = True
                self.player_over = True
        else:
            if self.dealer_total > self.twentyone:
                self.message_manager("Dealer went over 21.")
                self.dealer_pass = True
                self.dealer_over = True
    
    def hit_me(self):
        self.player_hand.append(self.deck[0])
        self.deck.remove(self.deck[0])
        if self.player_hand[0]["value"] == 1 and not self.player_has_ace:
            if self.player_total + 11 <= self.twentyone:
                self.message_manager("You have an ace in your hand. Do you want it to have a value of 11?")
                self.to_send.put(self.get_data())
                while self.queue.empty():
                    sleep(1)
                answer = self.queue.get()
                if answer == 1:
                    self.player_has_ace = True
        self.player_turn += 1

    def dealer_hit(self):
        if self.dealer_turn < self.max_turns and not self.player_over:
            if self.dealer_total < self.player_total:
                self.dealer_hand.append(self.deck[0])
                self.deck.remove(self.deck[0])
                print(self.dealer_hand)
                if self.dealer_hand[0]["value"] == 1 and not self.dealer_has_ace:
                    if self.dealer_total + 11 <= self.twentyone:
                        self.dealer_has_ace = True
                self.dealer_turn += 1
            else:
                self.dealer_pass = True
        else:
            self.dealer_pass = True

    def message_manager(self, message):
        while len(self.messages) > 10:
            self.messages.pop(-1)
        self.messages.append(message)

    def ai_logic(self):
        print(f"Dealer is equal or more than max: {self.dealer_turn >= self.max_turns}")
        print(self.dealer_turn)
        sleep(1)
        if not self.dealer_pass:
            print("dealer pass false")
            if self.dealer_turn < self.max_turns:
                print("dealer turn less than max turns")
                if self.player_over:
                    print("Player went over 21.")
                    self.dealer_pass = True
                else:
                    if self.player_total <= self.dealer_total:
                        print("Dealer has more than player")
                        self.dealer_pass = True
                    else:

                        self.dealer_hit()
            else:
                print("dealer_pass true")
                self.dealer_pass = True

    def get_data(self):
        return self.data_dict


    def run(self):
        while self.queue.empty():
            sleep(1)
        ignore_command = self.queue.get()
        print("Command received")
        self.first_deal()
        self.message_manager("dealing cards")
        print("answer send")
        self.score_calculation()
        while not self.dealer_pass:
            while not self.player_pass:

                self.message_manager(f"Player has {self.player_total}. Do you want another card?")
                self.to_send.put(self.get_data())
                while self.queue.empty():
                    sleep(1)
                command = self.queue.get()
                if command == 1:
                    self.hit_me()
                    self.score_calculation()
                    self.over_check()
                else:
                    self.player_pass = True
            print("Dealer turn reached.")
            self.ai_logic()
            self.score_calculation()
            self.over_check()
            print(self.dealer_total)
        self.message_manager(f"dealer has {self.dealer_total}.")

        if self.player_pass and self.dealer_pass:
            if self.player_over:
                self.message_manager("Player went over 21. Player lost.")
                self.to_send.put(self.get_data())
                print("1")
            elif self.player_total < self.dealer_total <= self.twentyone:
                self.message_manager("Dealer got greater hand. Player lost.")
                self.to_send.put(self.get_data())
                print("2")
            elif self.dealer_over:
                self.message_manager("Dealer went over 21. Dealer lost.")
                self.to_send.put(self.get_data())
                print("3")