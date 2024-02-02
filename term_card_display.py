
def test(cardtype, attributes):
    if cardtype == 'multi':
        print(f'\n\nMultiple Choice:\n{attributes[0]}\n')
        count = 0
        answers = {}
        for option, answer in attributes[1].items():
            count += 1
            print(f'{count} ..... {option}')
            answers[count] = answer
        answer = None
        while not answer in answers.keys():
            answer = int(input('Pick the number of option\t'))
        return answers[answer]

    elif cardtype == 'gen':
        print(f'\n\nMultiple Choice:\n')
        print(f'{attributes[0]} [{" "*len(attributes[1])}] {attributes[2]}\n')
        input('Press enter to reveal\n')
        print(f'{attributes[0]} [{attributes[1]}] {attributes[2]}\n')
        correct = " "
        while not correct in "01":
            correct = input('Incorrect: 0\tCorrect: 1\t-> ')
        return bool(int(correct))

    elif cardtype == 'res':
        print(f'\n\n{attributes[0]}\n')
        input('Press enter to reveal')
        print(f'\n{attributes[1]}\n')
        correct = " "
        while not correct in "01":
            correct = input('Incorrect: 0\tCorrect: 1\t-> ')
        return bool(int(correct))
        
    else:
        raise ValueError(f'cardtype {cardtype} not valid. Cardtypes are: multi, gen, and res')
