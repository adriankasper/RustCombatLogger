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
    return_code = os.system(RCL_UPDATER)
    if return_code == 0:
        print("Updating RCL")
    else:
        print(f"Updating failed: {return_code}.")
    

def initialSetup():
    global rustPath
    latestVersion = GetLatestVersion()
    if os.path.isfile(saveDataFile):
        with open(saveDataFile, 'r') as file:
            lines = file.readlines()
            rustPath = lines[0].strip()
            if (CURRENT_VERSION != latestVersion):
                DownloadLatestVersion(latestVersion)
                time.sleep(2)
                os._exit(0)
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


    os.system('mode con: cols=47 lines=55')  
    



def on_key_event(e):
    global lastPressedTime
    currentTime = time.time()
    
    if e.name == 'z':  
        if currentTime - lastPressedTime >= COOLDOWN_TIME:
            lastPressedTime = currentTime
            os.system('cls')  # Clear the console
            
            print("Press 'Z' to refresh combatlog")

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
                                            if i + 4 < len(columns):
                                                if columns[i+4] in killStates:
                                                    killState = columns[i+4]
                                                else:
                                                    killState = ""
                                            recentLines.append((health, damage, killState))
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
            
            # Print the formatted table
            print(f"{'Health':<15} {'Damage':<15} {'Info':<15}")
            print("="*45)

            if (hiddenEventAmount > 1):
                print(f"+ {hiddenEventAmount} events in the last 10 seconds")
                hiddenEventAmount == 0
            elif (hiddenEventAmount == 1):
                print(f"+ {hiddenEventAmount} event in the last 10 seconds")
                hiddenEventAmount == 0

            for health, damage, killState in reversedLastRows:
                print(f"{health:<15} {damage:<15} {killState:<15}")

# Set the console title
os.system('title RustCombatLogger')

logIdentifyingKeywords = {"chest", "arm", "head", "leg", "hand", "generic", "stomach"}
killStates = {"killed", "wounded", "projectile_los"}

COOLDOWN_TIME = 0.5
CURRENT_VERSION = "1.0"
RCL_UPDATER = os.path.join(os.getenv('APPDATA'), 'RustCombatLogger', 'RCLUpdater.bat')
lastPressedTime = 0

keyboard.hook(on_key_event)

# Set up the path for saveData.txt and create necessary directories
saveDataFile = os.path.join(os.getenv('APPDATA'), 'RustCombatLogger', 'saveData.txt')
os.makedirs(os.path.dirname(saveDataFile), exist_ok=True)

initialSetup()

print("Press 'Z' to show combatlog")
while True:
    keyboard.wait('z') 

