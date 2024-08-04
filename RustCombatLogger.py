import keyboard
import time
import os

# Set the console title
os.system('title RustCombatLogger')


keywords = {"chest", "arm", "head", "leg", "hand", "generic", "stomach"}

killStates = {"killed", "wounded", "projectile_los"}

COOLDOWN_TIME = 0.5

# Initialize global variables
last_pressed_time = 0

# Set up the path for rustpath.txt and create necessary directories
rustPathFile = os.path.join(os.getenv('APPDATA'), 'RustCombatLogger', 'rustpath.txt')
os.makedirs(os.path.dirname(rustPathFile), exist_ok=True)
rustPath = ""
def initialSetup():
    global rustPath
    # Read or prompt for Rust executable path
    if os.path.isfile(rustPathFile):
        with open(rustPathFile, 'r') as file:
            rustPath = file.readline().strip()
    else:
        print('Enter this command into rust console: bind z "client.consoletoggle;combatlog;client.consoletoggle;"')
        rustPathInput = input("Enter path where Rust.exe is located: ")
        with open(rustPathFile, 'w') as file:
            file.write(rustPathInput.strip())
        rustPath = rustPathInput.strip()
    
initialSetup()
os.system('mode con: cols=47 lines=55')  

def on_key_event(e):
    global last_pressed_time
    current_time = time.time()
    
    if e.name == 'z':  
        if current_time - last_pressed_time >= COOLDOWN_TIME:
            last_pressed_time = current_time
            os.system('cls')  # Clear the console
            
            print("Press 'Z' to refresh combatlog")

            # Clear recent_lines at the start of each refresh
            recent_lines = []
            logPath = os.path.join(rustPath, 'output_log.txt')
            
            try:
                with open(logPath, 'r', encoding='utf-8') as file:
                    for line in file:
                        columns = line.split()
                        if len(columns) > 1 and columns[1] == "you" and columns[3] == "player" and 'assets/prefabs/weapons/' in line:
                            for i, element in enumerate(columns):
                                if any(keyword in element for keyword in keywords):
                                    if i + 3 < len(columns):
                                        try:
                                            damage = round(float(columns[i+2]) - float(columns[i+3]), 1)
                                            health = columns[i+3]
                                            if i + 4 < len(columns):
                                                if columns[i+4] in killStates:
                                                    killState = columns[i+4]
                                                else:
                                                    killState = ""
                                            recent_lines.append((health, damage, killState))
                                        except ValueError:
                                            recent_lines.append(("Error", "Error", ""))
                                    break
                        if (len(columns) > 1 and columns[1] == "attacker"):
                            recent_lines = []
                            hiddenEventAmount = 0
                        if (len(columns) > 7):
                            if (columns[7] == "seconds"):
                                hiddenEventAmount = int(columns[1])

            except FileNotFoundError:
                print("Error: The file 'output_log.txt' does not exist.")
                return
            
            # Get the last 10 entries and reverse them
            lastRows = recent_lines[-50:]
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

# Set up the keyboard hook
keyboard.hook(on_key_event)

print("Press 'Z' to show combatlog")
while True:
    keyboard.wait('z') 