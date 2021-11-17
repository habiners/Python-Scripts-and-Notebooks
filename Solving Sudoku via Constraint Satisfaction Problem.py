def printSudokuBoard(board):
    for x in range(9):
        for y in range(9):
            print(board[x][y], end="")
            if y == 2 or y == 5:
                print("|", end="")
        print("")
        if x == 2 or x == 5:
            print("-----------")

def printDomains(board):
    print("Printing Domains")
    for x in range(9):
        for y in range(9):
            print(f"Domains in {x,y}:", end=" ")
            print(type(board[x][y]), end=" ")
            print(board[x][y])

def printConstraining(board):
    for x in range(9):
        for y in range(9):
            print(board[x][y], end=" ")
            if y == 2 or y == 5:
                print(" | ", end="")
        print("")
        if x == 2 or x == 5:
            print("-----------")

def isValidAndSolved(board):
    # Check All Cols
    for col in range(9):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for row in range(9):
            if board[row][col] in numbers:
                numbers.remove(board[row][col])
        if len(numbers) != 0:
            return False
    # Check All Rows
    for row in range(9):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for col in range(9):
            if board[row][col] in numbers:
                numbers.remove(board[row][col])
        if len(numbers) != 0:
            return False
    # Check All 3x3s
    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for y in range(3):
                for x in range(3):
                    if board[row + y][col + x] in numbers:
                        numbers.remove(board[row + y][col + x])
            if len(numbers) != 0:
                return False
    return True

def checkIfSolved(board):
    if isValidAndSolved(board):
        print("SOLVED")
        printSudokuBoard(board)
        return True
    return False

def getDomainsWithSmallest(board, row, col, smollest):
    possibleDomains = [1,2,3,4,5,6,7,8,9]

    # Check the column
    for y in range(9):
        if board[y][col] in possibleDomains:
            possibleDomains.remove(board[y][col])

    # Check the row
    for x in range(9):
        if board[row][x] in possibleDomains:
            possibleDomains.remove(board[row][x])

    # Check 3x3
    refX = 6 if col >= 6 else 3 if col >= 3 else 0
    refY = 6 if row >= 6 else 3 if row >= 3 else 0
    for y in range(3):
        for x in range(3):
            if board[refY + y][refX + x] in possibleDomains:
                possibleDomains.remove(board[refY + y][refX + x])

    # Get most constrained
    if len(possibleDomains) and len(possibleDomains) < smollest[0]:
        smollest[0] = len(possibleDomains) 
        smollest[1] = row
        smollest[2] = col

    return possibleDomains

def mostConstrainedVariable(board, solved):
    if not solved[0]:
        domains = [[list() for i in range(9)] for j in range(9)] # Initialize 2D Array with lists
        smollest = [10, -1, -1] # [0] is # of domains, [1] is row, [2] is column

        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    domains[row][col] = getDomainsWithSmallest(board, row, col, smollest)

        for inputDomain in domains[smollest[1]][smollest[2]]:
            if not solved[0]:
                board[smollest[1]][smollest[2]] = inputDomain

                time.sleep(0.1) # Delay para dili instant
                solved[0] = checkIfSolved(board)

                mostConstrainedVariable(board, solved)
        if not solved[0]:
            board[smollest[1]][smollest[2]] = 0

def getDomains(board, row, col):
    possibleDomains = [1,2,3,4,5,6,7,8,9]

    # Check the column
    for y in range(9):
        if board[y][col] in possibleDomains:
            possibleDomains.remove(board[y][col])

    # Check the row
    for x in range(9):
        if board[row][x] in possibleDomains:
            possibleDomains.remove(board[row][x])

    # Check 3x3
    refX = 6 if col >= 6 else 3 if col >= 3 else 0
    refY = 6 if row >= 6 else 3 if row >= 3 else 0
    for y in range(3):
        for x in range(3):
            if board[refY + y][refX + x] in possibleDomains:
                possibleDomains.remove(board[refY + y][refX + x])
    
    return possibleDomains

def getConstraining(board, domains, row, col, most):
    constraining = list()

    # Check the column
    for y in range(9):
        if board[y][col] == 0 and [y, col] not in constraining:
            constraining.append([y, col])

    # Check the row
    for x in range(9):
        if board[row][x] == 0 and [row, x] not in constraining:
            constraining.append([row, x])

    # Check 3x3
    refX = 6 if col >= 6 else 3 if col >= 3 else 0
    refY = 6 if row >= 6 else 3 if row >= 3 else 0
    for y in range(3):
        for x in range(3):
            if board[refY + y][refX + x] == 0 and [refY + y, refX + x] not in constraining:
                constraining.append([refY + y, refX + x])
    
    constraining.remove([row, col]) # Remove itself
    if len(constraining) > most[0] and domains[row][col]:
        most[0] = len(constraining)
        most[1] = row
        most[2] = col
    return len(constraining)

