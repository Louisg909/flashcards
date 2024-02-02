

# Maths and logic


## Forgetting curve and spaced reptition

The **Half-Life Regression model** is a method I think I could use to determine the length between the repetitions of flash cards, based of user performance and timed reviews.[^1]

The model is defined by the expression:
$$p = 2^{-\frac{t}{h}}$$
where:
- $p$ is the probability of recall
- $t$ is the time since the item was last seen
- $h$ is the half-life, or the strength of the learner's memory.

The estimated half life ($\hat{h}$) is defined as:
$$\hat{h} = 2^{x\beta}$$
where:
- $x$ is the vector of features
- $\beta$ is the vector of weights for the features
The features would be the individual concepts and key words being tested.

The HLR model is trained using the following loss function:
```math
\ell \left(x; \beta\right) \left(p-\hat{p}_\beta\right)^2 +\left(h-\hat{h}_\beta\right)^2 +\lambda \left | \left | \beta \right | \right | ^2_2
```
In practice, it is found that optimising for $p$ and $h$ in the loss function improved the model. The true value of $h$ is defined as $\frac{-t}{\log(p)}$. $p$ and $\hat{p}_\beta$ are the true probability and model estimated probability of recall, respectively.



Problem with normal methods is they aren't adaptive, I have looked at a paper to learn about other methods:

### Adaptive Forgetting Curves for Spaced Repetition Language Learning
It is proven that more complex words and concepts are forgotten faster on the forgetting curve. Rather than coding something that determines the forgetting curve weights for each flashcard / flashcard difficulty, I can code a way for them to addapt. if I pad out this application to be larger, with flashcard sharing, These difficulty weightings can be attatched to the flashcards, as well as the addition of a user learning ability score, which is used in conjunction with the flashcard's complexity score to determine the forgetting curve for that user on that card. The more the flashcard is used, the complexity can be adjusted. This can be simplified when implemented to not continuously updated and adjusted when is relativty consitent. Could even have an option to input predicted complexity when first entering flashcards to give a better initial indication of the flashcard's complexity.

### How does the forgetting curve adapt upon relearning?
Once the forgetting curve is calculated, the testing should occur at 80% probabiliyu of retention, with the correctness determining the next iteration of the forgetting curve. The curve weightings for each user for each card should probably be saved, as this can determine how urgantly the card needs to be revised. For example, if you have a card that is set to review every 2 years, and it is late for 3 days, and a card you are set to review every day is late by 2 days, going by urgancy from due dates would favour the 2 year review, but the forgetting curve of the daily card would be steaper, and therefore more important to review.

### Basically I want the following:

<table>
<tr><td>
<table>
<tr><th>User</th></tr>
<tr><td>- <code>user_data : Dict</code> <br> - <code>user_ability : Double</code> <br> - <code>stacks : List</code> </td></tr>
<tr><td> - <code>test_stack(stack:String)->Void </code></td></tr>
</table>
</td><td>
<table>
<tr><th>Card</th></tr>
<tr><td> - <code>tests : Dict</code> <br> - <code>complexity : Double</code> <br> - <code>curve_weights</code> </td></tr>
<tr><td> - <code>set_tests()->Void</code> <br> - <code>test()</code> <br> - <code>study(correct:Bool)->Void</code> <br> - <code>get_retention()->Double</code></td></tr>
</table>
</td><td>
<table>
<tr><th>Stack</th></tr>
<tr><td> - <code>name : String</code> <br> - <code>cards : List[Card]</code> <br> - <code>confidence : Double</code> <br> - <code>size : Int</code> </td></tr>
<tr><td> - <code>add_card(card:Card)->Void </code> <br> - <code>remove_card(card:String)->Void</code> <br> - <code>test()->Void</code> <br> - <code> forgotten_date()->Int </td></tr>
</table>
</td></tr>
</table>


> Notes about attributes and methods:
> - `Card.tests` includes all three of the testing methods: *Multiple Choice*, *Generation*, and *Recall*.
> - `Stack.confidence` could be a confidence score, or I just had an idea to have it as how many days it would take for the average curve of all the cards in the stack to go bellow a certain percentage (aka, be forgotten)
> - `Stack.test()` looks through all of the cards in the stack and compiles a queue of the ones that have a probability of retention for that day of 80% or less, and then sorts them by this retention percentage, testing the user for the cards with the least retention probability, reajusting each of their curves based off of whether they were answered correctly or not. After testing, can update the stack confidence? If a card is marked as wrong, it gets moved to the back of the queue, and the count of how many times it went wrong for that one test gets increased by 1. This continues untill the current testing queue is empty.
> - `Stack.forgotten_date()` takes all the forgetting curve dates of the cards in the stack, and uses this to say when the retention percentage of the stack goes bellow a certain percentage - can be arbitarily set to something like 5% for now.

The todo list to achieve this is:
- [ ] Work out how to add weights to forgetting curve
- [ ] Find out and impliment how these weights are updated upon recall, based off of the previous weightings, the date, and how many incorrect responses on the reacll (0 means got it right first time).
- [ ] Write `Card.get_retention()` function to get rentention probability percentage at a given date/today
- [ ] Write `Stack.forgotten_date()` to find when the stack will be 'forgotten'

