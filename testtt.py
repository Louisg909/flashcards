#from random import shuffle
#
#class Card:
#    def __init__(self, due_date):
#        self.due = due_date
#
#    def __repr__(self):
#        return str(self.due)
#
#    def __lt__(self, other):
#        return self.due < other.due
#
#   
#
##def test_today(cards):
##    today_date = 9
##    # construct dictionary of card due dates
##    today = {card.due:card for card in cards if card.due <= today_date}
##    # construct set of 10 of the most overdue cards - and randomise the order
##    if len(today) >= 10:
##        # find 10 most due cards
##        x = [key for key in today.keys()]
##        x.sort(reverse=True)
##        x2 = [today[r] for r in x]
##        today = x[:10]
##    else:
##        today = [value for value in today.values()]
##    return today
#
#def test_today(cards):
#    cards.sort()
#    return cards[:10]
#
#numbers = [n for n in range(20)] + [n for n in range(20)]
#shuffle(numbers)
#
#cards = [Card(number) for number in numbers]
#
#print(cards)
#test = test_today(cards)
#print(test)
#print('\n\n')
#cards.sort(key=lambda x: x.due)
#
#test.sort()
#print(cards)
#print(test)


from datetime import datetime, timedelta # timedelta will be redundant after testing
import math

class Card:
    def __init__(self, difficulty, daysago):
        self.halflife : float = 0.2 # intialised at some value based off of predicted difficulty
        self.date_last_tested = datetime.today()-timedelta(days=daysago) # temp to simulate past date)

    def days_since_tested(self):
        return (datetime.today()-self.date_last_tested).days

class Stack:
    def __init__(self, *cards):
        self.cards = [card for card in cards] # Card(0.3,4),Card(0.2,10),Card(0.6,3)]

    def forget_regression_estimate(self, ability):
        # initialise the x values, and find their y values
        lnPn = lambda cards, x: sum(math.e**(-(x+card.days_since_tested())/(ability*card.halflife)) for card in cards) / len(cards)
        x1 = [-1, 0, 7, 30]
        y1 = [lnPn(self.cards, x) for x in x1]
        xy = sum(x1[n]*y1[n] for n in range(4))

        # linear regression on these values:
        m = ( 4*xy-sum(x1)*sum(y1) )/( 4*sum(x**2 for x in x1)-sum(x1)**2 )
        c = (sum(y1) - m*sum(x1))/4

        # finding x when P(x)~0.01
        return (1/m) * (math.log(0.01)-c)

class User:
    def __init__(self):
        self.ability = 4
        self.stacks = {'Physics_Quantum':Stack}

    def forget_stack(self, stack_name:str):
        return self.stacks[stack_name].forget(self.ability)

    def add_stack(self,stack_name,stack):
        self.stacks[stack_name] = stack

    def forget(self,stack_name):
        return self.stacks[stack_name].forget_regression_estimate(self.ability)

if __name__ == '__main__':
    user = User()
    stack_cheese = Stack(Card(0.02,3),Card(0.8,30),Card(0.3,1))
    stack_physics= Stack(Card(0.1,2),Card(0.5,2),Card(0.8,5),Card(0.7,2))
    stack_ameera = Stack(Card(0.4,2),Card(0.7,4),Card(0.8,10))
    user.add_stack('Cheese', stack_cheese)
    user.add_stack('Physics' , stack_physics)
    user.add_stack('Ameera', stack_ameera)
    for stack in ['Cheese', 'Physics', 'Ameera']:
        print(user.forget(stack))