def mostConstrainingVariable(board, solved):
    if not solved[0]:
        domains = [[list() for i in range(9)] for j in range(9)] # Initialize 2D Array with lists
        constraining = [[0 for i in range(9)] for j in range(9)] # Initialize 2D Array with numbers
        most = [-1, -1, -1]

        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    domains[row][col] = getDomains(board, row, col)
                    constraining[row][col] = getConstraining(board, domains, row, col, most)

        for inputDomain in domains[most[1]][most[2]]:
            if not solved[0]:
                board[most[1]][most[2]] = inputDomain
                solved[0] = checkIfSolved(board)

                mostConstrainingVariable(board, solved)
        if not solved[0]:
            board[most[1]][most[2]] = 0

def bruteforce(board): # Testing
    domains = [[list() for i in range(9)] for j in range(9)] # Initialize 2D Array with lists

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                domains[row][col] = getDomains(board, row, col)

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for inputDomain in domains[row][col]:
                    board[row][col] = inputDomain
                    checkIfSolved(board)
                    bruteforce(board)
                board[row][col] = 0

import tkinter as tk
from threading import Thread
import time

def main():
    def applyTestCases(n):
        for row in range(9):
            for col in range(9):
                entry_board[row][col].delete(0, tk.END)
                if n == 0: # Very easy
                    entry_board[row][col].insert(0, testcaseVeryEasy[row][col])
                elif n == 1: # Easy
                    entry_board[row][col].insert(0, testcaseEasy[row][col])
                elif n == 2: # Normal
                    entry_board[row][col].insert(0, testcase[row][col])
                elif n == 3: # Clear
                    entry_board[row][col].insert(0, "")
                elif n == 4: # Set to 0
                    entry_board[row][col].insert(0, 0)
                else: # In case??? idk man
                    entry_board[row][col].insert(0, testcase2[row][col])
    
    def updateUI(currentBoard): # Ref: https://www.reddit.com/r/learnpython/comments/ffrv5e/while_true_loop_in_tkinter/
        for row in range(9):
            for col in range(9):
                label_solutionboard[row][col].configure(text=currentBoard[row][col])
        window.update()
        window.after(100, lambda: updateUI(currentBoard)) # Default is 200

    def cspHeader(currentBoard, mode):
        for y in range(9):
            for x in range(9):
                currentBoard[x][y] = int(entry_board[x][y].get())
        print("User Input:")
        printSudokuBoard(currentBoard)
        button_solve_mostconstrained.configure(state=tk.DISABLED)
        button_solve_mostconstraining.configure(state=tk.DISABLED)

        if mode == 1:
            mostConstrainedVariable(currentBoard, [False])
        else:
            mostConstrainingVariable(currentBoard, [False])

        button_solve_mostconstrained.configure(state=tk.NORMAL)
        button_solve_mostconstraining.configure(state=tk.NORMAL)

    currentBoard = [[0 for i in range(9)] for j in range(9)] # Initialize 2D Array with numbers
    padding = 5
    window = tk.Tk(className=" Constraint Satisfaction Problem - Sudoku")
    window.geometry("640x480")
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)

    # Main Frame
    frame = tk.Frame(master=window)
    frame.grid(row=0, column=0, padx=padding, pady=padding, ipadx=padding, ipady=padding, sticky=tk.NSEW)
    for i in range(19):
        frame.grid_columnconfigure(i, minsize=20, weight=1)
    for i in range(16):
        frame.grid_rowconfigure(i, minsize=20, weight=1)

    # Main Frame Widgets==================================================
    # Row 0
    label_testcases = tk.Label(master=frame, text="Test Cases")
    label_testcases.grid(row=0, column=0, columnspan=8, sticky=tk.EW)

    # Row 1
    button_veryeasy = tk.Button(master=frame, text="Very Easy", borderwidth=1, command=lambda: applyTestCases(0))
    button_veryeasy.grid(row=1, column=0, columnspan=3, sticky=tk.EW)
    button_easy = tk.Button(master=frame, text="Easy", borderwidth=1, command=lambda: applyTestCases(1))
    button_easy.grid(row=1, column=3, columnspan=3, sticky=tk.EW)
    button_normal = tk.Button(master=frame, text="Normal", borderwidth=1, command=lambda: applyTestCases(2))
    button_normal.grid(row=1, column=6, columnspan=3, sticky=tk.EW)

    label_solutions = tk.Label(master=frame, text="Solution:")
    label_solutions.grid(row=1, column=10, columnspan=8, sticky=tk.EW)

    # Row 12
    button_clear = tk.Button(master=frame, text="Clear/Empty", borderwidth=1, command=lambda: applyTestCases(3))
    button_clear.grid(row=12, column=0, columnspan=4, sticky=tk.EW)
    button_setzero = tk.Button(master=frame, text="Set All To Zero", borderwidth=1, command=lambda: applyTestCases(4))
    button_setzero.grid(row=12, column=5, columnspan=4, sticky=tk.EW)

    # Row 14
    button_solve_mostconstrained = tk.Button(master=frame, text="Solve Using Most Constrained", borderwidth=1, command=lambda:Thread(target=lambda:cspHeader(currentBoard, 1)).start())
    button_solve_mostconstrained.grid(row=14, column=0, columnspan=4, sticky=tk.EW)
    button_solve_mostconstraining = tk.Button(master=frame, text="Solve Using Most Constraining", borderwidth=1, command=lambda:Thread(target=lambda: cspHeader(currentBoard, 2)).start())
    button_solve_mostconstraining.grid(row=14, column=5, columnspan=4, sticky=tk.EW)

    # Input Board==================================================
    # Border
    label_board_border = [[tk.Label(master=frame, borderwidth=1, relief="solid") for y in range(3)] for x in range(3)]
    for y in range(3):
        for x in range(3):
            label_board_border[x][y].grid(row=(x*3)+2, column=(y*3), rowspan=3, columnspan=3, sticky=tk.NSEW)
    # Input board
    entry_board = [[tk.Entry(master=frame, width=3) for y in range(9)] for x in range(9)]
    for y in range(9):
        for x in range(9):
            entry_board[x][y].insert(tk.END, "0")
            entry_board[x][y].grid(row=x+2, column=y, columnspan=1)

    # Solution Board==================================================
    # Border
    label_solutionboard_border = [[tk.Label(master=frame, borderwidth=1, relief="solid") for y in range(3)] for x in range(3)]
    for y in range(3):
        for x in range(3):
            label_solutionboard_border[x][y].grid(row=(x*3)+2, column=(y*3)+10, rowspan=3, columnspan=3, sticky=tk.NSEW)

    # Solution board
    label_solutionboard = [[tk.Label(master=frame, width=1, anchor=tk.CENTER) for y in range(9)] for x in range(9)]
    for y in range(9):
        for x in range(9):
            label_solutionboard[x][y].configure(text="0")
            label_solutionboard[x][y].grid(row=x+2, column=y+10, columnspan=1)

    updateUI(currentBoard)
    window.mainloop()

