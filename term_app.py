import pickle
import os
from datetime import datetime
from math import exp
from random import shuffle

from term_card_display import test as term_test
from datatypes import Queue

def current_date():
    return (datetime.now().date() - datetime(1970, 1, 1).date()).days


class Card:
    def __init__(self, title, difficulty, testing_attributes = None):
        today = current_date()
        self.halflife = difficulty
        self.title = title
        # self.confidence = 0 # condidence changes how difficult the question is - from picking an option for the blank, to blank generation, to resiting definitions <--- redundant currently, but want to add later
        self.last_studied = None
        self.today_retention = None
        self.testing_attributes = {} if testing_attributes == None else testing_attributes # {'multi':['question',{'choices':correct:bool}],'gen':['text1','generate','text2'],'res':['title','definition']}

    def set_multi(self, question: str, options: dict)-> None:
        self.testing_attributes['multi'] = [question, options]

    def set_generation(self, text1, generate, text2):
        self.testing_attributes['gen'] = [text1, generate, text2]

    def set_res(self, title, definition):
        self.testing_attributes['res'] = [title, definition]

    def __repr__(self):
        return self.title

    def study(self, correct):
        self.last_studied = time.today()
        if correct:
            self.confidence += 1
        else:
            if self.confidence > 2:
                self.confidence -= 2
            else:
                self.confidence = 0
        self.next_studied = 2 # this should be an increase on the time expotential to the confidence. - due to the forgetting curve

    def get_card(self):
        # depending on confidence, shows different type
        if self.confidence < 4: # and multichoice settings exist
            # type = multi choice
            return 'multi', self.question, self.options # options with randomised order
        elif self.confidence < 7 and not (self.generate is None): # and generation settings exist
            # type = generation
            return 'gen', self.question, self.generation
        else:
            # type = resitation
            return 'res', self.title, self.definition

    def get_retention(self, ability : float, date : datetime.date = None):
        today = datetime.today()
        t = (today - self.last_studied).days
        x = (date - today).days if date != None else 0
        retention = exp(-(x+t)/(ability * self.halflife))
        if date == None:
            self.today_retention = retention
        return retention


class Stack:
    def __init__(self,name):
        self.name = name
        self.cards = []
        self.size = 0
        self.confidence = 0
        self.next_test = None

    def add_card(self,title, definition):
        self.cards.append(Card(title, definition, self.size))
        self.size += 1

    def test_today(self, ability):

        # get list of every card in stack that has a retention today that is less or equal to 0.8
        today = datetime.today()
        cards_testing = [card for card in self.cards if card.get_retention()<=0.8]
        cards_testing.sort(key=lambda x : x.today_retention)
        cards_testing = cards_testing[10:]
        shuffle(cards_testing)
        # create study queue
        study_queue = Queue()
        [study_queue.enqueue(card) for card in card_testing]

        progress = 0
        while not study_queue.isEmpty():
            progress += 1
            print(f'{progress}/{study_queue.length}')
            # get card from queue
            card = study_queue.dequeue()
            # test card
            correct = term_test(card)
            card.study(correct)
            if not correct:
                # put to back of queue
                study_queue.enqueue(card)
                progress -= 1


    def remove_card(self,card):
        return

    def forgotten_date():
        # get weights of all of the cards in the stack - as 
        return




class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.file = f'./userdata/{username}.stack'
        if os.path.exists(f'{self.file}'):
            with open(self.file, 'rb') as f:
                self.stacks = pickle.load(f)
        else:
            self.stacks = {} # {'Stack Title': <Stack>}

    def add_stack(self,stack):
        self.stacks[stack.name] = stack

    def test(self, stack_name): # maybe better way to choose which stack to use? Not sure
        # get list of cards that need to be tested
        # test = self.stacks[stack_name].
        return

    def save(self):
        os.makedirs('/userdata', exist_ok=True)  # Create directory if it doesn't exist
        with open(self.file, 'wb') as f:
            pickle.dump(self.stacks, f)


if __name__ == '__main__':
    user = User('louisg9', 'poop')
    print(f'Welcome {user.username}!\n')
    stack = Stack('Poop')
    print(stack.cards)
    stack.add_card('Yeahhh','Wow')
    stack.add_card('Wowwww','Yeah')
    print()
    print(stack.cards)
    user.add_stack(stack)
    user.save()
    # log out and login
    user2 = User('louisg9', 'poop')
    print(f'Welcome {user2.username}!\n') # so I just added this line and the bellow line to get them to work together, but it isn't showing the saved cards. Haven't looked at what has gone wrong yet.
    for key, value in user2.stacks.items():
        print(f'{key}, {value.cards}')




