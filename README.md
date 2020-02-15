# Monte-Carlo-powered reversi player

This is reversi player that uses monte carlo method in order to compute the move to play.
 
## Using the interface

This program have a very simple interface (coded by Larent Simon) that allows to do a match against the player. You just have to launch the main.py. Then the game will start, displaying the board and playing for the monte carlo program.

### Controls

Once you can play, the program will display the possible moves you can play, you just have to enter the choosen coordinates to place a stone. 


## Limitations

The computation time is limited, and therefor the number of rollout is too. The probleme is that, with the slowness of python and the reversi implementation that is a little bit slow, it is hard to do more than 300 simulations each turn, counting 5 minutes for a 10 by 10 board. So most humans will win.  

## How it works

This is a simplistic implementation of a monte carlo algorithm, with a purely random choice other the moves in the tree exploration.