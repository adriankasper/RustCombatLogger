import keyboard
import time
import os
import requests
import time
from datetime import datetime, timedelta

def GetLatestVersion():
    url = 'https://github.com/adriankasper/RustCombatLogger/releases/latest'
    r = requests.get(url)
    version = r.url.split('/')[-1]
    return version

def DownloadLatestVersion(latestVersion):
    print("New version detected, downloading latest version: ", latestVersion)
    time.sleep(2)
    os.rename(os.path.join(SRC_PATH, 'RCLUpdater.bat'), os.path.join(SRC_PATH, 'RCLUpdater_old.bat'))
    return_code = os.system(f'powershell -Command "start {RCL_UPDATER} -Verb RunAs"')
    os._exit(0)

def SetTextColor(text, color,):
    return color + text + COLORS[0]

def initialSetup():
    global rustPath
    latestVersion = GetLatestVersion()
    if os.path.isfile(saveDataFile):
        with open(saveDataFile, 'r') as file:
            lines = file.readlines()
            rustPath = lines[0].strip()
            if (CURRENT_VERSION != latestVersion):
                DownloadLatestVersion(latestVersion)
            else:
                if (os.path.isfile(RCL_UPDATER)):
                    os.remove(RCL_UPDATER)
    else:
        print('Enter this command into Rust console: bind z "client.consoletoggle;combatlog;client.consoletoggle;"')
        while True:
            rustPathInput = input("Enter path where Rust.exe is located: ")
            rustExePath = os.path.join(rustPathInput, "Rust.exe")
            if os.path.isfile(rustExePath):
                with open(saveDataFile, 'w') as file:
                    file.write(rustPathInput.strip())
                rustPath = rustPathInput.strip()
                break
            else:
                os.system('cls')
                print("The specified path does not contain Rust.exe. Please try again.")


    os.system(f'mode con: cols={WINDOW_WIDTH} lines={WINDOW_HEIGHT}')  

def subtractSecondsFromDt(time_params, subtractSecond):
    # Unpack the tuple into year, month, day, hour, minute, and second
    year, month, day, hour, minute, second = time_params
    
    # Create a datetime object with the provided parameters
    dt = datetime(year, month, day, hour, minute, second)
    
    # Subtract the specified number of seconds
    new_dt = dt - timedelta(seconds=subtractSecond)
    
    # Pack the new year, month, day, hour, minute, and second into a tuple
    new_time_params = (
        new_dt.year,
        new_dt.month,
        new_dt.day,
        new_dt.hour,
        new_dt.minute,
        new_dt.second
    )
    
    return new_time_params

def replaceNonPrintableCharacters(string):
    return string.encode('ascii', 'replace').decode('ascii')
    
