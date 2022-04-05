#! /usr/bin/env python3

#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- 
#   Imports

import os
import sys
import traceback
from time import sleep
from datetime import datetime

#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- 
#   ANSI Escape Codes for formatting text

class FG:
  BLACK     = "\u001b[30m"
  RED       = "\u001b[31m"
  GREEN     = "\u001b[32m"
  YELLOW    = "\u001b[33m"
  BLUE      = "\u001b[34m"
  MAGENTA   = "\u001b[35m"
  CYAN      = "\u001b[36m"
  WHITE     = "\u001b[37m"

class BG:
  BLACK     = "\u001b[40m"
  RED       = "\u001b[41m"
  GREEN     = "\u001b[42m"
  YELLOW    = "\u001b[43m"
  BLUE      = "\u001b[44m"
  MAGENTA   = "\u001b[45m"
  CYAN      = "\u001b[46m"
  WHITE     = "\u001b[47m"

class UTIL:
  RESET     = "\u001b[0m"
  BOLD      = "\u001b[1m"
  ITALICS   = "\u001b[3m"
  UNDERLINE = "\u001b[4m"
  REVERSE   = "\u001b[7m"

  CLEAR     = "\u001b[2J"
  CLEARLINE = "\u001b[2K"

  UP        = "\u001b[1A"
  DOWN      = "\u001b[1B"
  RIGHT     = "\u001b[1C"
  LEFT      = "\u001b[1D"

  NEXTLINE  = "\u001b[1E"
  LASTLINE  = "\u001b[1F"

  TOP       = "\u001b[0;0H"

#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- 
#   Classes for program information

# General info class
class INFO:
    VERSION     = "c1"
    SUBVERSION  = "0e"
    BUILD       = "107"
    LICENSE     = "GPL 3.0"
    AUTHOR      = "PsychicPenguin"
    NAME        = "Timeless Tom"
    STATUS      = "STOPPED"
    CMD         = ""

# This is basically used like #define in C. This way we don't have to remember what numbers represent what level
class LVL:
    INFO    = 0
    WARNING = 1
    HEADER  = 2
    ERROR   = 3
    STATUS  = 4

# Class to save timestamps
class TIME:
    START   = "00:00:00"
    STOP    = "00:00:00"
    BEGIN   = "00:00:00"
    EXIT    = "00:00:00"

#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- 
#   Dealing with time

def GetDate(): # Returns the current date as dd.mm.yy
    now = datetime.now()
    return now.strftime("%d.%m.%y")

def GetTime(): # Return the current time as hh:mm:ss
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def GetDuration(start, stop): # Returns the duration between to timestamps as hh:mm:ss

    # Split input into its parts, convert to int and add to array
    start = start.split(":")
    for i in range(len(start)):
        start[i] = int(start[i])
    stop = stop.split(":")
    for i in range(len(stop)):
        stop[i] = int(stop[i])

    # Subtract stop from start to get hours, minutes and seconds
    h = stop[0]-start[0]
    m = stop[1]-start[1]
    s = stop[2]-start[2]
    
    # In some cases the result will be negative. Start at 50s, end at 10s, will end up as 10-50=-40
    # For this reason we add 60 to s until s is not negative anymore. For every 60 added we need to subtract 1 from m
    while s < 0:
        s += 60
        m -= 1
    # Doing the same thing to get correct minutes. Add 60 to m, sub 1 from h
    while m < 0:
        m += 60
        h -= 1

    # We have integers atm, so 9 will not be 09. To do this we add '0' to the result string if input < 10
    result = ""
    if h < 10:
        result += "0"
    result += str(h) + ":"
    if m < 10:
        result += "0"
    result += str(m) + ":"
    if s < 10:
        result += "0"
    result += str(s)
    return result

#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
#   Interacting with the OS

