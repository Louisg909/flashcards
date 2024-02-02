import term_app as app

class Flashcard_Terminal:
    def __init__(self, confidence):
        self.stacks = []
        self.confidence = confidence # user hasn't been updated yet so not using it here, not important yet anyway - only will be once ready for multiple users.
        self.path = ''

    def help(self):
        print('Custom commands:\n\nshow_stacks() - this displays all the saved stacks\n')

    def show_stacks(self):
        if self.stacks == []:
            print('You have no stacks. Create a stack with `new_stack()`.')
        else:
            print('Stacks:')
            for n in range(len(self.stacks)):
                print(f'{n+1} .... {self.stacks[n].name}')

    def new_stack(self, name):
        self.stacks.append(app.Stack(name))
    
    def open_stack(self, index):
        print(f'Opening stack {self.stacks[index-1].name}')
        self.path = str(index-1)


if __name__=='__main__':
    term = Flashcard_Terminal(4)

    while True:
        try:
            if term.path != '':
                command = input(f'[FlashCards.py/{term.stacks[int(term.path)].name}]>> ')
                exec(f'term.stacks[int(term.path)].{command}')
            else:
                command = input('[FlashCards.py]>> ')
                exec(f'term.{command}')
        except Exception as e:
            print(f'Error. {e}')