def PrintHeading():
    print("v" + CURRENT_VERSION)
    print((" "*((WINDOW_WIDTH-30)//2)) + '\033[31m8888888b.   .d8888b.  888     \033[37m') 
    print((" "*((WINDOW_WIDTH-30)//2)) + '\033[31m888   Y88b d88P  Y88b 888     \033[37m') 
    print((" "*((WINDOW_WIDTH-30)//2)) + '\033[31m888    888 888    888 888     \033[37m') 
    print((" "*((WINDOW_WIDTH-30)//2)) + '\033[31m888   d88P 888        888     \033[37m') 
    print((" "*((WINDOW_WIDTH-30)//2)) + '\033[31m8888888P"  888        888     \033[37m') 
    print((" "*((WINDOW_WIDTH-30)//2)) + '\033[31m888 T88b   888    888 888     \033[37m') 
    print((" "*((WINDOW_WIDTH-30)//2)) + '\033[31m888  T88b  Y88b  d88P 888     \033[37m') 
    print((" "*((WINDOW_WIDTH-30)//2)) + '\033[31m888   T88b  "Y8888P"  88888888\033[37m') 
    print()
    print((" "*((WINDOW_WIDTH-21)//2)) + "Z - Refresh CombatLog")
    print(f"   {'Health':<{10}} {'Damage':<{10}} {'Distance':<{10}} {'BodyPart':<{10}} {'Info':<{20}} {'Name':<{30}}")
    print("="*WINDOW_WIDTH)

def MapPlayerIDToColors(playerID):
    global playerColor1, playerColor2

    if playerID not in playerColorMap:
        colorIndex1, colorIndex2 = GetNextColorPairIDs()
        # Map two colors (they can be the same)
        color1 = COLORS[colorIndex1]
        color2 = COLORS[colorIndex2]

        # Store color mapping
        playerColorMap[playerID] = (color1, color2)
        return playerColor1, playerColor2
    
def GetNextColorPairIDs():
    #Generate the next color pair in base-7-like sequence
    usedPairs = set(playerColorMap.values())
    for i in range(7):
        if (COLORS[i], COLORS[i]) not in usedPairs:
            return (i, i)
    for i in range(len(COLORS)):
        for j in range(len(COLORS)):
            colorPair = (i, j)
            if (COLORS[i], COLORS[j]) not in usedPairs:
                return colorPair
    #If none left, return (0,0)
    return (0,0)

def on_key_event(e):
    global lastPressedTime
    currentTime = time.time()
    
    if e.name == 'z' or e.name == 'Z':  
        if currentTime - lastPressedTime >= COOLDOWN_TIME:
            lastPressedTime = currentTime
            time.sleep(0.1)
            os.system('cls')  # Clear the console
            
            # Clear recentLines at the start of each refresh
            recentLines = []
            logPath = os.path.join(rustPath, 'output_log.txt')
            
            try:
                with open(logPath, 'r', encoding='utf-8') as file:
                    for line in file:
                        columns = line.split()
                        if (len(columns) > 1 and columns[1] == "attacker"): #This identifies the heading of a single combatlog
                            #recentLines = []
                            hiddenEventAmount = 0
                            logTime = (
                                int(columns[0][0:4]),   # Year
                                int(columns[0][5:7]),   # Month
                                int(columns[0][8:10]),  # Day
                                int(columns[0][11:13]), # Hour
                                int(columns[0][14:16]), # Minute
                                int(columns[0][17:19])  # Second
                            ) 
                        if len(columns) > 1 and columns[1] == "died:" and columns[2] == "killed" and columns[3] == "by"  in line: #This identifies a killed message
                            playerName = ""
                            playerName = ' '.join(columns[4:-1])
                            timeKilled = (
                                int(columns[0][0:4]),   # Year
                                int(columns[0][5:7]),   # Month
                                int(columns[0][8:10]),  # Day
                                int(columns[0][11:13]), # Hour
                                int(columns[0][14:16]), # Minute
                                int(columns[0][17:19])  # Second
                            )
                            timeKilledToNameMap[timeKilled] = playerName
                        if len(columns) > 1 and columns[1] == "player" and columns[3] == "you" and 'assets/prefabs/' and columns[-6] == "killed" in line: # This identifies a death in combatlog
                            deathTime = subtractSecondsFromDt(logTime, float(columns[0][:-1]))

                            variations = [
                                (deathTime[0], deathTime[1], deathTime[2], deathTime[3], deathTime[4], deathTime[5] - 1),
                                (deathTime[0], deathTime[1], deathTime[2], deathTime[3], deathTime[4], deathTime[5]),
                                (deathTime[0], deathTime[1], deathTime[2], deathTime[3], deathTime[4], deathTime[5] + 1)
                            ]

                            # Check if any of the variations are present in the map
                            for variation in variations:
                                if variation in timeKilledToNameMap:
                                    playerIdToNameMap[columns[2]] = timeKilledToNameMap[variation]
                                    break
                            
                        if len(columns) > 1 and columns[1] == "you" and columns[3] == "player" and 'assets/prefabs/' in line: # This identifies a hit in combatlog
                            for i, element in enumerate(columns):
                                if element in logIdentifyingKeywords:
                                    if i + 3 < len(columns):
                                        try:
                                            health = columns[i+3]
                                            damage = round(float(columns[i+2]) - float(columns[i+3]), 1)
                                            if damage < 0:
                                                damage = float(columns[i+2])
                                            bodyPart = columns[i]
                                            distance = columns[i+1]
                                            playerID = columns[4]
                                            if playerID in playerIdToNameMap:
                                                if len(playerIdToNameMap[playerID]) > 29:
                                                    playerName = playerIdToNameMap[playerID][:26] + "..."
                                                else:
                                                    playerName = playerIdToNameMap[playerID][:29]
                                            else:
                                                playerName = ""
                                            if i + 4 < len(columns):
                                                if columns[i+4] in killStates:
                                                    killState = columns[i+4]
                                                else:
                                                    killState = ""
                                            if (damage < 0):
                                                killState = "wounded"
                                            if (killState == "you"):
                                                killState == "You died first"
                                            recentLines.append((health, damage, bodyPart, distance, killState, playerID, playerName))
                                        except (IndexError, ValueError) as e:
                                            recentLines.append(("Error", "Error", "Error", "Error", "Error", "Error", "Error"))
                                            print(f"Error occurred in parsing line: {line.strip()}")
                                    break


                        seen = set()
                        unique_lines = []
                        for line in recentLines:
                            if line not in seen:
                                unique_lines.append(line)
                                seen.add(line)
                        recentLines = unique_lines
                        if (len(columns) > 7):
                            if (columns[7] == "seconds"):
                                hiddenEventAmount = int(columns[1])

            except FileNotFoundError:
                print("Error: The file 'output_log.txt' does not exist.")
                return
            
            # Get the last 10 entries and reverse them
            lastRows = recentLines[-45:]
            reversedLastRows = list(reversed(lastRows))

            # Map Colors based on id, remove mapping from ids that are no longer shown
            currentActivePlayerIDs = set()
            for _, _, _, _, _, playerID, _ in reversedLastRows:
                currentActivePlayerIDs.add(playerID)
                if playerID not in playerColorMap:
                    MapPlayerIDToColors(playerID)
            
            playerIDsToRemove = []
            for playerID in playerColorMap:
                if playerID not in currentActivePlayerIDs:
                    playerIDsToRemove.append(playerID)

            # Remove unused ids from the map
            for pid in playerIDsToRemove:
                del playerColorMap[pid]

            PrintHeading()

            # Print table contents
            if (hiddenEventAmount > 1):
                print(f"+ {hiddenEventAmount} events in the last 10 seconds")
                hiddenEventAmount == 0
            elif (hiddenEventAmount == 1):
                print(f"+ {hiddenEventAmount} event in the last 10 seconds")
                hiddenEventAmount == 0
            for health, damage, bodyPart, distance, killState, playerID, playerName in reversedLastRows:
                playerColors = playerColorMap.get(playerID)
                playerColor1, playerColor2 = playerColors
                square = SetTextColor("█", playerColor1) + SetTextColor("█", playerColor2)
                if (bodyPart == "head"):
                    bodyPart = SetTextColor(bodyPart + "      ", "\033[31m")
                print(f"{square} {health:<{10}} {damage:<{10}} {distance:<{10}} {bodyPart:<{10}} {killState:<{20}} {replaceNonPrintableCharacters(playerName):<{30}}")

# Set the console title
os.system('title RustCombatLogger')

# WHITE, RED, YELLOW, GREEN, BLUE, CYAN, MAGENTA
#COLORS = ["\033[37m", "\033[31m", "\033[33m", "\033[32m", "\033[34m", "\033[36m", "\033[35m"]
COLORS = [
    "\033[37m", 
    "\033[31m", 
    "\033[33m", 
    "\033[32m", 
    "\033[34m", 
    "\033[36m", 
    "\033[35m"
    ]

logIdentifyingKeywords = {"chest", "arm", "head", "leg", "hand", "generic", "stomach", "foot"}
killStates = {"killed", "wounded", "projectile_los", "projectile_los_detailed", "you", "projectile_distance"}

WINDOW_WIDTH = 98
WINDOW_HEIGHT = 60
COLUMN_WIDTH = WINDOW_WIDTH//6

COOLDOWN_TIME = 1
CURRENT_VERSION = "2.6"
RCL_UPDATER = os.path.join(os.getenv('APPDATA'), 'RustCombatLogger', 'RCLUpdater_old.bat')
SRC_PATH = os.path.join(os.getenv('APPDATA'), 'RustCombatLogger')

lastPressedTime = 0

hiddenEventAmount = 0

playerColor1 = 0
playerColor2 = 0
playerColorMap = {}

playerIdToNameMap = {}
timeKilledToNameMap = {}

keyboard.hook(on_key_event)

# Set up the path for saveData.txt and create necessary directories
saveDataFile = os.path.join(os.getenv('APPDATA'), 'RustCombatLogger', 'saveData.txt')
os.makedirs(os.path.dirname(saveDataFile), exist_ok=True)

initialSetup()

PrintHeading()

while True:
    keyboard.wait('z') 
