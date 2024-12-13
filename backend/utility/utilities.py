from typing import List
from classes.card import Card


def bubble_sort(cards: List[Card]):
    for i in range(len(cards)):
        for j in range(len(cards) - i - 1):
            if cards[j].get_rank() > cards[j + 1].get_rank():
                cards[j], cards[j + 1] = cards[j + 1], cards[j]
    return cards


def insertion_sort(cards: List[Card]):
    for i in range(1, len(cards)):
        key = cards[i]
        j = i - 1
        while j >= 0 and key.get_rank() < cards[j].get_rank():
            cards[j + 1] = cards[j]
            j -= 1
        cards[j + 1] = key
    return cards


def find_max_rank(cards: List[Card], can_be_joker):
    cards = bubble_sort(cards)
    for i in range(len(cards) - 1, -1, -1):

        if (
            cards[i].get_rank() != 1
            and cards[i].get_rank() != 14
            and (not cards[i].is_joker() or can_be_joker)
        ):
            return cards[i].get_rank()
    return -1


def find_min_rank(cards: List[Card], can_be_joker):
    cards = bubble_sort(cards)
    for i in range(len(cards)):
        if (
            cards[i].get_rank() != 14
            and cards[i].get_rank() != 1
            and (not cards[i].is_joker() or can_be_joker)
        ):
            return cards[i].get_rank()
    return -1