def Exit(clean): # Close the program down
    if not clean: # If the user tried to exit with ctrl+c, tell him about the 'exit' command
        print(UTIL.CLEARLINE + UTIL.UP)
        Log(LVL.WARNING, "You can just type 'exit', you know?")
        sleep(2)
    
    # Set status to what is currently going on
    INFO.STATUS = "Exiting ..."
    SetStatus()
    sleep(0.5)

    # Get the time of when the program was closed
    TIME.END = GetTime()
    # Output how long the program has been running in total
    print("Total runtime: " + GetDuration(TIME.BEGIN, TIME.END))
    sleep(2)

    # Clear the screen and close the environment
    print(UTIL.CLEAR + UTIL.TOP, end="")
    quit()

def RemoveFile(backup=False):
    # Check if file even exists. This should never really return true though
    if not os.path.exists("tt.csv"):
        Log(LVL.ERROR, "File could not be found ...")
        return
    # If backup mode, just rename the file
    if backup:
        os.rename("tt.csv", "tt.csv.bak")
        return
    # Otherwise actually delete the file
    else:
        Log(LVL.WARNING, "You are about to delete your logfile. This might be a bad idea yo ...")
        # Make REALLY sure user wants to do that
        if Doublecheck():
            os.remove("tt.csv")
            return

def Write(txt, time=True): # Writes to 'tt.csv' file
    # Open the file
    file = open("tt.csv", "a")
    # Write to file what came as argument, seperate via ','
    file.write(txt + ",")

    # If time parameter is true, add time of logging to file
    if time:
        file.write(GetDate() + "," + GetTime())
        
        # If txt is 'PAUSE' or 'STOP', calculate the duration since the last 'START' or 'CONTINUE'
        if (txt == "PAUSE" or txt == "STOP"):
            file.write("," + GetDuration(TIME.START, TIME.STOP))

        # Finally write to file
    file.write("\n")
    # And close the file down cleanly
    file.close()

def ClosedProperly(): # Checks if last time the program ran, it was stopped before exited
    last_line = ""
    # Open 'tt.csv' file and read it in by line
    with open("tt.csv") as file:
        for line in file:
            pass
        last_line = line

    # Split the last line by ','
    parts = last_line.split(",")

    # Check if last line starts with 'STOP' or 'LOGON', then the program was closed down properly
    if parts[0] == "STOP" or parts[0] == "LOGON" or parts[0] == "WHAT":
        Log(LVL.INFO, "File looks okay :)")
        return
   
    # If file was NOT closed propery, ask user if they want to start anew or continue from where they left off
    Log(LVL.WARNING, "File was not closed propery.\n\t\tYou are about to continue where you left off ...")
    if (Doublecheck()):
        INFO.STATUS = "LOGGING"
    return

def Doublecheck(): # Warning prompt when the user wants to do something that might cause trouble
    answer = input("Do you want to continue anyway? [Y/n]\t")
    # Only check first letter of answer and convert to lowercase, that way 'Y', 'y', 'Yes', 'yes', 'yeah!' etc. work
    if answer[0].lower() == "y": # 'yo pls stop' will work, too. So there's that
        print(UTIL.CLEARLINE + "Okay then! I hope you know what you are doing ..." + UTIL.RESET)
        return True
    print(UTIL.CLEARLINE + "Aborted! Probably for the best, don't you think?" + UTIL.RESET)
    return False

#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
#   Status

def GetStatusColor(): # Return style of current status
    color = FG.BLACK
    if INFO.STATUS == "LOGGING": # Green for LOGGING
        color += BG.GREEN
    elif INFO.STATUS == "PAUSED": # Yellow for PAUSED
        color += BG.YELLOW
    elif INFO.STATUS == "STOPPED": # Red for STOPPED
        color += BG.RED
    else:
        color += BG.WHITE # White if other
    return color

def SetStatus():
    # Move cursor down
    print(UTIL.DOWN, end="")
    # Print current status
    Log(LVL.STATUS, INFO.STATUS)
    # Move cursor back up
    print(UTIL.UP + UTIL.UP + UTIL.UP)

