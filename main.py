from gui import gui

def main():
    game=gui()
    while True:
        board=game.startWindow()
        game.execution(board)
    
if __name__ == "__main__":
    main()
