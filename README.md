
# Version history and plans
## Current Version
- Mostly designed for key-word and vocabulary-based learning.
- Based of concepts shown in apps like Kinuu and Duolingo
- Custom flashcards, gamification etc
- Spaced repition, based off of adaptive learning-curves
- Terminal Based


## Past Versions

## Plans for future versions:
- Flask implementation, with interactive cards, and fun design that doesn't take away from the content, but gives it a more engaging feel.
- Adding extra features for learning concepts, rather than just vocabluary.
- Ability to share flashcards across users, and users having a learnability score which determines how quicky they learn, these two numbers are optimised to ensure everyone who learns from the cards gets around 80% retention on the learning curve.
- Card complexities and learning curves could be determined by neural networks maybe? Not sure [^1](2.4)

# Todo
- [ ] Work out how to add weights to forgetting curve
- [ ] Find out and impliment how these weights are updated upon recall, based off of the previous weightings, the date, and how many incorrect responses on the reacll (0 means got it right first time).
- [ ] Write `Card.get_retention()` function to get rentention probability percentage at a given date/today
- [x] ~Write `Stack.forgotten_date()` to find when the stack will be 'forgotten'~
- [ ] Check code for 'Stack.forgotten_date()` to ensure the estimate works, and run tests on fake data to see if I think I should use this or use Newton-Rapton (can always add it later once I get real data too as this is a non-functional feature.

[^1]: https://api.repository.cam.ac.uk/server/api/core/bitstreams/9e418506-e95e-442f-b8ea-739ed0679179/content


