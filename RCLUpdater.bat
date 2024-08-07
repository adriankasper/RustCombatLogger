@echo off
setlocal
title RCLUpdater

:: Define variables
set "url=https://github.com/adriankasper/RustCombatLogger/releases/latest/download/RustCombatLogger.zip"
set "zipfile=%temp%\RustCombatLogger.zip"
set "installDir=%APPDATA%"
set "shortcut=%userprofile%\Desktop\RustCombatLogger.lnk"
set "exe=%installDir%\RustCombatLogger\RustCombatLogger.exe"

:: Check if the installation directory exists
if exist "%installDir%\RustCombatLogger" (
    echo Installation directory exists. Cleaning up...

    :: Delete RustCombatLogger.exe if it exists
    if exist "%exe%" (
        echo Deleting %exe%...
        del "%exe%"
    )

    :: Delete the _internal directory if it exists
    if exist "%installDir%\RustCombatLogger\_internal" (
        echo Deleting %installDir%\RustCombatLogger\_internal...
        rmdir /s /q "%installDir%\RustCombatLogger\_internal"
    )
) else (
    echo Installation directory does not exist. Proceeding with installation...
)

:: Add windows defender exclusion
powershell -inputformat none -outputformat none -NonInteractive -Command "Add-MpPreference -ExclusionPath '%APPDATA%\RustCombatLogger'"

:: Download the zip file
echo Downloading %url%...
powershell -command "Invoke-WebRequest -Uri '%url%' -OutFile '%zipfile%'"

:: Create the destination directory if it doesn't exist
if not exist "%installDir%\RustCombatLogger" (
    echo Creating directory %installDir%\RustCombatLogger...
    mkdir "%installDir%"
)

:: Unzip the file
echo Unzipping %zipfile% to %installDir%...
powershell -command "Expand-Archive -Path '%zipfile%' -DestinationPath '%installDir%' -Force"

:: Clean up
echo Cleaning up...
del "%zipfile%"

:: Launch New updater if currently old
set "scriptName=%~nx0"
if "%scriptName%"=="RCLUpdater_old.bat" (
    :: Launch RCLUpdater.bat
    powershell -Command "start %installDir%\RustCombatLogger\RCLUpdater.bat -Verb RunAs"
    :: Exit the current script
    exit /b
)

:: Create a desktop shortcut
echo Creating shortcut...
powershell -command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut%'); $Shortcut.TargetPath = '%exe%'; $Shortcut.Save()"

echo Insallation done!

start "" "%installDir%\RustCombatLogger\RustCombatLogger.exe"

endlocal
exit