#### Writing `Card.get_retention()`
##### Maths
With a retention probabilty for a card of $p\left(x,h\right)=e^{-\frac{x}{kh}}$, where $x$ is days into the future, $h$ is the knowledge half-life (which is what gets addapted the more a person learns it), and $k$ is the user's ability.

The curves for each card are defined by $p\left(x+t,h\right)$, where $h$ is the current knowledge half-life of the card, and $t$ is the time since the card was last studied.

The curve for the full stack can be worked out with the function:
```math
P\left(t\right)=\sum_{n=0}^{N}\left(e^{-\frac{t_{n}}{kh_{n}}}\right)
```
Where $N$ is the number of cards in the stack.

I want a good estimated value. To do this, I can do some linear regression on the logarithmic scale as the function of P(t) is based of expotentials and will roughly match it. To do this, I will find the values of $$\ln\left(P(-1)\right)$, $$\ln\left(P(0)\right)$, $$\ln\left(P(7)\right)$, and $\ln\left(P(30)\right)$. I will then will take a simple linear regression:
```math
\ln\left(P(x)\right)~mx+c
```
and:
```math
m=\frac{N\sum xy-\left(\sum x\right)\left(\sum y\right)}{N\sum x^{2}-\left(\sum x\right)^{2}}
```
```math
c=\frac{\sum y-m\sum x}{N}
```
We can then rearrange the equation to get $x=\frac{1}{m}\left(\ln\left(P(x)\right)-c\right)$, and $P(x)$ can be substituted with the value of $0.05$, where the equation will give an estimate of x. This value can then be put through the original equation to see how close it is. If it is within the boundaries of $\pm 0.01$, we will keep it as the value. If not, I will continue on with the method by

For now, I think this is more than good enough - later on down the line, I might find that, to efficiently find the value of 0.05, I should use the Newton-Raphson method. To do this, I would need to use the derivative of the stack's retention function:
```math
P'\left(x\right)=-\frac{1}{N}\sum_{n=0}^{N}\left(\frac{1}{kh_{n}}e^{-\frac{x+t_{n}}{kh_{n}}}\right)
```

##### Coding
To impliment this into code, I first will ensure the `Card` class has all the correct weightings for the forgetting curve:
```python
from datetime import date
class Card:
    self.halflife : float = 0.2 # intialised at some value based off of predicted difficulty
    self.date_last_tested : date
    
    def days_since_tested(self):
        return (date.today()-self.date_last_tested).days
```
Then this can be used, in the `Stack` class, to make the regression estimate:
```python
import math

class Stack:
    self.cards : list[Card]

    def forget_regression_estimate(self, ability):
        # initialise the x values, and find their y values
        lnPn = lambda cards, x: sum(math.e**(-(x+card.days_since_tested())/(ability*card.halflife)) for card in cards) / len(cards)
        x1 = [-1, 0, 7, 30]
        y1 = [lnPn(x) for x in x1]
        xy = sum(x1[n]*y1[n] for n in range(4))

        # linear regression on these values:
        m = ( 4*xy-sum(x1)*sum(y1) )/( 4*sum(x**2 for x in x1)-sum(x)**2 )
        c = (sum(y1) - m*sum(x1))/4

        # finding x when P(x)~0.01
        return (1/m) * (math.ln(0.01)-c)
```

```python
class User:
    self.ability : float
    self.stacks : dict['stack_name':Stack]

    def forget_stack(self, stack_name:str):
        return self.stacks[stack_name].forget(self.ability)
```

After testing, these give very weird values so will need to look back on them.


#### Writing `Card.get_retention()`
##### Aim of function
This function is to get rentention probability at a given date/today. I think, for now at least, it will take an input of a datetime date and will output the retention probability.
| Card |
| ---- |
| - `get_retention(date : datetime.date)-> retention : float` |

##### Logic and coding
This just takes into account the one equation's forgetting curve, so only has to work with a few weights so will be quite efficent. The weights are defined to make the equation:
```math
p(x) = e^{-\frac{x+t_{n}}{k\ h_{n}}}
```
And these are all values stored, so this can easily just be evaluated:
```python
from math import exp
from datetime import datetime, timedelta

class Card:
    def __init__(self, hl, daysago):
        self.halflife = hl
        self.last_studied = datetime.today() - timedelta(days=daysago) # just for testing
    
    def get_retention(self, date : datetime.date, ability : float):
        today = datetime.today()
        t = (today - self.last_studied).days
        x = (date - today).days
        return exp(-(x+t)/(ability * self.halflife))
```


#### Updating the weightings of the forgetting curve


### Problems with this method

#### The problems
- Might only really be applicable if the user strictly abides by it
- Might not be weighted correctly for user

#### How I could potentially adapt to get around these problems
For the weighting, could try and adapt it actively based on how much the user is retaining and how easy the user is getting the questions correct, aiming for 80% retention, as this is the most efficent level of learning without causing *learned helplessness*.


## Generation



[Ref]: References
[^1]: https://api.repository.cam.ac.uk/server/api/core/bitstreams/9e418506-e95e-442f-b8ea-739ed0679179/content
