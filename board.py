import numpy as np
from random import randint
from ai import targetPosition

# returns the content of the incoming file converted into an array
def readBoard(file):
    board = np.loadtxt(fname=file, delimiter=",")
    return board

# returns an array of zeros with different sizes depending on the input
# input 0 = 14x22, input 1 = 14x16, input 2 = 10x12
# or 3 for a custom size
def board(type,w,h):
    if type==0:
        board=np.zeros((14,22))
    elif type==1:
        board=np.zeros((14,16))
    elif type==2:
        board=np.zeros((10,12))
    elif type==3:
        board=np.zeros((h,w))
    return board

# modify the edges of the array to be -1   
def edges(board):
    m=len(board)
    n=len(board[0])
    for i in range(n):
        if i<m:
            board[i][0]=-1
            board[i][n-1]=-1
        board[0][i]=-1
        board[m-1][i]=-1
    return board

#  -1 = stone
#  2 = enemy
#  3 = key
#  4 = link

# Add the objects and characters in random positions
# no rocks are added to the outlet column
def randomBoard(board):
    n=1
    stone=0
    enemy=0
    board[0][randint(1,len(board[0])-2)]=5
    while n<=4:
        y=randint(1,len(board)-2)
        x=randint(1,len(board[0])-2)
        if board[y][x]==0:
            if n==1:
                if stone<len(board[0]) and board[0][x]==-1:
                    board[y][x]=n*-1
                    stone+=1
                elif stone>=len(board[0]):
                    n+=1
            elif n==2:
                if enemy<1:
                    board[y][x]=n
                    enemy+=1
                else:
                    board[y][x]=-1*n
                    n+=1
            elif n==3:
                board[y][x]=n
                n+=1
            else:
                board[y][x]=n
                n+=1
    return board

# in this function we unite all the functions to create the board  
def generateRandomBoard(type,w,h):
    return randomBoard(edges(board(type,w,h))) 

# Depending on a direction (up 0, down 1, left 2, right 3) update the position of a character
def updateBoard(board,chart,way):
    pos=targetPosition(chart,board)
    if way==0:
        board[pos[0]][pos[1]]=0
        board[pos[0]-1][pos[1]]=chart
    elif way==1:
        board[pos[0]][pos[1]]=0
        board[pos[0]][pos[1]+1]=chart
    elif way==2:
        board[pos[0]][pos[1]]=0
        board[pos[0]+1][pos[1]]=chart
    elif way==3:
        board[pos[0]][pos[1]]=0
        board[pos[0]][pos[1]-1]=chart
    return board