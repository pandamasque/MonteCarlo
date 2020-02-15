import reversi
import myPlayer
import humanPlayer
import time

b = reversi.Board(10)

players = []
player1 = myPlayer.myPlayer()
player1.newGame(b._BLACK)
players.append(player1)
player2 = humanPlayer.myPlayer()
player2.newGame(b._WHITE)
players.append(player2)

totalTime = [0,0] # total real time for each player
nextplayer = 0
nextplayercolor = b._BLACK
nbmoves = 1

print(b.legal_moves())
while not b.is_game_over():
    print("Referee Board:")
    print(b)
    print("Before move", nbmoves)
    print("Legal Moves: ", b.legal_moves())
    nbmoves += 1
    otherplayer = (nextplayer + 1) % 2
    othercolor = b._BLACK if nextplayercolor == b._WHITE else b._WHITE
    
    currentTime = time.time()
    move = players[nextplayer].getPlayerMove()
    print(("[Player "+str(nextplayer) + "] "))
    totalTime[nextplayer] += time.time() - currentTime
    print("Player ", nextplayercolor, players[nextplayer].getPlayerName(), "plays " + str(move))
    (x,y) = move 
    if not b.is_valid_move(nextplayercolor,x,y):
        print(otherplayer, nextplayer, nextplayercolor)
        print("Problem: illegal move")
        break
    b.push([nextplayercolor, x, y])
    players[otherplayer].playOpponentMove(x,y)

    nextplayer = otherplayer
    nextplayercolor = othercolor

    print(b)

print("The game is over")
print(b)
(nbwhites, nbblacks) = b.get_nb_pieces()
print("Time:", totalTime)
print("Winner: ", end="")
if nbwhites > nbblacks:
    print("WHITE")
elif nbblacks > nbwhites:
    print("BLACK")
else:
    print("DEUCE")
