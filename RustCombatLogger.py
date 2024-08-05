import keyboard
import time
import os
import requests

def GetLatestVersion():
    url = 'https://github.com/adriankasper/RustCombatLogger/releases/latest'
    r = requests.get(url)
    version = r.url.split('/')[-1]
    return version

def DownloadLatestVersion(latestVersion):
    print("New version detected, downloading latest version: ", latestVersion)
    os.rename("RCLUpdater.bat", "RCLUpdater_old.bat")
    return_code = os.system("start " + RCL_UPDATER)
    os._exit(0)

def SetTextColor(text, color):
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


    os.system('mode con: cols=82 lines=55')  
    
def PrintLogo():
    print('                          \033[31m8888888b.   .d8888b.  888     \033[37m') 
    print('                          \033[31m888   Y88b d88P  Y88b 888     \033[37m') 
    print('                          \033[31m888    888 888    888 888     \033[37m') 
    print('                          \033[31m888   d88P 888        888     \033[37m') 
    print('                          \033[31m8888888P"  888        888     \033[37m') 
    print('                          \033[31m888 T88b   888    888 888     \033[37m') 
    print('                          \033[31m888  T88b  Y88b  d88P 888     \033[37m') 
    print('                          \033[31m888   T88b  "Y8888P"  88888888\033[37m') 


def on_key_event(e):
    global lastPressedTime
    currentTime = time.time()
    
    if e.name == 'z':  
        if currentTime - lastPressedTime >= COOLDOWN_TIME:
            lastPressedTime = currentTime
            os.system('cls')  # Clear the console
            
            # Clear recentLines at the start of each refresh
            recentLines = []
            logPath = os.path.join(rustPath, 'output_log.txt')
            
            try:
                with open(logPath, 'r', encoding='utf-8') as file:
                    for line in file:
                        columns = line.split()
                        if len(columns) > 1 and columns[1] == "you" and columns[3] == "player" and 'assets/prefabs/weapons/' in line:
                            for i, element in enumerate(columns):
                                if any(keyword in element for keyword in logIdentifyingKeywords):
                                    if i + 3 < len(columns):
                                        try:
                                            damage = round(float(columns[i+2]) - float(columns[i+3]), 1)
                                            health = columns[i+3]
                                            playerID = columns[4]
                                            bodyPart = columns[i]
                                            distance = columns[i+1]
                                            if i + 4 < len(columns):
                                                if columns[i+4] in killStates:
                                                    killState = columns[i+4]
                                                else:
                                                    killState = ""
                                            if (damage < 0):
                                                killState = "wounded"
                                            if (killState == "you"):
                                                killState == "You died first"
                                            recentLines.append((health, damage, bodyPart, distance, killState, playerID))
                                        except ValueError:
                                            recentLines.append(("Error", "Error", ""))
                                    break
                        if (len(columns) > 1 and columns[1] == "attacker"):
                            recentLines = []
                            hiddenEventAmount = 0
                        if (len(columns) > 7):
                            if (columns[7] == "seconds"):
                                hiddenEventAmount = int(columns[1])

            except FileNotFoundError:
                print("Error: The file 'output_log.txt' does not exist.")
                return
            
            # Get the last 10 entries and reverse them
            lastRows = recentLines[-50:]
            reversedLastRows = list(reversed(lastRows))

            # Assign colors to each player
            playerColorMap = {}
            colorIndex = 0
            for _, _, _, _, _, playerID in reversedLastRows:
                if playerID not in playerColorMap:
                    if colorIndex < len(COLORS):
                        playerColorMap[playerID] = COLORS[colorIndex]
                        colorIndex += 1
                    else:
                        playerColorMap[playerID] = COLORS[0]

            print()
            PrintLogo()
            print()
            print("                              Z - Refresh CombatLog")
            print(f"   {'Health':<15} {'Damage':<15} {'Distance':<15} {'BodyPart':<15} {'Info':<15}")
            print("="*78)

            # Print table contents
            if (hiddenEventAmount > 1):
                print(f"+ {hiddenEventAmount} events in the last 10 seconds")
                hiddenEventAmount == 0
            elif (hiddenEventAmount == 1):
                print(f"+ {hiddenEventAmount} event in the last 10 seconds")
                hiddenEventAmount == 0
            
            for health, damage, bodyPart, distance, killState, playerID in reversedLastRows:
                color = playerColorMap.get(playerID)
                square = SetTextColor("██", color)
                if (bodyPart == "head"):
                    bodyPart = SetTextColor(bodyPart + "           ", "\033[31m")
                print(f"{square} {health:<15} {damage:<15} {distance:<15} {bodyPart:<15} {killState:<15}")

# Set the console title
os.system('title RustCombatLogger')

# WHITE, RED, YELLOW, GREEN, BLUE, CYAN, MAGENTA
#COLORS = ["\033[37m", "\033[31m", "\033[33m", "\033[32m", "\033[34m", "\033[36m", "\033[35m"]
COLORS = ["\033[37m", "\033[31m", "\033[33m", "\033[32m", "\033[34m", "\033[36m", "\033[35m"]
logIdentifyingKeywords = {"chest", "arm", "head", "leg", "hand", "generic", "stomach", "foot"}
killStates = {"killed", "wounded", "projectile_los", "you"}

COOLDOWN_TIME = 0.5
CURRENT_VERSION = "1.8"
RCL_UPDATER = os.path.join(os.getenv('APPDATA'), 'RustCombatLogger', 'RCLUpdater_old.bat')
lastPressedTime = 0

keyboard.hook(on_key_event)

# Set up the path for saveData.txt and create necessary directories
saveDataFile = os.path.join(os.getenv('APPDATA'), 'RustCombatLogger', 'saveData.txt')
os.makedirs(os.path.dirname(saveDataFile), exist_ok=True)

initialSetup()

print()
PrintLogo()
print()
print("                              Z - Refresh CombatLog")
print(f"   {'Health':<15} {'Damage':<15} {'Distance':<15} {'BodyPart':<15} {'Info':<15}")
print("="*78)


while True:
    keyboard.wait('z') 
