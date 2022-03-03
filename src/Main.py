# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 02:06:39 2022

@author: Joshua
"""

from mainmenuhelper import updateElectricityPrice
from mainmenuhelper import updateUsageTarget
from mainmenuhelper import printMenu
from mainmenuhelper import updateSavingDiary
from mainmenuhelper import updateUsageDiary
from mainmenuhelper import checkCurrentMonthDetails
from mainmenuhelper import printReminder
from mainmenuhelper import printExitMessage
from mainmenuhelper import checkPeriodDetails
from data import writeDataToCsv
from data import loadData
from data import getMonthData
from data import loadUserData
from data import saveUserData


#Main function
def main():
    userdata,electricityPrice,conservationTarget = loadUserData()
    csvdata = loadData()
    getMonthData(csvdata)
    while True:
        try:
            userInput = printMenu()
            if userInput < 0 or userInput > 7:
                raise ValueError
            elif userInput == 1:
                electricityPrice = updateElectricityPrice(electricityPrice)
            elif userInput == 2:
                conservationTarget = updateUsageTarget(conservationTarget)
            elif userInput == 3:
                updateSavingDiary()
            elif userInput == 4:
                updateUsageDiary()
            elif userInput == 5:
                checkCurrentMonthDetails(electricityPrice,conservationTarget)
            elif userInput == 6:
                #check prev month
                checkPeriodDetails(csvdata,electricityPrice)
            elif userInput == 7:
                printReminder()
                printExitMessage()
                saveUserData(userdata,electricityPrice,conservationTarget)
                writeDataToCsv(csvdata)
                break
        except ValueError:
            print("Enter a number from 1 to 7 only. Please try again.")




#caller to start running the main function
if __name__=="__main__":
   main()
