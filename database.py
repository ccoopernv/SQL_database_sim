# Name: Christopher Cooper
# Filename: database.py
# Does: Runs similar to SQLITE3 database software.
#       databases are subfolders,
#       tables are files,
#       columns are data within the files.
# Modified: 2/21/2019
# Version: 0.02 beta
#

import os
import os.path
from os import path
import shutil


#creates subfolder for database
def Create_Database(dName):
    #Creates Directory Folders
    if not os.path.isdir(dName):
        try:
            os.mkdir(dName)
        except OSError:
            print("Creation of database %s failed" %dName)
        else:
            print("Database %s created:" %dName)
    else:
        print("!Failed to create database %s because it already exists." %dName)

#creates table for database
def Create_Table(dName, tName, tCol):
    #Creates Files Within Database
    filepath = (os.getcwd() + "/" + dName + "/" + tName)
    if not path.exists(filepath):
        table = open(filepath, "w+")
        numCol = len(tCol)
        for i in range(numCol):
            table.write(tCol[i])
            if i < numCol-1:
                table.write(" | ")
        table.close()
        print("Table %s created." %tName)
    else:
        print("!Failed to create table %s because it already exists." %tName)

#deletes table if database is specified
def Drop_Table(dName, tName):
    filepath = (os.getcwd()+ "/" + dName + "/" + tName)
    if os.path.isdir(dName):
        if path.exists(filepath):
            os.remove(filepath)
            print("Table %s deleted." %tName)
        else:
            print("!Failed to delete table %s because it does not exist." %tName)
    else:
        print("!Failed to delete table %s because database %t does not exist." %tName %dName)

#deletes database if it exists
def Drop_Database(dName):    
    if os.path.isdir(dName):
        filepath = (os.getcwd()+ "/" + dName)
        shutil.rmtree(filepath)
        print("Database %s deleted." %dName)
    else:
        print("!Failed to delete Database %s because it does not exist." %dName)

#Modifies Files Within Database
def Mod_Table(dName, tName, tCol): 
    filepath = (os.getcwd() + "/" + dName + "/" + tName)
    if path.exists(filepath):
        table = open(filepath, "a")
        table.write(' | ')
        numCol = len(tCol)
        for i in range(numCol):
            table.write(tCol[i])
            if i < numCol-1:
                table.write(" | ")
        table.close()
        print("Table %s modified." %tName)
    else:
        print("!Failed to modify table %s because it doesn't exist." %tName)

def Select(dName, tName, modif):
    filepath = (os.getcwd() + "/" + dName + "/" + tName)    
    if path.exists(filepath):
        with open(filepath) as table:
            tableData = table.readlines()
        for row in tableData:
            print(row)
    else:
        print("!Failed to modify table %s because it doesn't exist." %tName)

#MAIN PROGRAM
dbScope = ''
stream = 'NULL' #holds terminal input strings
exit = False #exit flag for while loop

