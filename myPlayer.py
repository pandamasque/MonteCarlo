# -*- coding: utf-8 -*-
from reversi import Board
import random
import time
from playerInterface import *
from math import sqrt, log
import numpy as np



class Node(object):#node that constitute the tree

    def __init__(self, p, tt, parent):
        self.tt = tt
        self.p = p
        self.childs = {}
        self.parent = parent
        

    def Backpropagation(self, p, tt):#recursively backpropagate the propability of winning 
        self.p = (self.p * self.tt + p *tt) / (self.tt + tt)
        self.tt = self.tt  + tt
        if self.parent is not None:
            self.parent.Backpropagation(p, tt)


    def Best(self):#lookup at every child and returns the best 
        best = 0
        for key in self.childs:
            if self.childs[key].p >= best:
                best = self.childs[key].p
                m = key
        return m
        

    def Expension(self, board):#expend the node based on the given board's legal moves 
        for m in board.legal_moves():
            n = Node(0,0,self)
            self.childs[(m[0], m[1], m[2])] = n



class myPlayer(PlayerInterface):


    def __init__(self, size = 10, time = 5*60, V=None):
        self.maxtime = time        
        self.size = size


    # My name is panda, and will always be
    def getPlayerName(self):
        return "PANDA"
    

    #This function set the time needed to compute the move to play
    #We need to count the time to return the answer as well
    def TimeToCompute(self):
        self.computationtime = 2*self.time/(self.size**2 - 2*self.turn) - 0.1


    #chose the move to play, by iterative deepening on an MTDf methode
    def getPlayerMove(self):
        self.initime = time.time()#mesure the time to assure to not exceed
        self.turn += 1
        self.bestmove = self.board.legal_moves()[0]
        self.TimeToCompute()#set the time to compute
        try:
            self.Choose()#launch the computation
        except TimeoutError:#An exception is raised if the computation time is over
            pass
        while (self.pushed > 0):#need to undo all the moves pushed on the board
            self.board.pop()
            self.pushed -= 1
        bestmove = self.root.Best()#seek the best move
        self.board.push([self.color, bestmove[1], bestmove[2]])#plays the move
        self.time -= time.time() - self.initime#remove the computation time
        return (bestmove[1], bestmove[2])


    def Choose(self):
        self.root = Node( 0, 0, None)#init the search tree 
        self.root.Expension(self.board)#expend for the first time the tree 
        while not (0 > self.computationtime - time.time() + self.initime):#while there is time left
            n = self.Selection(self.root)#select a node to expend
            n.Expension(self.board)
            tt, p = self.Evaluate()#evaluate the node by the rollout method
            n.Backpropagation(p, tt)#back propagate the score through the tree
            while (self.pushed > 0):#need to undo all the moves pushed on the board
                self.board.pop()
                self.pushed -= 1
        raise TimeoutError()#time's up


    def Selection(self, node):#just select a node to expand at complete random
        l = self.board.legal_moves()
        m = l[np.random.choice(np.arange(len(l)))]
        m = (m[0], m[1], m[2])
        self.Push(m)
        if len(node.childs[m].childs) == 0:
            return node.childs[m]
        else :
            return self.Selection(node.childs[m])


    def Evaluate(self):#evaluate the score of a node by rolling out 
        start = self.pushed
        win = 0
        try:
            for i in range(20):
                while not self.board.is_game_over():#we play a purely random game until it is finished
                    l = self.board.legal_moves()
                    self.Push(l[np.random.choice(np.arange(len(l)))])
                scr = self.board.get_nb_pieces()
                if self.color == self.board._BLACK:#compute who's the winner
                    vic = scr[0] < scr[1]
                else:
                    vic = scr[0] > scr[1]
                if vic:#count every victory
                    win +=1
                while (self.pushed != start):#need to undo all the moves pushed on the board
                    self.Pop()
        except TimeoutError:
            pass
        return i+1, win/(i+1)#return the score


    #This function is the same than in the given exemple
    def playOpponentMove(self, x,y):
        self.board.push([self.opponent, x, y])


    # Starts a new game, and give you your color.
    # As defined in Reversi.py : color=1 for BLACK, and color=2 for WHITE
    # Reset everything that could have been modified in a game
    def newGame(self, color):
        self.board = Board(self.size)
        self.color = color
        self.opponent = 1 if color == 2 else 2
        self.time = self.maxtime        
        self.turn = 1
        self.pushed = 0
        self.bestmove = None
        self.initime = 0
        self.computationtime = 0


    # This function is here to shows our feelings about the game
    def endGame(self, color):
        if self.color == color:
            print("YOU LOSE >:D!!!")
        else:
            print("I'M STILL CUTER THAN YOU :p")


    # This functionis used during the exploration of the tree to push the moves,
    #it allows to check for the time, and to make sure all moves will be remove in the end
    def Push(self, move):
        if (0 > self.computationtime - time.time() + self.initime):#check if we still have time to compute
            raise TimeoutError()
        self.board.push(move)
        self.pushed += 1#this count if there are modifications on the board


    # This functionis used during the exploration of the tree to pop the moves,
    #it allows to check for the time, and to make sure all moves will be remove in the end
    def Pop(self):
        self.board.pop()
        self.pushed -= 1 #this count if there are modifications on the board
        if (0 > self.computationtime - time.time() + self.initime):#check if we still have time to compute
            raise TimeoutError()