def ClearStatus():
    # Move cursor down, clear line, move cursor back up, clear line again
    print(UTIL.CLEARLINE, end="")

#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
#   Making the UI pretty

def Logo(): # The logo of the program, created with figlet
    print(FG.GREEN + UTIL.BOLD, end="")
    print("|--------------------------------------------------------------------|")
    print("|   _____ _                _                 _____                   |") 
    print("|  |_   _(_)_ __ ___   ___| | ___  ___ ___  |_   _|__  _ __ ___      |")
    print("|    | | | | '_ ` _ \ / _ \ |/ _ \/ __/ __|   | |/ _ \| '_ ` _ \     |") 
    print("|    | | | | | | | | |  __/ |  __/\__ \__ \---| | (_) | | | | | |    |")
    print("|    |_| |_|_| |_| |_|\___|_|\___||___/___/---|_|\___/|_| |_| |_|    |")
    print("|                                                                    |")
    print("|--------------------------------------------------------------------|")
    print(UTIL.RESET,end="")

def Bubi(): # Picture of the bestest bube, converted to ASCII with ascii-image-converter
    print(BG.BLACK + FG.WHITE + UTIL.BOLD, end="")
    print("########################################################")
    print("#****************************************=%************#")
    print("#**************************************+:.=************#")
    print("#***********%*************************=.:.-************#")
    print("#***********:=#*********************#:.:..=************#")
    print("#***********=..:=#%************%%**-..:...#************#")
    print("#************-.....:=*###*++==-::. ......:*************#")
    print("#*************-......::::::-:::::........-*************#")
    print("#*************%....::::::........:::.... +*************#")
    print("#**************=.:::........   .:::.::.:.=*************#")
    print("#**************#:::=-.  ....  . :*- ...::-*************#")
    print("#**************+:..=: ........-. :....::::%************#")
    print("#**************+-:..............   ....:::*************#")
    print("#**************#::.............   .....:::#************#")
    print("#***************-..:...:-..:.   ....  ...=*************#")
    print("#****************........    .. ..     ..%*************#")
    print("#***************#..    .===:-#-:=     ...#*************#")
    print("#***************-..      #*=**=-.      ..=*************#")
    print("#**********%#++=..       :+::--.       ..:%************#")
    print("#********#=::::-..                     ...#************#")
    print("#******%=:::..::.              -+*==:.....#************#")
    print("#******:.:.....:.              .-#*#=:....*************#")
    print("#***%=::...  .:=:.                .   ....#************#")
    print("#**%-.:...   .-=-                      . -*************#")
    print("#**=:...     :--:.                    . :**************#")
    print("#%=:...      .:::.                     :%**************#")
    print("#-:...       .:..                     .%***************#")
    print("#:..          :.                    ...:**************##")
    print("########################################################")
    print(UTIL.RESET,end="")

def Log(lvl, txt): # Example: [TYPE]	Message
    if lvl == LVL.INFO: # Green for [INFO]
        print(FG.GREEN + UTIL.BOLD + "[INFO]" + UTIL.RESET + FG.GREEN + "\t\t" + txt + UTIL.RESET)
    elif lvl == LVL.WARNING: # Yellow for [WARNING]
        print(FG.YELLOW + UTIL.BOLD + "[WARNING]" + UTIL.RESET + FG.YELLOW + "\t" + txt + UTIL.RESET)
    elif lvl == LVL.ERROR: # Red for [ERROR]
        print(FG.RED + UTIL.BOLD + "[ERROR]" + UTIL.RESET + FG.RED + "\t\t" + txt + UTIL.RESET)
    elif lvl == LVL.STATUS: # The style of status depends on the status itself
        print(GetStatusColor() + "[STATUS: " + INFO.STATUS + "]" + UTIL.RESET + FG.CYAN + UTIL.RESET)
    else: # If invalid lvl was given, just highlight by making the text bald
        print(UTIL.BOLD + "[" + txt + "]" + UTIL.RESET)

