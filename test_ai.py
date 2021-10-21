import unittest
import numpy as np
from ai import targetPosition, canExpand, manhattanDistance, changePos, nodeToExpand, goBack, expand, A_star_algorithm

def readBoard(file):
    board = np.loadtxt(fname=file, delimiter=",")
    return board

n = 50

class Test_ai(unittest.TestCase):
    
  
    def test_targetPosition(self):
        for i in range(n):
            boardT = readBoard("boards/"+ str(i) +".csv")
            boardA = readBoard("boards_answers/"+ str(i) +".csv")
            self.assertEqual(targetPosition(4,boardT),[boardA[3],boardA[4]])
    
    def test_canExpand(self):
        for i in range(n):
            boardT = readBoard("boards/"+ str(i) +".csv")
            boardA = readBoard("boards_answers/"+ str(i) +".csv")
            self.assertEqual(canExpand(targetPosition(4,boardT),boardT,4),[boardA[5],boardA[6],boardA[7],boardA[8]])
           
    def test_manhattanDistance(self):
        for i in range(n):
            boardT = readBoard("boards/"+ str(i) +".csv")
            boardA = readBoard("boards_answers/"+ str(i) +".csv")
            self.assertEqual(manhattanDistance(boardT,targetPosition(3,boardT),4),boardA[9])
                
    def test_changePos(self):
        for i in range(n):
            boardT = readBoard("boards/"+ str(i) +".csv")
            boardA = readBoard("boards_answers/"+ str(i) +".csv")
            self.assertEqual(changePos(targetPosition(4,boardT),1),[boardA[10],boardA[11]])

    def test_A_star_algorithm(self):
        for i in range(n):
            boardT = readBoard("boards/"+ str(i) +".csv")
            boardA = readBoard("boards_answers/"+ str(i) +".csv")
            self.assertEqual(A_star_algorithm(boardT,4),[boardA[0],boardA[1],boardA[2]])