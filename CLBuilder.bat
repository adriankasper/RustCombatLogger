@echo off

:: Check if the 'build' directory exists and delete it
if exist "build" (
    echo Deleting 'build' directory...
    rmdir /s /q "build"
)

:: Check if the 'dist' directory exists and delete it
if exist "dist" (
    echo Deleting 'dist' directory...
    rmdir /s /q "dist"
)

:: Check if the 'RustCombatLogger.spec' file exists and delete it
if exist "RustCombatLogger.spec" (
    echo Deleting 'RustCombatLogger.spec' file...
    del /q "RustCombatLogger.spec"
)

:: Create the executable with PyInstaller
pyinstaller --icon=CLIcon.ico RustCombatLogger.py

:: Place the updater file into the exe dir
copy "RCLUpdater.bat" "dist\RustCombatLogger"

:: zip up the folder for distribution
powershell -command "Compress-Archive -Path 'dist\RustCombatLogger' -DestinationPath 'dist\RustCombatLogger.zip'"
pause
