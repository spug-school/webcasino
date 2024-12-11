from random import shuffle
from time import sleep
from ..Game import Game
from typing import override

class Twentyone(Game):
    def __init__(self, player: object, db_handler: object):
        super().__init__(player, db_handler, self.__class__.__name__.lower())

        # Game specific attributes
        self.ventti = 21
        self.max_turns = 3
        self.ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
        self.suits = ("hertta", "ruutu", "risti", "pata")
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


# Nollaa kaikki pelin arvot
    def game_stat_reset(self):
        self.deck.clear()
        self.player_hand.clear()
        self.dealer_hand.clear()
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

# Funktio paljastaa joko pelaajan tai jakajan käden
    def hand_reveal(self):
        print()
        if not self.player_pass:
            for card in self.player_hand:
                print(f"{self.player_hand.index(card) + 1}. kätesi kortti on {card['suit']} {card['rank']}")
        else:
            for card in self.dealer_hand:
                print(f"Jakajan {self.dealer_hand.index(card) + 1}. kortti on {card['suit']} {card['rank']}")

# Tällä funktiolla luodaan pakka ja sekoitetaan käyttäen randomin shuffle funktiota.
    def shuffle_deck(self):
        for i in range(len(self.suits)):
            for j in range(len(self.ranks)):
                value = j + 1
                if self.ranks[j] in ["J", "Q", "K"]:
                    value = 10
                self.deck.append({"suit": self.suits[i], "rank": self.ranks[j], "value": value})
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
        self.score_calculation()
        for card in self.player_hand:
            if card["value"] == 1 and self.player_total + 13 <= self.ventti and not self.player_has_ace:
                if input("Sinulla on ässä! Muunnetaanko sen arvo 14? (k / e): ").upper() == "K":
                    self.player_has_ace = True
        for card in self.dealer_hand:
            if card["value"] == 1 and self.dealer_total + 13 <= self.ventti and not self.dealer_has_ace:
                self.dealer_has_ace = True

# Funktio tarkistaa onko käden arvo ylittänyt ventin ja lopettaa joko pelaajan tai jakajan vuoron.
    def over_check(self):
        if self.player_over:
            self.dealer_pass = True
        if not self.player_pass:
            if self.player_total > self.ventti:
                print("Yli meni!")
                self.player_pass = True
                self.player_over = True
            else:
                print(f"Kätesi on yhteensä {self.player_total}!")
        else:
            if self.dealer_total > self.ventti:
                print(f"Jakajan käsi on yhteensä {self.dealer_total}!")
                print("Jakajalla meni yli!")
                self.dealer_pass = True
                self.dealer_over = True
            else:
                print(f"Jakajan käsi on yhteensä {self.dealer_total}!")   
        print()

# Funktio uuden kortin nostamiseen. Merkkaa myös kulkevaa vuoroa
    def hit_me(self):
        if not self.player_pass:
            if self.player_turn < self.max_turns:
                if input("Nostetaanko kortti? (k / e): ").upper() == "K":
                    self.player_hand.append(self.deck[0])
                    self.deck.remove(self.deck[0])
                    if self.player_hand[0]["value"] == 1 and not self.player_has_ace:
                        if self.player_total + 13 <= self.ventti:
                            print("Kädessäsi on seuraavat kortit: ")
                            for card in self.player_hand:
                                print(card["rank"] + " of " + card["suit"])
                            if input("Muunnetaanko ässän arvo 14? (k / e): ").upper() == "K":
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
                        if self.dealer_total + 13 <= self.ventti:
                            self.dealer_has_ace = True
                    self.dealer_turn += 1
                else:
                    self.dealer_pass = True
            else:
                self.dealer_pass = True

# funktio jolla lasketaan pelaajan/jakajan pistetulos.
    def score_calculation(self):
        self.player_total = 0
        self.dealer_total = 0
        if self.player_has_ace:
            self.player_total += 13
        if self.dealer_has_ace:
            self.dealer_total += 13
        for p_card in self.player_hand:
            self.player_total += p_card["value"]
        for d_card in self.dealer_hand:
            self.dealer_total += d_card["value"]

# Funktio voittajan määrittelyyn.
    def is_winner(self, bet: int) -> int:
        if self.player_over or self.dealer_over:
            if self.player_over:
                print("Jakaja voitti pelin!\n")
            else:
                winnings = bet * 2
                print(f"Onnittelut! Voitit pelin ja {winnings} pistettä!\n")
                self.player_win = True
                return winnings  # return the winnings
        else:
            if self.player_total <= self.dealer_total:
                print("Jakaja voitti pelin!")
            else:
                winnings = bet * 2
                print(f"Onnittelut! Voitit pelin ja {winnings} pistettä!\n")
                self.player_win = True
                return winnings  # return the winnings
         
        return 0 # return 0 if the player lost

# Pelin logiikka tulee tänne.
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
    @override
    def start_game(self) -> dict:
        '''
        Game specific logic for: Twentyone
        '''
        
        self.game_stat_reset()
        
        bet = self.get_bet(self.player.get_balance())
        
        # start the game
        self.first_deal()
        
        # the players turn
        while not self.player_pass:
            self.hand_reveal()
            self.score_calculation()
            self.over_check()
            self.hit_me()
            
        # dealers turn
        while not self.dealer_pass:
            self.hand_reveal()
            self.score_calculation()
            self.over_check()
            sleep(1)
            self.ai_logic()
            sleep(1)
        
        outcome = self.is_winner(bet)
        
        return {
            'won': outcome > 0,
            'win_amount': outcome,
            'bet': bet
        }