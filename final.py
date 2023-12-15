#!/usr/bin/env pyhton3
__author__ = "Sam Danforth"

import random
import time

from PyQt5 import QtWidgets, QtGui
from crapsUI import Ui_MainWindow


# Initializes the window by hiding unneeded widgets, updating the ui, and setting bet limits
def startupProcess():
    ui.winStatus.hide()
    ui.numberToRollFor.hide()
    ui.bankBalance.setText(f"Bank Balance: ${bankBalance:.2f}")
    ui.currentBet.setMinimum(1)
    ui.currentBet.setMaximum(int(bankBalance))
    ui.winCounter.setText(f"Wins: {winCount}")
    ui.lossCounter.setText(f"Losses: {lossCount}")


# Connects the functional widgets to functions to make game playable, only 2 at the moment
def connectFunctions():
    ui.rollDie.clicked.connect(chooseRandomRoll)
    ui.menuFile.triggered.connect(startNewGame)


# Chooses random number for each die rolled, and calls other functions needed for gameplay
def chooseRandomRoll():
    firstDieRoll = random.randint(1, 6)
    secondDieRoll = random.randint(1, 6)
    updateGui(firstDieRoll, secondDieRoll)
    totalRoll = firstDieRoll + secondDieRoll
    determineWin(totalRoll)


# Updates the ui so dice show correct number and shows the total number rolled by the player
def updateGui(firstDieRoll, secondDieRoll):
    ui.dieFace1.setPixmap(QtGui.QPixmap(f"number{firstDieRoll}.png"))
    ui.dieFace2.setPixmap(QtGui.QPixmap(f"number{secondDieRoll}.png"))
    totalRoll = firstDieRoll + secondDieRoll
    ui.numberToRollFor.setText(f"You rolled: {totalRoll}")
    ui.numberToRollFor.show()
    QtGui.QGuiApplication.processEvents()


# Determines win or lose status
def determineWin(totalRoll):
    global firstRoll, lastNumber
    if firstRoll:  # Checks if first roll of the game, important to determine win or loss
        if totalRoll in [7, 11]:  # 7 or 11 on first roll is immediate win
            playerWin(1)
        elif totalRoll in [2, 3, 12]:  # 2, 3, or 12 on first roll is immediate loss
            playerLoss()
        else:
            firstRoll = False
            lastNumber = totalRoll
            ui.rollNumber.setText("Second Roll")
    else:
        if totalRoll == lastNumber:  # Second roll total must be same as first for win
            payoutRatio = calculatePayout()
            playerWin(payoutRatio)
        else:
            playerLoss()


# Calculates how much to pay winning player
def calculatePayout():
    global lastNumber
    payoutRates = {4: 2, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 12}
    payoutRate = payoutRates[lastNumber]
    return payoutRate


# Executes on player win, resets game
def playerWin(payoutRatio):
    global firstRoll, bankBalance, winCount
    firstRoll = True
    ui.winStatus.setText("You Won!")
    ui.winStatus.show()
    amountToPay = ui.currentBet.value() * payoutRatio
    bankBalance += amountToPay
    winCount += 1
    ui.currentBet.setMaximum(int(bankBalance))
    ui.bankBalance.setText(f"Bank Balance: ${bankBalance:.2f}")
    ui.winCounter.setText(f"Wins: {winCount}")
    ui.rollDie.setDisabled(True)
    QtGui.QGuiApplication.processEvents()
    time.sleep(3)
    ui.winStatus.hide()
    ui.rollNumber.setText("First Roll")
    ui.rollDie.setEnabled(True)


# Executes on player loss, resets game
def playerLoss():
    global firstRoll, bankBalance, lossCount
    firstRoll = True
    ui.winStatus.setText("You Lost!")
    ui.winStatus.show()
    amountToDeduct = ui.currentBet.value()
    bankBalance -= amountToDeduct
    lossCount += 1
    ui.currentBet.setMaximum(int(bankBalance))
    ui.bankBalance.setText(f"Bank Balance: ${bankBalance:.2f}")
    ui.lossCounter.setText(f"Losses: {lossCount}")
    ui.rollDie.setDisabled(True)
    QtGui.QGuiApplication.processEvents()
    time.sleep(3)
    ui.winStatus.hide()
    ui.rollNumber.setText("First Roll")
    ui.rollDie.setEnabled(True)
    checkBank()


# Checks after loss for positive, non-zero bank balance
def checkBank():
    global bankBalance
    if bankBalance < 1:
        ui.winStatus.setText("You lost all of your money!")
        ui.rollDie.setDisabled(True)
        QtGui.QGuiApplication.processEvents()
        time.sleep(5)
        startNewGame()
        ui.rollDie.setEnabled(True)


# Allows player to start a new game from the menu
def startNewGame():
    global firstRoll, lastNumber, bankBalance, winCount, lossCount
    firstRoll = True
    lastNumber = 0
    bankBalance = 100.0
    winCount = 0
    lossCount = 0
    startupProcess()
    connectFunctions()


if __name__ == "__main__":
    import sys
    # Setting up Gui and the main window
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    time.sleep(0.5)  # Gives ui time to set up before using it
    firstRoll = True  # Global variable, defaults to true on game start
    lastNumber = 0
    bankBalance = 100.0  # Gives player starting money to use for betting
    winCount = 0
    lossCount = 0
    startupProcess()  # Modifies Gui to the correct initial state
    connectFunctions()  # Connect functional widgets to a function
    MainWindow.show()
    sys.exit(app.exec_())
