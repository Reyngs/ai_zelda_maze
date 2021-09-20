import os
from board import generateRandomBoard, readBoard
from ai import A_star_algorithm

dir_name=input("Ingresa el nombre de la carpeta donde se almacenaran los tableros: ")

try:
    os.mkdir(dir_name)
    os.mkdir(dir_name+"_answers")
except OSError:
    print("Fallo la creacion del directorio %s" % dir_name)

n=int(input("Ingrese numero de tableros a generar: "))
s=int(input(" --------------------------\n 0 for small board (10x8).\n 1 for medium board (14x12).\n 2 for big board (20x12).\n 3 for custom size board.\n:"))
w=0
h=0
if s==3:
    print(" --------------------------\n Custom size")
    w=int(input(" w:"))+2
    h=int(input(" h:"))+2

i=-1
while i+1 < n:
    i+=1
    board=generateRandomBoard(s,w,h)
    file_name=str(i)+".csv"
    f=open(dir_name + "/" + file_name, 'w')
    text=""
    for j in range(len(board)):
        for k in range(len(board[0])):
            text+=str(board[j][k])
            if k<len(board[0])-1:
                text+=", "
        text+="\n"
    f.write(text)
    f.close()

    answer_Astar=A_star_algorithm(readBoard(dir_name + "/" + file_name),4)

    if answer_Astar==[0,0,0] or answer_Astar[2]==4:
        i-=1
        continue

    f=open(dir_name + "_answers" + "/" + file_name, 'w')
    text=str(answer_Astar)
    f.write(text)
    f.close()