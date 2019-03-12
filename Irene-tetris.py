# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 13:16:15 2019

@author: Yelena
"""
# return a four-tuple containing these four values
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    dimNum = (rows, cols, cellSize, margin)
    return dimNum #return tuple

#calculate the width and height of the screen & call run()
def playTetris():
    num = 2
    numThird = 3
    dimNum = gameDimensions()
    width = dimNum[1] * dimNum[num] + num * dimNum[numThird]
    height = dimNum[0] * dimNum[num] + num * dimNum[numThird]
    return run(width, height) 
    
# Seven "standard" pieces (tetrominoes)
iPiece = [
    [  True,  True,  True,  True ]
]
jPiece = [
    [  True, False, False ],
    [  True,  True,  True ]
]
lPiece = [
    [ False, False,  True ],
    [  True,  True,  True ]
]
oPiece = [
    [  True,  True ],
    [  True,  True ]
]
sPiece = [
    [ False,  True,  True ],
    [  True,  True, False ]
]
tPiece = [
    [ False,  True, False ],
    [  True,  True,  True ]
]
zPiece = [
    [  True,  True, False ],
    [ False,  True,  True ]
]

# draw the board 
def drawBoard(canvas, data):
    Xposition = 0
    Yposition = 0
    for row in range(data.rows):
        for col in range(data.cols):
            xPosition = col * data.cellSize
            yPosition = row * data.cellSize
            xyColor = data.board[row][col]
            drawCell(canvas, data, xPosition, yPosition, xyColor)
  
#draw the given cell using board[row][col]
def drawCell(canvas, data, rows, cols, color):
    widthNum = 3
    canvas.create_rectangle(data.margin + rows, data.margin + cols,
                            data.margin + rows + data.cellSize, 
                            data.margin + cols + data.cellSize,
                            fill = color, width = widthNum)

import random
#Create the position of the new falling piece
def newFallingPiece(data):
    divideHalfPiece = 2
    data.randomIndex = random.randint(0, len(data.tetrisPieces) - 1) 
    data.Pieces = data.tetrisPieces[data.randomIndex]  
    data.PiecesColors = data.tetrisPieceColors[data.randomIndex]  
    
    numFallingPieceCols = len(data.Pieces[0])
    numFallingPieceRows = len(data.Pieces)
    
    #set it to center subtract half the width of the falling piece
    fallingPieceRow = 0 
    fallingPieceCol = data.cellSize * \
    (data.cols//divideHalfPiece - numFallingPieceCols//divideHalfPiece)

    data.fallPie = [fallingPieceCol, fallingPieceRow, data.PiecesColors]

# The falling piece is drawn over the board
def drawFallingPiece(canvas, data):
    # Iterate over each cell in the fallingPiece
    for i in range(len(data.Pieces[0])): 
        for j in range(len(data.Pieces)): 
            # If value == True, draw it reusing drawCell() 
            if data.Pieces[j][i] == True:
                drawCell(canvas, data, data.fallPie[0] + i * data.cellSize, 
                         data.fallPie[1] + j * data.cellSize, data.fallPie[2])

#Move the falling piece according to legal test
def moveFallingPiece(data, drow, dcol): 
    #If moving down
    if drow == 0:  
        data.fallPie[0] += dcol * data.cellSize
        if fallingPieceIsLegal(data) == True:
            return True
        else:
            data.fallPie[0] -= dcol * data.cellSize  
            return False
    elif dcol == 0:
        data.fallPie[1] += drow * data.cellSize 
        if fallingPieceIsLegal(data) == True:
            return True
        else:
            data.fallPie[1] -= drow * data.cellSize
            return False

#Test if the falling piece is in legal position
def fallingPieceIsLegal(data):   
    count = 0
    count2 = 0
    for colx in range(len(data.Pieces[0])): 
        for rowy in range(len(data.Pieces)): 
            if data.Pieces[rowy][colx] == True: 
                count += 1
                if 0 <= data.fallPie[0]:
                    if data.fallPie[0] + len(data.Pieces[0]) * data.cellSize <= data.cols * data.cellSize:
                        if data.fallPie[1] + len(data.Pieces) * data.cellSize <= data.rows * data.cellSize:
                            if (data.board[data.fallPie[1]//data.cellSize + rowy][data.fallPie[0]//data.cellSize + colx] == data.emptyColor):
                                count2 += 1
    if count == count2:
        return True

#Rotate the falling piece counterclockwise
def rotateFallingPiece(data):
    num = 2
    #Store the dimensions nrows * ncols and the piece itself
    oldRowNum = len(data.Pieces) 
    oldColNum = len(data.Pieces[0]) 
    newRowNum = oldColNum 
    newColNum = oldRowNum 
    data.newTwoDimList = []
    for row in range(newRowNum): 
        data.newTwoDimList += [[None] * newColNum]          
    for col in range(oldColNum): 
        for row in range(oldRowNum): 
            if data.Pieces[row][col] == True:
                newCol = row  
                newRow = (oldColNum - 1) - col 
                data.newTwoDimList[newRow][newCol] = True   
    data.fallPie[1] += (oldRowNum//num - newRowNum//num) * data.cellSize 
    data.fallPie[0] += (oldColNum//num - newColNum//num) * data.cellSize 
    data.PiecesCase = data.Pieces
    data.Pieces = data.newTwoDimList   
    if fallingPieceIsLegal(data) == True: pass
    else:
        data.fallPie[1] -= (oldRowNum//num - newRowNum//num) * data.cellSize 
        data.fallPie[0] -= (oldColNum//num - newColNum//num) * data.cellSize 
        data.Pieces = data.PiecesCase

#paint the color on board if piece falls.     
def placeFallingPiece(data):
    for i in range(len(data.Pieces[0])): 
        for j in range(len(data.Pieces)): 
            if data.Pieces[j][i]:
                data.board[data.fallPie[1]//data.cellSize + j][data.fallPie[0]//data.cellSize + i] = data.PiecesColors
    data.board = removeFullRows(data)

#remove full rows
def removeFullRows(data):
    data.newBoard = []
    count = 0
    for row in range(data.rows):
        data.newBoard += [[data.emptyColor] * data.cols]
    for i in range(len(data.board)-1, -1, -1):
        if "blue" in data.board[i]:
            data.newBoard[i + count] = data.board[i]
        else:
            count +=1
            data.score += count
    return data.newBoard

#Draw the sign if game over
def drawGameOver(canvas, data):
    if (data.isGameOver):
        canvas.create_rectangle(data.margin, data.margin + data.cellSize,
                                data.width - data.margin, data.margin + 3 * data.cellSize,
                                fill = "black")
        canvas.create_text(data.margin + 5 * data.cellSize, data.margin + 2 * data.cellSize, text="Game Over!",
                           fill = "yellow", font="Arial 16 bold") 

#draw the score text        
def drawScore(canvas, data):
    canvas.create_text(data.width//2, data.margin//2, text= "Score " + str(data.score),
                           fill = "purple", font="Arial 16 bold") 
####################################
# customize these functions
####################################
from tkinter import *

#initialize data
def init(data):
    data.rows = gameDimensions()[0] #return intf 15
    data.cols = gameDimensions()[1] #10
    data.cellSize = gameDimensions()[2] #20
    data.margin = gameDimensions()[3] #25
    
    data.width = data.cols * data.cellSize + 2 * data.margin
    data.height = data.rows * data.cellSize + 2 * data.margin
    
    data.board = []
    data.emptyColor = "blue"
    for row in range(data.rows):
        data.board += [[data.emptyColor] * data.cols]
    
    data.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    data.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]
    
    newFallingPiece(data)
    
    data.isGameOver = False
    data.beforeIsTrue = False
    data.timerDelay = 200 # 100 millisecond == 0.1 seconds
    data.score = 0
    
def mousePressed(event, data):
    # use event.x and event.y
    pass

#set interactive keypress
def keyPressed(event, data):
    if event.keysym == "r":
        init(data)
    if event.keysym == "Left":
        moveFallingPiece(data, 0, -1)
    elif event.keysym == "Right":
        moveFallingPiece(data, 0, 1)
    elif event.keysym == "Up":
        rotateFallingPiece(data)
    elif event.keysym == "Down":
        moveFallingPiece(data, 1, 0)
   
#set timerfired
def timerFired(data):
    if not data.isGameOver:
        if moveFallingPiece(data, 1, 0) == True:           
            data.beforeIsTrue = True
        elif moveFallingPiece(data, 1, 0) == False and data.beforeIsTrue:
            placeFallingPiece(data)
            newFallingPiece(data)
            data.beforeIsTrue = False
        elif moveFallingPiece(data, 1, 0) == False and not data.beforeIsTrue:
            data.isGameOver = True
 
#draw all          
def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "orange")
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    drawGameOver(canvas, data)
    drawScore(canvas, data)

####################################
# use the run function as-is
####################################
#Run function
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

playTetris() 