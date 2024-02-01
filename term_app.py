import pickle
import os
from datetime import datetime

def current_date():
    return (datetime.now().date() - datetime(1970, 1, 1).date()).days


class Card:
    def __init__(self, title, definition, id_no):
        today = current_date()
        self.title = title
        self.definition = definition
        self.confidence = 0 # condidence changes how difficult the question is - from picking an option for the blank, to blank generation, to resiting definitions
        self.last_studied = None
        self.due = today
        self.generate = None
        self.question = None
        self.options = None

    def set_multi(self, question: str, options: dict)-> None:
        self.question = question
        self.options = options # options = [{'question':'option1', 'corect':False}, {'question':'option2', 'correct':True},...]

    def set_generation(self, q1, h1, q2):
        self.generation = {q1, h1, q2}

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


# 789461086002:

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

    def test_today(self):
        def test(card):
            card_type, x, y = card.get_card()
            # display card and check if correct or wrong
            if card_type == 'multi':
                # display card as multi with the question and render template
                print(f'\n\nCard:\n{x}')
                # randomise option order
                random.shuffle(y)
                for n in range(len(y)):
                    print(f'{n+1} ... {y[n]}') # In flask, each of these will be submit fields? Or multiple choice selection - radio type?
                option = int(input('\nEnter choice:'))

            elif card_type == 'gen':
                pass
            else:
                pass
            correct : bool = True
            card.study(correct)

        self.cards.sort()
        self.next_test = self.cards[:10]

        # display them one at a time
        for card in today:
            test(card)

    def remove_card(self,card):
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
        test = self.stacks[stack_name].

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




