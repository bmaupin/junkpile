# To use this:
# 1. Enable running scripts
#    ⚠️ Must be run as administrator. If you don't have permissions, just copy and paste the script contents into Powershell
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force
# 2. Unblock this file:
# Unblock-File -Path ./configure-windows-11.ps1
# 3. Run the file
# ./configure-windows-11.ps1

# Source: https://learn.microsoft.com/en-us/answers/questions/2355519/hide-or-unhide-widgets-on-taskbar-in-windows-11-in
function Hide-Widgets {
    try {
        Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "TaskbarDa" -Value 0 -ErrorAction Stop
        Write-Host "Hide Widgets on taskbar"
    } catch {
        Write-Host -ForegroundColor red "Failed to hide Widgets on taskbar; you can do it manually: right-click taskbar > Taskbar Settings > turn Widgets off"
    }
}
Hide-Widgets

# Source: https://gist.github.com/bobby-tablez/4b5f1ee02c68a93dc8312c4ff858c0a7
function Set-DarkTheme {
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "AppsUseLightTheme" -Value 0
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "SystemUsesLightTheme" -Value 0
    Write-Host "Dark theme enabled"
}
Set-DarkTheme

# Source: https://superuser.com/a/896408/93066
# License: cc by-sa 3.0 with attribution
function ShowFileExtensions {
    Push-Location
    Set-Location HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced
    Set-ItemProperty . HideFileExt "0"
    Pop-Location
    Write-Host "Show file extensions"
}
ShowFileExtensions

# Source: https://stackoverflow.com/a/45152368/399105
# License: cc by-sa 3.0 with attribution
function UnpinFromTaskbar($appname) {
    ((New-Object -Com Shell.Application).NameSpace("shell:::{4234d49b-0245-4df3-b780-3893943456e1}").Items() |
    ?{$_.Name -eq $appname}).Verbs() |
    ?{$_.Name.replace("&", "") -match "Unpin from taskbar"} |
    %{$_.DoIt(); $exec = $true}
}
Write-Host "Removing unwanted icons from taskbar"
UnpinFromTaskbar("Microsoft 365 Copilot")
UnpinFromTaskbar("Microsoft Edge")
UnpinFromTaskbar("Microsoft Store")

# Source: https://stackoverflow.com/a/22819650/399105
# License: cc by-sa 3.0 with attribution
function AdjustVisualEffectsForBestPerformance {
    Push-Location
    Set-Location HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects\
    # -ErrorAction SilentlyContinue is to avoid errors if it already exists
    New-ItemProperty . VisualFxSetting -Value 2 -ErrorAction SilentlyContinue
    Pop-Location
}
Write-Host "Adjust visual effects for best performance"
AdjustVisualEffectsForBestPerformance

# Source: https://devblogs.microsoft.com/scripting/hey-scripting-guy-how-can-i-hide-my-desktop-wallpaper/
# NOTE: If this doesn't work, run it after RestartExplorer; I think it should work as long as it's only run once
Function Remove-Wallpaper {
    # Removes the annoying "Learn about this picture" button in the top right
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\DesktopSpotlight\Settings" -Name "EnabledState" -Value 0
    Set-ItemProperty -path 'HKCU:\Control Panel\Desktop\' -name wallpaper -value ""
    rundll32.exe user32.dll, UpdatePerUserSystemParameters
    Write-Host "Remove wallpaper"
}
Remove-Wallpaper

# Restart Explorer to make changes (theme, file extensions, etc) take effect immediately
function RestartExplorer {
    Stop-Process -name explorer
    Write-Host "Restart explorer so changes take effect immediately"
}
RestartExplorer

# Keyboard shortcuts
# - Super + arrow keys: move window

# Window layout management
# - Install https://learn.microsoft.com/en-us/windows/powertoys/fancyzones
# - Hold Shift to snap window to grid
