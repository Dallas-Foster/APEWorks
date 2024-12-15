import numpy as np
import random
from HandEvaluator import HandEvaluator

class PokerEnv:
    def __init__(self):
        # Initialize deck, players, and state
        self.deck = [i for i in range(52)]
        self.reset()

    def reset(self):
        # Reset game state
        self.deck = [i for i in range(52)]
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.opponent_hand = [self.deck.pop(), self.deck.pop()]
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.done = False
        return self.get_state()

    def step(self, action):
        # Action: 0 = Fold, 1 = Call, 2 = Raise
        if action == 0:  # Fold
            reward = -1 * self.pot
            self.done = True
        elif action == 1:  # Call
            self.pot += self.current_bet
            if len(self.community_cards) < 5:
                self.add_community_card()
            if len(self.community_cards) == 5:
                reward = self.resolve_hand()
                self.done = True
            else:
                reward = 0
        elif action == 2:  # Raise
            self.current_bet += 10
            self.pot += self.current_bet
            reward = 0
        return self.get_state(), reward, self.done

    def add_community_card(self):
        if len(self.community_cards) < 5:
            self.community_cards.append(self.deck.pop())

    def resolve_hand(self):
        # Evaluate hands and determine winner
        player_score = HandEvaluator.evaluate_hand(self.player_hand + self.community_cards)
        opponent_score = HandEvaluator.evaluate_hand(self.opponent_hand + self.community_cards)
        if player_score > opponent_score:
            return self.pot
        else:
            return -1 * self.pot

    def get_state(self):
        # Return state representation including player hand, community cards, pot, and current bet
        return np.array(self.player_hand + self.community_cards + [self.pot, self.current_bet])