# To use this:
# 1. Enable running scripts (must be run as an administrator):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force
# 2. Unblock this file:
# Unblock-File -Path ./configure-windows-10.ps1
# 3. Run the file
# ./configure-windows-10.ps1

# Source: https://gallery.technet.microsoft.com/scriptcenter/How-to-disable-Cortana-on-b44924a4
# License: TechNet terms of use (https://gallery.technet.microsoft.com/scriptcenter/site/How-to-disable-Cortana-on-b44924a4/eulapartial?licenseType=TechNet)
function DisableCortana {
    $path = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    if (!(Test-Path -Path $path)) {
        New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows" -Name "Windows Search"
    }
    Set-ItemProperty -Path $path -Name "AllowCortana" -Value 0
}
DisableCortana

# Source: https://social.technet.microsoft.com/Forums/ie/en-US/af677b8e-f30d-4fbc-a3b7-cd70c001c89f/windows-10-remove-cortanasearch-box-from-task-bar-via-gpo-for-osd?forum=win10itprosetup
function RemoveCortanaSearch {
    $path = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Search"
    if (!(Test-Path -Path $path)) {
        New-Item -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion" -Name "Search"
    }
    Set-ItemProperty -Path $path -Name "SearchboxTaskbarMode" -Value 0
}
RemoveCortanaSearch

# Source: https://superuser.com/a/896408/93066
# License: cc by-sa 3.0 with attribution
function ShowFileExtensions {
    Push-Location
    Set-Location HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced
    Set-ItemProperty . HideFileExt "0"
    Pop-Location
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
UnpinFromTaskbar("Mail")
UnpinFromTaskbar("Microsoft Edge")
UnpinFromTaskbar("Microsoft Store")

# Source: https://superuser.com/q/1191143/93066
# License: cc by-sa 3.0 with attribution
function UnpinFromStart($appname) {
    try {
        ((New-Object -Com Shell.Application).NameSpace("shell:::{4234d49b-0245-4df3-b780-3893943456e1}").Items() |
        ?{$_.Name -eq $appname}).Verbs() |
        ?{$_.Name.replace("&", "") -match "Unpin from Start"} |
        %{$_.DoIt(); $exec = $true}
    } catch {
        Write-Host "Warning: failed to unpin $appname; it may not exist"
    }
}
UnpinFromStart("Calendar")
UnpinFromStart("Groove Music")
UnpinFromStart("Mail")
UnpinFromStart("Maps")
UnpinFromStart("Microsoft Edge")
UnpinFromStart("Microsoft Store")
UnpinFromStart("Movies & TV")
UnpinFromStart("My Office")
UnpinFromStart("OneNote")
UnpinFromStart("Paint 3D")
UnpinFromStart("Photos")
UnpinFromStart("Skype")
UnpinFromStart("Weather")
UnpinFromStart("Xbox")

# Source: https://stackoverflow.com/a/22819650/399105
# License: cc by-sa 3.0 with attribution
function AdjustVisualEffectsForBestPerformance {
    Push-Location
    Set-Location HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects\
    New-ItemProperty . VisualFxSetting -Value 2 -ErrorAction SilentlyContinue
    Pop-Location
}
AdjustVisualEffectsForBestPerformance

# Restart Explorer to make changes (Cortana, file extensions) take effect immediately
function RestartExplorer {
    Stop-Process -name explorer
}
RestartExplorer