def Header(txt): # Used for any kind of highlighted output
   Log(LVL.HEADER, txt)

def Body(txt, indent=False): # Any kind of not highlighted output
    if indent:
        print("  ->  ", end="")
    print(txt)

#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
#   Command Functions

def Usage(): # Usage prints the contents of README.md
    file = open("README.md", "r+")
    
    # Set style of the output
    print(UTIL.BOLD)

    # Print contents of file line by line
    for line in file.readlines():
        print(line)

    # Reset style to default
    print(UTIL.UP + UTIL.RESET, end="")

def License(): # License prints the contents of LICENSE
    file = open("LICENSE", "r+")
    
    # Set style of the output
    print(UTIL.BOLD)

    # Print contents of file line by line
    for line in file.readlines():
        print(line)

    # Reset style to default
    print(UTIL.UP + UTIL.RESET, end="")

def Help(): # Print list of available command and what they do
    Header("List of available commands")
    Body("help / wtf \t(display this menu)",indent=True)
    Body("exit / :wq \t(exit out of this program)",indent=True)
    Body("clear / cls\t(clear the screen)",indent=True)

    print("")
    Body("usage      \t(the long version of the help menu)",indent=True)
    Body("licence    \t(display the full license)",indent=True)
 
    print("")
    Body("start      \t(start    logging)",indent=True)
    Body("pause      \t(pause    logging)",indent=True)
    Body("continue   \t(continue logging)",indent=True)
    Body("stop       \t(stop     logging)",indent=True)

def Confusion(): # If user types invalid command, help them in their confusion
    Log(LVL.WARNING, "Invalid command")
    Body("'" + INFO.CMD + "'" + " is not a valid command.")
    Body("Type 'help' or 'wtf' to display list of available commands.")

def Clear():
    # Clear the screen and move cursor to top
    print(UTIL.CLEAR + UTIL.TOP, end="")
    # Print the logo
    Logo()
    # Print program information
    txt = INFO.NAME + " by " + INFO.AUTHOR + " v" + INFO.VERSION + "." + INFO.SUBVERSION + "." + INFO.BUILD
    Header(txt)
    txt = "Licensed under " + INFO.LICENSE
    Header(txt)
    txt = TIME.START
    Header(txt)

#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
#   Logging Functions

def Start():
    # Continue if paused
    if INFO.STATUS == "PAUSED":
        Continue()
        return
    # Throw error if already logging
    elif INFO.STATUS == "LOGGING":
        Log(LVL.ERROR, "You are already logging. Don't get too excited now ...")
        return

    # Get current time of command
    time = GetTime()
    TIME.START = time

    # Log to stdout and file
    txt = "Started Logging at\t" + time
    Log(LVL.INFO, txt)
    INFO.STATUS = "LOGGING"
    Write("START")

def Pause():
    # Throw error if not already logging
    if INFO.STATUS != "LOGGING":
        print(UTIL.REVERSE + UTIL.BOLD + ">> " + INFO.CMD + UTIL.RESET)
        # Be especially rude if already paused
        if INFO.STATUS == "PAUSED":
            print("Needing a break from the break? I feel you :/")
            return
        Log(LVL.ERROR, "There is nothing to pause, I can't pause life (yet) ...")
        return

    # Get current time of command
    time = GetTime()
    TIME.STOP = time

    # Log to stdout and file
    txt = "Paused logging at\t" + time
    Log(LVL.INFO, txt)
    INFO.STATUS = "PAUSED"
    Write("PAUSE")

def Continue():
    # Throw error if not paused
    if INFO.STATUS != "PAUSED":
        print(UTIL.REVERSE + UTIL.BOLD + ">> " + INFO.CMD + UTIL.RESET)
        Log(LVL.ERROR, "You need to pause before continuing ...")
        return

    # Get current time of command
    time = GetTime()
    TIME.START = time

    # Log to stdout andfile
    txt = "Continued logging at\t" + time
    Log(LVL.INFO, txt)
    INFO.STATUS = "LOGGING"
    Write("CONTINUE")

