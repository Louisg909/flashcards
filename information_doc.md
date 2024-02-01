

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


Problem with normal methods is they aren't adaptive, I have looked at a paper to learn about other methods:

### Adaptive Forgetting Curves for Spaced Repetition Language Learning


### Problems with this method

#### The problems
- Might only really be applicable if the user strictly abides by it
- Might not be weighted correctly for user

#### How I could potentially adapt to get around these problems
For the weighting, could try and adapt it actively based on how much the user is retaining and how easy the user is getting the questions correct, aiming for 80% retention, as this is the most efficent level of learning without causing *learned helplessness*.


## Generation



[Ref]: References
[^1]: https://api.repository.cam.ac.uk/server/api/core/bitstreams/9e418506-e95e-442f-b8ea-739ed0679179/content
