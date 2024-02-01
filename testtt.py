from random import shuffle

class Card:
    def __init__(self, due_date):
        self.due = due_date

    def __repr__(self):
        return str(self.due)

    def __lt__(self, other):
        return self.due < other.due

   

#def test_today(cards):
#    today_date = 9
#    # construct dictionary of card due dates
#    today = {card.due:card for card in cards if card.due <= today_date}
#    # construct set of 10 of the most overdue cards - and randomise the order
#    if len(today) >= 10:
#        # find 10 most due cards
#        x = [key for key in today.keys()]
#        x.sort(reverse=True)
#        x2 = [today[r] for r in x]
#        today = x[:10]
#    else:
#        today = [value for value in today.values()]
#    return today

def test_today(cards):
    cards.sort()
    return cards[:10]

numbers = [n for n in range(20)] + [n for n in range(20)]
shuffle(numbers)

cards = [Card(number) for number in numbers]

print(cards)
test = test_today(cards)
print(test)
print('\n\n')
cards.sort(key=lambda x: x.due)

test.sort()
print(cards)
print(test)


