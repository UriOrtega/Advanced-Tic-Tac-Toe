from ezgraphics import GraphicsWindow
from ezgraphics import GraphicsCanvas
import random

def drawBoxes(canvas):
    # Variables to name and hold box values
    count = 1
    boxInfo=[]
    
    # Repeats 3 times for x
    for x in range(0,3):
        # And 3 times for y
        for y in range (0,3):
            box = {"name": count}
            
            # Generates the coordinates for the corner of the box (multiplied by 300 because window = 900)
            xPos = x * 300
            yPos = y * 300
            
            # Saves the coordinates of the box onto a list
            box["topLeft"] = [xPos, yPos]
            box["botRight"] = [xPos + 300, yPos + 300]
            
            # Creates the box onto the canvas
            canvas.drawRect(xPos,yPos,300,300)
            
            # Creates the coordinate for text, which is in the middle of the box
            box["textPos"] = [xPos + 150, yPos + 150]
            
            # Will be used to store either X or O depending on which player chooses it
            box["value"] = ""
            
            # Adds the box to the larger list, then resets it for the next one
            boxInfo.append(box)
            del box            
            count += 1
    
    # Returns list of boxes
    return (boxInfo)

def playChoice(pt):
    # Gets coordinate of where player clicked
    coords = [pt[0],pt[1]]
    
    # Checks all boxes to see in which one the player clicked
    for box in boxInfo:
        # X and Y value of the top left corner
        xTop = box["topLeft"][0]
        yTop = box["topLeft"][1]
        
        # X and Y value of the bottom right corner
        xBot = box["botRight"][0]
        yBot = box["botRight"][1]
        
        # Sees if the pointer is between the top corner
        if (coords[0] >= xTop) and (coords[0] <= xBot):
            # and the lower corner 
            if (coords[1] >= yTop) and (coords[1] <= yBot):
                # Returns the box which holds the pointer
                return box
def getBoard():
    global boxInfo
    
    # Records the game state of the board
    board = []
    
    # Records a column of boxes
    boxCol = []
    
    # Counts to 3 boxes per column
    count3 = 0
    for box in boxInfo:
        if count3 == 3:
            board.append(boxCol)
            boxCol = []
            count3 = 0
            
        boxCol.append(box["value"])
        count3 += 1            
    # One final append for the last column
    board.append(boxCol)
    return board
    
def checkWin():
    board = getBoard()
    # Records whether X or O won the game
    winValue = ""
        
    # Checking columns for win
    for x in range(0,3):
        # Checks if first box of column is empty, will ignore column 
        if (board[x][0] != ""):
            # Checks if all values of a column are equal
            if (board[x][0] == board[x][1] and board[x][0] == board[x][2]):
                winValue = board[x][0]
        if (board[0][x] != ""):
            # Checks if all values of a row are equal
            if (board[0][x] == board[1][x] and board[0][x] == board[2][x]):
                winValue = board[0][x]
    
    # If columns and rows do not match, we check diagonals
    if (winValue == "" and board[1][1] != ""):
        if(board[0][0] == board[1][1] and board[0][0] == board[2][2]):
            winValue = board[1][1]
        elif(board[0][2] == board[1][1] and board[0][2] == board[2][0]):
            winValue = board[1][1]
    
    # Checking for draw
    boxCount = 0
    for y in range(0,3):
        for val in board[y]:
            if (val == "X" or val == "O"):
                boxCount += 1
    if boxCount == 9:
        winValue = "DRAW"

    return winValue

# Random Computer Function
def compPlayer():
    global box
    while (box["value"] != ""):
        # Generates a random point in the range of the grid
        xPos = random.randint(0,900)
        yPos = random.randint(0,900)
        pt = (xPos,yPos)
        
        # Checkes if the box is open
        box = playChoice(pt)
    return box

