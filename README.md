# 2048_AI

an AI that plays the 2048 game, solved using [Pure Monte Carlo game search ](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search#Pure_Monte_Carlo_game_search)

![game example gif](https://i.postimg.cc/wxZKK4RX/ezgif-com-video-to-gif.gif)

## The idea
the basic idea is that for each state the game is in, we finish the game starting from that state a number of x times by taking random moves until the game is finished. We then take the best inital move from those x number of games, and take a step in our original game taking that move.

## Notes 
- you can change the number of games to complete per state by changing the value of "GAMES_TO_FINISH_PER_STATE".
- if the  value of "GAMES_TO_FINISH_PER_STATE" is 100, the game will reach the 4098 tile most of the times
## Credits
[lewisjdeane](https://github.com/lewisjdeane/2048-Game) coded the base game with amazing style!
