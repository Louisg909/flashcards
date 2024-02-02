from term_card_display import test as term_test
from term_app import Card

if __name__ == '__main__':
    card1 = Card('Card Title', 0.8)
    card1.set_multi('What is a card?', {'Something in a stack':True, 'Poop':False, 'Yehaw':False,'Yellow':False})
    card1.set_generation('The sweet, adorable', 'Ameera', 'is the most beautiful girl ever.')
    card1.set_res('Winchester','A city in the united kingdom, used to be the capital of the kingdom of wessex.')
    #correct = term_test('multi', card1.testing_attributes['multi'])
    #correct = term_test('gen', card1.testing_attributes['gen'])
    correct = term_test('res', card1.testing_attributes['res'])
    print(correct)
