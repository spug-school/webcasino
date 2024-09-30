# TODO saada aikaan funktio, jonka avulla ässä voidaan valita arvolla 14 tai 1
# TODO Korjata jakajan tuloksen lasku. Ottaa tällä hetkkellä laskee jostain syystä pakan päällimmäisen kortin mukaan jakajan käteen
#      ennenaikaisesti ja laskee tällöin tuloksen väärin. Tulos on kuitenkin oikea, mutta ennenaikainen.

from random import shuffle
from time import sleep

class Ventti:
    def __init__(self):
        self.ventti = 21
        self.max_turns = 2
        self.ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K")
        self.suits = ("hertta", "ruutu", "risti", "pata")
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_turn = 0
        self.dealer_turn = 0
        self.player_total = 0
        self.dealer_total = 0
        self.player_pass = False
        self.dealer_pass = False
        self.player_over = False
        self.dealer_over = False


# Funktio paljastaa joko pelaajan tai jakajan käden
    def hand_reveal(self):
        if not self.player_pass:
            for card in self.player_hand:
                print(f"{self.player_hand.index(card) + 1} Korttisi on {card['suit']} {card['rank']}")
        else:
            for card in self.dealer_hand:
                print(f"Jakajan {self.dealer_hand.index(card) + 1} kortti on {card['suit']} {card['rank']}")

# Tällä funktiolla luodaan pakka ja sekoitetaan käyttäen randomin shuffle funktiota.
    def shuffle_deck(self):
        for i in range(len(self.suits)):
            for j in range(len(self.ranks)):
                self.deck.append({"suit":self.suits[i],"rank":self.ranks[j], "value":j+1})
                shuffle(self.deck)

# Funktio jolla jaetaan kortit jakajalle ja pelaajalle. Ajetaan vain kerran pelin alussa.
    def first_deal(self):
        self.shuffle_deck()
        for i in range(2):
            self.player_hand.append(self.deck[0])
            self.deck.remove(self.deck[0])
        for i in range(2):
            self.dealer_hand.append(self.deck[0])
            self.deck.remove(self.deck[0])

# Funktio tarkistaa onko käden arvo ylittänyt ventin ja lopettaa joko pelaajan tai jakajan vuoron.
    def over_check(self):
        if self.player_over:
            self.dealer_pass = True
        if not self.player_pass:
            if self.player_total > self.ventti:
                print("BUST!")
                self.player_pass = True
                self.player_over = True
            else:
                print(f"Sinulla on {self.player_total}!")
        else:
            if self.dealer_total > self.ventti:
                print(f"Jakajalla on {self.dealer_total}!")
                print("Jakaja ylitti ventin")
                self.dealer_pass = True
                self.dealer_over = True
            else:
                print(f"Jakajalla on {self.dealer_total}!")

# Funktio uuden kortin nostamiseen. Merkkaa myös kulkevaa vuoroa
    def hit_me(self):
        if not self.player_pass:
            if self.player_turn < self.max_turns:
                if input("Haluatko uuden kortin? k/e: ").upper() == "K":
                    self.player_hand.append(self.deck[0])
                    self.deck.remove(self.deck[0])
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
                    self.dealer_turn += 1
                else:
                    self.dealer_pass = True
            else:
                self.dealer_pass = True

# funktio jolla lasketaan pelaajan/jakajan pistetulos.
    def score_calculation(self):
        self.player_total = 0
        self.dealer_total = 0
        for p_card in self.player_hand:
            self.player_total += p_card["value"]
        for d_card in self.dealer_hand:
            self.dealer_total += d_card["value"]

# Funktio voittajan määrittelyyn.
    def is_winner(self):
        if self.player_over or self.dealer_over:
            if self.player_over:
                print("Jakaja voitti pelin")
            else:
                print("Voitit pelin")
        elif self.player_total == self.dealer_total:
            print("Jakaja voitti pelin!")
        elif self.player_total <= self.dealer_total:
            print("Jakaja voitti pelin!")
        else:
            print("Voitit pelin.")



# Tekoälyn logiikka tulee tänne.
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


# Pääfunktio pelin ajamiseen.
    def run(self):
        self.first_deal()
        while not self.player_pass:
            self.hand_reveal()
            self.score_calculation()
            self.over_check()
            self.hit_me()
            print()
        while not self.dealer_pass:
            self.hand_reveal()
            self.ai_logic()
            self.score_calculation()
            self.over_check()
            sleep(1)
            print()
        self.is_winner()

if __name__ == "__main__":
    game = Ventti()
    game.run()