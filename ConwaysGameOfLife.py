from random import randint
from os import system, name, remove, path
from time import sleep
import sys 

###Are we writing to a log file?
write = False


###Defines a cell object that has coordinates and a state
class Cell:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
    
    def __str__(self):
        stateString = ["dead","living"][self.state]
        return f"A {stateString} cell with the coordinates ({self.x},{self.y})"
    
    #returns if the parent cell is dead or alive where True is alive and False is dead
    def isAlive(self):
        return self.state

    #sets the current state of the parent cell to dead or alive where True is alive and False is dead 
    def setState(self, state):
        self.state = state
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    

###Prints the game board
def printGame(game, logFile):
    global write
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 


    
    for i in game:
        for j in i:
            if j.isAlive():
                print("☺", end='')
                if write:
                    print("☺", end='', file=logFile)
            else:
                print(" ", end='')
                if write:
                    print(" ", end='', file=logFile)
        print("")
        if write:
            print("", file=logFile)


###Returns the amount of living neighbors around any given cell
def amountOfNeighbors(game, cell):
    originX = cell.getX()
    originY = cell.getY()
    totalAlive = 0

    #checking cells in the current x column
    if originY + 1 < len(gameBoard) and game[originX][originY + 1].isAlive():
        totalAlive += 1
    if originY - 1 >= 0 and game[originX][originY - 1].isAlive():
        totalAlive += 1

    #checking cells in the x column to the left
    if originX - 1 >= 0:
        if game[originX - 1][originY].isAlive():
            totalAlive += 1
        if originY - 1 >= 0 and game[originX - 1][originY - 1].isAlive():
            totalAlive += 1
        if originY + 1 < len(gameBoard) and game[originX - 1][originY + 1].isAlive():
            totalAlive += 1
    
    #checking cells in the x column to the right
    if originX + 1 < len(gameBoard[0]):
        if game[originX + 1][originY].isAlive():
            totalAlive += 1
        if originY - 1 >= 0 and game[originX + 1][originY - 1].isAlive():
            totalAlive += 1
        if originY + 1 < len(gameBoard) and game[originX + 1][originY + 1].isAlive():
            totalAlive += 1

    return totalAlive
    
    



while True:
    gameBoard = []
    sideLength = 20
    for i in range(sideLength):
        row = []
        for j in range(sideLength):
            choice = randint(0,1)
            if choice == 0:
                row.append(Cell(j, i, False))
            else:
                row.append(Cell(j,i,True))
        gameBoard.append(row)

    if path.exists("log.txt"):
        remove("log.txt")


    with open('log.txt', 'a') as f:
        gameIsActive = True
        reasonForGameOver = "There was an error somewhere..."
        changes = []
        pastBoards = []
        while gameIsActive:
            printGame(gameBoard, f)
            sleep(0.1)
            totalDead = 0
            totalChanges = 0
            for i in range(len(gameBoard)):
                for j in range(len(gameBoard[i])):
                    currentCell = gameBoard[i][j]
                    if write:
                        print(f"Working on: {currentCell}", file=f)
                    originalBoard = gameBoard
                    neighborCount = amountOfNeighbors(originalBoard, currentCell)
                    if write:
                        print(f"Cell has {neighborCount} neighbors", file=f)
                    if currentCell.isAlive():
                        if neighborCount < 2 or neighborCount > 3:
                            totalChanges += 1
                            currentCell.setState(False)
                            if write:
                                print(f"Cell was killed...", file=f)
                    else:
                        totalDead += 1
                        if neighborCount == 3:
                            totalChanges += 1
                            currentCell.setState(True)
                            if write:
                                print(f"Cell was birthed", file=f)
            changes.append(totalChanges)
            pastBoards.append(originalBoard)
            try:
                if totalDead == (sideLength ** 2):
                    gameIsActive = False
                    reasonForGameOver = "All the cells died..."
                elif changes[-1] == 0 and changes[len(changes) - 1] == 0:
                    gameIsActive = False
                    reasonForGameOver = "Cells have reached equilibrium"
            except:
                continue
            

        print(reasonForGameOver)
        if write:
            print(reasonForGameOver, file=f)
        sleep(2)
                