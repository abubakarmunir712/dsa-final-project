def bubble_sort(cards):
    for i in range(len(cards)):
        for j in range(len(cards) - i - 1):
            if cards[j].get_rank() > cards[j+1].get_rank():
                cards[j], cards[j+1] = cards[j+1], cards[j]
    return cards

def insertion_sort(cards):
    for i in range(1, len(cards)):
        key = cards[i]
        j = i - 1
        while j >= 0 and key.get_rank() < cards[j].get_rank():
            cards[j+1] = cards[j]
            j -= 1
        cards[j+1] = key
    return cards