#runs until ".EXIT" is read from terminal
while exit != True:
    #first terminal input
    stream = raw_input("SQLITE>>")
    stream = stream.lower()
    #if exit is false and there is no semicolon keep prompting for text until a ";" is detected
    if stream.find('.exit') == -1:
        while stream.find(';') == -1:
            stream = stream + raw_input("      >>")

    stream = stream.lower()
    streamArr = stream.split(';') #string array that holds commands broken up by the semicolon
    streamLen = len(streamArr) #number of elements stored in string array
    streamCount = 0 # stream loop counter
    
    comExit = False
    #breaking incoming commands up into indiviudal words
    while streamCount < streamLen and comExit != True and exit != True:

        commandArr = streamArr[streamCount].split(' ')
        commandLen = len(commandArr) #number of words in single command

        #if first word in an entry is ".exit"
        if commandArr[0] == '.exit':
            exit = True #trigger exit flag for this while loop and the outer while loop
        
        else: #normal opperation (not exit)
            if commandLen > 1:

                if commandArr[0] == 'create' and commandLen > 2: #create function

                    if commandArr[1] == 'database': #if second word in statement is database

                        if commandLen > 2: #quick error checking all commands should have a length larger than two
                            Create_Database(commandArr[2])#ADD FUNCTIONALITY FOR SPACES IN FUTURE <----

                        else:#ERROR STATE *statement is less than two strings long
                            print ("Command Error. No name for database")#ERROR NOTIFICATION
                        comExit = True # exit flag triggered (exit statement review but not program)

                    elif commandArr[1] == 'table' and dbScope != '' and os.path.isdir(dbScope): #if second word in statement is table
                        if commandLen > 3: #quick error checking *correct statements will be larger than 2 strings in length
                            if '(' in commandArr[3] and ')' in commandArr[commandLen-1]:
                                colList = [] #string list of column names and types
                                commandCount = 3
                                commandArr[commandCount] = commandArr[commandCount].lstrip(' (')
                                commandArr[commandLen-1] = commandArr[commandLen-1][:-1] #removes last character of final column ')'
                                while commandCount < commandLen:#while there are more columns to process
                                    colList.append(commandArr[commandCount])
                                    if commandCount + 1 <= commandLen - 1:
                                        colList[(commandCount-3)/2] = (colList[(commandCount-3)/2] + ' ' + commandArr[commandCount+1].rstrip(','))
                                    else: #Syntex failure
                                        print("Command Error. Incorrect Column Syntex - Col_num: %s" %commandCount)
                                        commandCount = commandLen
                                    commandCount += 2
                                if not commandCount==commandLen+2:
                                    Create_Table(dbScope, commandArr[2], colList)
                                else:
                                    print("Command Error. Incorrect Column Syntex - Col_num: %s" %commandCount)
                            else:
                                print("Command Error. Incorrect Column Syntex")
                        else:
                            print("Command Error. No name for database")

                    else:
                        if dbScope == '':
                            print('Never set database scope.  Currently NULL') 
                        else:                      
                            print("Error Undefined Object Type -%s-" %commandArr[1])	                 

                elif commandArr[0] == 'drop' and commandLen == 3:
                    if commandArr[1] == 'database':
                        Drop_Database(commandArr[2])
                        if dbScope == commandArr[2]:
                            dbScope = ''
                    elif commandArr[1] == 'table':
                        if not dbScope == '':
                            Drop_Table(dbScope, commandArr[2])
                        else:
                            print('Never set database scope.  Currently NULL')
                    else:
                        print("Command Error -%s- is not correct syntex" %streamArr[streamCount])


                elif commandArr[0] == 'use' and commandLen > 1:
                    if commandLen == 2:
                            if os.path.isdir(commandArr[1]):
                                dbScope = commandArr[1]
                                print("Using database %s" %commandArr[1])
                            else:
                                print("Error: The database %s does not exit." %commandArr[1])
                    else:
                        print("Command Error -%s- is not correct syntex" %streamArr[streamCount])

                elif commandArr[0] == 'select' and commandLen > 3:
                    if commandArr[1] == '*':
                        if commandArr[2] == 'from':
                            if dbScope != '':
                                Select(dbScope, commandArr[3], commandArr[1])
                            else:
                                print('Never set database scope.  Currently NULL')
                        else:
                            print("Command Error -%s- is not correct syntex" %commandArr[2])
                    else:
                        print("Command Error -%s- is not CURRENTLY correct syntex" %commandArr[1])
                elif commandArr[0] == 'alter' and commandLen > 3:
                    if commandArr[1] == 'table':
                        if dbScope != '':
                            if commandArr[3] == 'add':
                                colList = [] #string list of column names and types
                                commandCount = 4
                                #commandArr[commandCount] = commandArr[commandCount].lstrip(' (') #ADD FUNC LATER
                                #commandArr[commandLen-1] = commandArr[commandLen-1][:-1] #ADD FUNC LATER
                                while commandCount < commandLen:#while there are more columns to process
                                    colList.append(commandArr[commandCount])
                                    if commandCount + 1 <= commandLen - 1:
                                        colList[(commandCount-3)/2] = (colList[(commandCount-3)/2] + ' ' + commandArr[commandCount+1].rstrip(','))
                                    else: #Syntex failure
                                        print("Command Error. Incorrect Column Syntex - Col_num: %s" %commandCount)
                                        commandCount = commandLen
                                    commandCount += 2
                                if not commandCount==commandLen+2:
                                    if os.path.isdir(dbScope):
                                        Mod_Table(dbScope, commandArr[2], colList)
                                    else:
                                        print("Command Error - database -%s- does not exist" %dbScope)
                                else:
                                    print ("Command Error. Incorrect Column Syntex - Col_num: %s" %commandCount)
                            else:
                                print("Command Error -%s- is not correct syntex. You can only currently ADD" %commandArr[3])
                        else:
                            print('Never set database scope.  Currently NULL')
                    else:                    
                        print("Command Error -%s- is not something that can be altered" %commandArr[1])
                else:
                    print("Command Error -%s- is not correct syntex" %streamArr[streamCount])
            else:
                comExit = True

        streamCount += 1 # increase stream counter
        if streamCount == streamLen-1 and streamArr[streamCount] == '':
            comExit = True
  

