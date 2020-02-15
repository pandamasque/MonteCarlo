# -*- coding: utf-8 -*-
import time
import reversi
from random import choice
from playerInterface import *

class myPlayer(PlayerInterface):

    def __init__(self):
        pass

    def getPlayerName(self):
        return "Human Player"

    def getPlayerMove(self):
        print("input x,y")
        i = input()
        c = i.split(',')
        return (int(c[0]),int(c[1]))

    def playOpponentMove(self, x,y):
        pass

    def newGame(self, color):
        pass

    def endGame(self, winner):
        pass