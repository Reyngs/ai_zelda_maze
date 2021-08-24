import pygame, os, sys
from board import generateRandomBoard, readBoard, updateBoard
from ai import A_start_algorithm, randomWay
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class gui:
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # This is the simple window for choose the board
    def startWindow(self):
        pygame.display.set_caption("Choose your board")
        background_init = pygame.image.load('media/background_Init.png')
        pygame.init()
        window = pygame.display.set_mode((960, 660))
        while True:
            window.blit(background_init, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                board=generateRandomBoard(0,0,0)
                return board
            if keys[pygame.K_b]:
                board=generateRandomBoard(1,0,0)
                print(board)
                return board
            if keys[pygame.K_c]:
                board=generateRandomBoard(2,0,0)
                return board
            if keys[pygame.K_o]:
                Tk().withdraw()
                fileName = askopenfilename()
                board=readBoard(fileName)
                return board
            pygame.display.update()
            pygame.time.delay(100)

    # In "execution" pygame shows graphically the board 
    # and in turn executes the AI functions to change 
    # the board and that in each cycle it changes
    def execution(self, board):
        pygame.display.set_caption("ai - Zelda")
        board_Backup=board
        empty = pygame.image.load('media/block_Empty.png')
        stone = pygame.image.load('media/block_Full.png')
        key = pygame.image.load('media/key.gif')
        link = pygame.image.load('media/link.gif')
        enemy = pygame.image.load('media/zol.gif')
        pygame.init()
        window = pygame.display.set_mode((60*len(board[0]), 60*len(board)))
        count=0
        while True:
            pygame.time.delay(1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            for i in range(len(board)):
                for j in range(len(board[0])):
                    window.blit(empty, (j*60,i*60))
                    if board[i][j]==-1:
                        window.blit(stone, (j*60,i*60))
                    if board[i][j]==2 or board[i][j]==-2:
                        window.blit(enemy, (j*60,i*60))
                    if board[i][j]==3:
                        window.blit(key, (j*60,i*60))
                    if board[i][j]==4:
                        window.blit(link, (j*60,i*60))
            pygame.display.update()
            Enemy1=A_start_algorithm(board,2)
            if Enemy1[0]==0:
                break
            board=updateBoard(board,2,Enemy1[2])
            board=updateBoard(board,-2,randomWay(board,-2))
            Link=A_start_algorithm(board,4)
            if Link[0]==0:
                break
            board=updateBoard(board,4,Link[2])
            fuente = pygame.font.Font(None, 30)
            text = "Turn: {}, Total nodes Link: {}, Total nodes Enemy1: {}".format(count, Link[1], Enemy1[1])
            mensaje = fuente.render(text, 1, (255, 255, 255))
            window.blit(mensaje, (15, 25))
            pygame.display.flip()
            count+=1
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                board=board_Backup
            if keys[pygame.K_b]:
                break