# Smart Super Computer Player
def superCompPlayer():
    # Get board state
    global boxInfo
    board = getBoard()
    
    # Getting names of each box into same layout as board
    boxName = []
    boxCol = []
    count3 = 0
    for box in boxInfo:
        if count3 == 3:
            boxName.append(boxCol)
            boxCol = []
            count3 = 0
            
        boxCol.append(box["name"])
        count3 += 1            
    # One final append for the last column
    boxName.append(boxCol)
    
    # Checks if middle space is open
    if (board[1][1] == ""):
        return boxInfo[4]
    
    # Name of open space
    openBox = ""
    # Checking for optimal play
    for x in range(0,3):
        # Tracks the amount of x's and o's
        countX = 0
        countO = 0        
        
        # Count values in a column to see if theres two and an open space
        for idx,y in enumerate(board[x]):
            if (y == "X"):
                countX += 1
            elif (y == "O"):
                countO += 1
            elif (y == ""):
                    openX = x
                    openY = idx
            
        # Check if there are two values in a column that match
        if (countX + countO != 3):
            if(countX == 2 or countO== 2):
                openBox = boxName[openX][openY]
                break
        
        countX = 0
        countO = 0
                
        if (openBox == ""):
            #Getting a row
            rowTrack = []
            rowTrack.append(board[0][x])
            rowTrack.append(board[1][x])
            rowTrack.append(board[2][x])
            
            # Count values in a row to see if theres two and an open space
            for idx,y in enumerate(rowTrack):
                if (y == "X"):
                    countX += 1
                elif (y == "O"):
                    countO += 1
                elif (y == ""):
                    openX = idx
                    openY = x
            
            # Check if there are two values in a row that match
            if (countX + countO != 3):
                if(countX == 2 or countO== 2):
                    openBox = boxName[openX][openY]
                    break
                
    # If columns and rows do not match, we check diagonals
    if (openBox == ""):
        # Getting the middle value
        middleValue = board[1][1]
        
        # Getting cornor values
        corners = []
        corners.append(board[0][0])
        corners.append(board[2][0])
        corners.append(board[2][2])
        corners.append(board[0][2])
        
        # Variables to track which corner is open and its position in the array
        cornerX = 5
        cornerY = 5
        cornerInd = 5
        for count, x in enumerate(corners):
            # Comparing each corner to middle value
            if x == middleValue:
                # If a corner matches, see if opposite corner is open
                try:
                    if(corners[count + 2] == ""):
                        cornerInd = count + 2
                        break
                except:
                    try:
                        if(corners[count - 2] == ""):
                            cornerInd = count - 2
                            break
                    except:
                        pass
                    
        # Determining which corner is open
        if cornerInd == 0:
            cornerX = 0
            cornerY = 0
        elif cornerInd == 1:
            cornerX = 2
            cornerY = 0
        elif cornerInd == 2:
            cornerX = 2
            cornerY = 2
        elif cornerInd == 3:
            cornerX = 0
            cornerY = 2
        if (cornerX != 5 and cornerY != 5):
            openBox = boxName[cornerX][cornerY]
    # If there is an optimal play, find that boxes infor
    if (openBox != ""):
        for box in boxInfo:
            if box["name"] == openBox:
                return box
    # Else, random play
    else:
        box = compPlayer()
        return box
# Determining which mode the user would like to play
try:
    mode
except NameError:
    try:
        mode = int(input("Which mode would you like to play?: \n1: User vs User\n2: User vs Computer\n3: User vs Super Computer\n"))
    except:
        print("Please enter a number matching the mode you want to play.")

# Variables to track if someone won, turn count, and whos turn it is
win = 0
turnCount = 0
playerTurn = 1

# Variables for window dimension
win_width = 900
win_height = 1000

# Creating window
window = GraphicsWindow(win_width, win_height)
window.setTitle("Tic Tac Toe")

# Creating canvas
canvas = window.canvas()

# Drawing boxes onto canvas
boxInfo = drawBoxes(canvas)

# Info box to display information
canvas.drawRect(300, 910, 300, 75)
textID = canvas.drawText(400,950, "Player 1: Your turn")

while win == 0:
    if (playerTurn == 1 or mode == 1):
        # Creating pointer event listener
        pt = window.getMouse()
        
        # Get the box the pointer is in 
        box = playChoice(pt)
        
        # Get text position of box
        xPos = box["textPos"][0]
        yPos = box["textPos"][1]
    # Checks if its a computer mode
    elif (playerTurn == 2):
        if (mode == 2):            
            box = compPlayer()
            xPos = box["textPos"][0]
            yPos = box["textPos"][1]
        if (mode == 3):
            box =superCompPlayer()
            xPos = box["textPos"][0]
            yPos = box["textPos"][1]
        
    # If the box has already been chosen, prints onto console
    if (box["value"] != ""):
        canvas.removeItem(textID)
        textID = canvas.drawText(350, 950, "This square has already been chosen")
        
    # If its Player ones turn, prints X onto box
    elif (playerTurn == 1):
        canvas.drawText(xPos, yPos, "X")
        box["value"] = "X"
        
        # Switches to second players turn
        playerTurn = 2
        canvas.removeItem(textID)
        textID = canvas.drawText(400,950, "Player 2: Your turn!")
    
    # If its Player twos turn, checks which mode user is playing
    elif (playerTurn == 2):
        canvas.drawText(xPos, yPos, "O")
        box["value"] = "O"
    
        # Switches to first players turn
        playerTurn = 1
        canvas.removeItem(textID)
        textID = canvas.drawText(400,950, "Player 1: Your turn!")         
    
    # Adds one to turn count
    turnCount += 1
    
    #After turn 5, which is the earliest possible win turn, check if there is a winner
    if(turnCount >= 5):
        winValue = checkWin()
    
        # If there is a winning value, break loop
        if(winValue != ""):
            win = 1
            
# Checks what the winning value is and announces the winner or draw if necessary. 
if (winValue == "X"):
    canvas.removeItem(textID)
    textID = canvas.drawText(400,950, "Player 1 has won the game!")

if (winValue == "O"):
    canvas.removeItem(textID)
    textID = canvas.drawText(400,950, "Player 2 has won the game!")

if (winValue == "DRAW"):
    canvas.removeItem(textID)
    textID = canvas.drawText(400,950, "Draw. Try again.")

window.wait()
