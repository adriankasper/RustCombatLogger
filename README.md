# RustCombatLogger
External combatlog for Rust

![RustCombatLogger Screenshot](https://raw.githubusercontent.com/adriankasper/RustCombatLogger/main/media/Screenshot.png)
## Install
1) Download the [latest release](https://github.com/adriankasper/RustCombatLogger/releases/latest)
2) Extract RustCombatLogger.zip
3) Launch RCLUpdater.bat
4) Delete the exctracted folder
5) Enter `bind z "client.consoletoggle;combatlog;client.consoletoggle;"` into rust console

## Uninstall
1) Close all instances of RustCombatLogger
2) Press `⊞ Win` + `R`
3) Type %appdata%
4) Delete folder RustCombatLogger

#### Why is antivirus blocking the program?
This program uses Pyinstaller to package a python script into an exe file, so users do not need to have Python and other requirements installed on their system. Pyinstaller is also used by malware developers to hide malicious code, so antivirus programs detect programs made with Pyinstaller as malicious. RustCombatLogger however is open source, so everyone can see the source code containing no malicious parts.
