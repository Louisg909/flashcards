

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
It is proven that more complex words and concepts are forgotten faster on the learning curve. Rather than coding something that determines the learning curve weights for each flashcard / flashcard difficulty, I can code a way for them to addapt. if I pad out this application to be larger, with flashcard sharing, These difficulty weightings can be attatched to the flashcards, as well as the addition of a user learning ability score, which is used in conjunction with the flashcard's complexity score to determine the learning curve for that user on that card. The more the flashcard is used, the complexity can be adjusted. This can be simplified when implemented to not continuously updated and adjusted when is relativty consitent. Could even have an option to input predicted complexity when first entering flashcards to give a better initial indication of the flashcard's complexity.

### How does the learning curve adapt upon relearning?
Once the learning curve is calculated, the testing should occur at 80% probabiliyu of retention, with the correctness determining the next iteration of the learning curve. The curve weightings for each user for each card should probably be saved, as this can determine how urgantly the card needs to be revised. For example, if you have a card that is set to review every 2 years, and it is late for 3 days, and a card you are set to review every day is late by 2 days, going by urgancy from due dates would favour the 2 year review, but the learning curve of the daily card would be steaper, and therefore more important to review.

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


### Problems with this method

#### The problems
- Might only really be applicable if the user strictly abides by it
- Might not be weighted correctly for user

#### How I could potentially adapt to get around these problems
For the weighting, could try and adapt it actively based on how much the user is retaining and how easy the user is getting the questions correct, aiming for 80% retention, as this is the most efficent level of learning without causing *learned helplessness*.


## Generation



[Ref]: References
[^1]: https://api.repository.cam.ac.uk/server/api/core/bitstreams/9e418506-e95e-442f-b8ea-739ed0679179/content
