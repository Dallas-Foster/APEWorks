import random
from collections import Counter

CARD_RANKS = "23456789TJQKA"
CARD_SUITS = "cdhs"
SUIT_SYMBOLS = {
    'c': '♣',  # Club
    'd': '♦',  # Diamond
    'h': '♥',  # Heart
    's': '♠'   # Spade
}

class HandEvaluator:
    @staticmethod
    def evaluate_hand(cards):
        card_ranks = [CARD_RANKS[c // 4] for c in cards]
        card_suits = [CARD_SUITS[c % 4] for c in cards]
        rank_counts = Counter(card_ranks)
        suit_counts = Counter(card_suits)

        is_flush = max(suit_counts.values()) >= 5
        rank_values = sorted([CARD_RANKS.index(rank) for rank in rank_counts.keys()], reverse=True)
        is_straight = HandEvaluator.is_straight(rank_values)

        if is_flush and is_straight:
            return HandEvaluator.get_hand_score(rank_values, hand_type='Straight Flush')
        elif 4 in rank_counts.values():
            return HandEvaluator.get_hand_score(rank_values, hand_type='Four of a Kind')
        elif sorted(rank_counts.values()) == [2, 3]:
            return HandEvaluator.get_hand_score(rank_values, hand_type='Full House')
        elif is_flush:
            return HandEvaluator.get_hand_score(rank_values, hand_type='Flush')
        elif is_straight:
            return HandEvaluator.get_hand_score(rank_values, hand_type='Straight')
        elif 3 in rank_counts.values():
            return HandEvaluator.get_hand_score(rank_values, hand_type='Three of a Kind')
        elif list(rank_counts.values()).count(2) == 2:
            return HandEvaluator.get_hand_score(rank_values, hand_type='Two Pair')
        elif 2 in rank_counts.values():
            return HandEvaluator.get_hand_score(rank_values, hand_type='One Pair')
        else:
            return HandEvaluator.get_hand_score(rank_values, hand_type='High Card')

    @staticmethod
    def is_straight(rank_values):
        for i in range(len(rank_values) - 4):
            if rank_values[i] - rank_values[i + 4] == 4:
                return True
        if rank_values[-4:] == [12, 3, 2, 1, 0]:  # Handle Ace-low straight
            return True
        return False

    @staticmethod
    def get_hand_score(rank_values, hand_type):
        # Translate hand type to a score (placeholder implementation)
        hand_ranks = {
            'High Card': 1,
            'One Pair': 2,
            'Two Pair': 3,
            'Three of a Kind': 4,
            'Straight': 5,
            'Flush': 6,
            'Full House': 7,
            'Four of a Kind': 8,
            'Straight Flush': 9,
            'Royal Flush': 10
        }
        return hand_ranks[hand_type] * 1000 + sum(rank_values[:5])  # Example scoring

    @staticmethod
    def display_hand(cards):
        card_ranks = [CARD_RANKS[c // 4] for c in cards]
        card_suits = [SUIT_SYMBOLS[CARD_SUITS[c % 4]] for c in cards]
        return [f"{rank}{suit}" for rank, suit in zip(card_ranks, card_suits)]