testcase = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]
testcase2 = [
    [1, 0, 0, 2, 0, 0, 0, 5, 0],
    [0, 0, 4, 0, 6, 0, 0, 3, 1],
    [0, 8, 0, 0, 0, 0, 0, 2, 9],

    [6, 0, 5, 8, 7, 4, 0, 0, 0],
    [0, 3, 0, 1, 0, 0, 0, 0, 8],
    [0, 4, 0, 0, 0, 0, 9, 0, 0],
    
    [9, 0, 0, 0, 0, 7, 0, 6, 2],
    [0, 0, 0, 3, 0, 8, 7, 0, 5],
    [0, 2, 0, 0, 0, 9, 0, 0, 0],
]
testcaseEasy = [
    [5, 0, 9, 0, 0, 0, 4, 0, 0],
    [7, 0, 8, 3, 0, 4, 9, 0, 0],
    [6, 0, 1, 0, 0, 0, 7, 3, 0],

    [4, 6, 2, 5, 3, 9, 0, 0, 0],
    [3, 8, 5, 7, 2, 1, 6, 4, 9],
    [1, 9, 7, 4, 6, 8, 2, 0, 0],

    [2, 0, 0, 1, 0, 0, 0, 0, 4],
    [0, 0, 3, 0, 4, 0, 0, 8, 7],
    [0, 7, 0, 0, 5, 3, 0, 0, 6],
]
testcaseVeryEasy = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],

    [2, 3, 1, 6, 7, 4, 8, 9, 5],
    [8, 7, 5, 9, 1, 2, 3, 6, 4],
    [6, 9, 4, 5, 3, 8, 2, 1, 7],

    [3, 1, 7, 2, 6, 5, 9, 4, 8],
    [5, 4, 2, 8, 9, 7, 6, 3, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

main()
