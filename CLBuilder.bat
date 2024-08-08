@echo off
pyinstaller --icon=CLIcon.ico RustCombatLogger.py
copy "RCLUpdater.bat" "dist\RustCombatLogger"
powershell -command "Compress-Archive -Path 'dist\RustCombatLogger' -DestinationPath 'dist\RustCombatLogger.zip'"
pause