def Stop():
    # Stop logging if logging or paused
    if INFO.STATUS == "PAUSED" or INFO.STATUS == "LOGGING":
        # Get current time of command
        time = GetTime()
        TIME.STOP = time

        # Log to stdout and file
        txt = "Stopped logging at\t" + time
        Log(LVL.INFO, txt)
        INFO.STATUS = "STOPPED"
        Write("STOP")
    else:
        # Throw error if neither logging nor paused
        print(UTIL.REVERSE + UTIL.BOLD + ">> " + INFO.CMD + UTIL.RESET)
        Log(LVL.ERROR, "You might want to start before stopping, eh?")


#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
#   How the user can interact with the program

def Prompt():
    try:
         while INFO.CMD != "exit":
            # Create header and status and prompt user for input
            SetStatus()    
            INFO.CMD = input(UTIL.BOLD + ">> " + UTIL.RESET)
            # Convert to lower to make everything case insensitive
            INFO.CMD = INFO.CMD.lower()
            ClearStatus()

            # General Commands
            if INFO.CMD == "help" or INFO.CMD == "wtf":
                Help()
            elif INFO.CMD == "usage":
                Usage()
            elif INFO.CMD == "license":
                License()
            elif INFO.CMD == "exit" or INFO.CMD == ":wq":
                Exit(True)    
            elif INFO.CMD == "clear" or INFO.CMD == "cls":
                Clear()
            elif INFO.CMD == "":
                print("", end="")
            # Handle files
            elif INFO.CMD == "rm" or INFO.CMD == "remove":
                RemoveFile()
            elif INFO.CMD == "bak" or INFO.CMD == "backup":
                RemoveFile(backup=True)
            # Logging Commands
            elif INFO.CMD == "start":
                Start()
            elif INFO.CMD == "pause":
                Pause()
            elif INFO.CMD == "continue":
                Continue()
            elif INFO.CMD == "stop":
                Stop()
            # Hidden Commands
            elif INFO.CMD == "bubi":
                Bubi()
            else:
                Confusion()
    except KeyboardInterrupt:
        Exit(False)
    except Exception as e:
        print("\n\n\n")
        Log(LVL.ERROR, "Something went wrong. The program is crashing ...")
        print(str(e))
        traceback.print_exc()
        print("\n")
        Log(LVL.ERROR, "Please send this to your administrator!")


#   --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
#   Starting point

'''
    I once asked my british friend what the function to initiali[sz]e a program was called
    He said "Init, innit?"
'''

def Init():
    # Check if running on Windows, do os.system("") if so to enable ansi escape codes
    if sys.platform == "win32":
        os.system("")

    # Set time for beginning for program
    TIME.BEGIN = GetTime()
    Log(LVL.INFO, "Checking if file exists ...")
    sleep(0.5)

    # Check if file exists
    if not os.path.isfile("tt.csv"): # Create file if it doesn't
        Log(LVL.WARNING, "File does not exist ...")
        sleep(0.5)
        Write("WHAT,DATE,TIME,DURATION",time=False)
        Log(LVL.INFO, "Created file!")
        sleep(0.5)
    else: # Be nice to user if it does
        Log(LVL.INFO, "File found! You are a good boi!")
        # Check if program was closed properly
        ClosedProperly()
        sleep(0.5)

    # Write new entry if file was closed propery (or error was ignored)
    if INFO.STATUS == "...":
        Write("\nLOGON")
    Clear()
    Prompt()

# Literal entry point of the program
if __name__ == "__main__":
    Init()
else: # If loaded in as module, say 'please don't touch me there, that's my no-no-square'
    Log(LVL.ERROR, "This module is not meant to be imported!")

