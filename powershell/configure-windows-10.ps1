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
    # Restart Explorer to change it immediately
    Stop-Process -name explorer
}
DisableCortana

# Source: https://superuser.com/a/896408/93066
# License: cc by-sa 3.0 with attribution
function ShowFileExtensions {
    Push-Location
    Set-Location HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced
    Set-ItemProperty . HideFileExt "0"
    Pop-Location
    # Restart Explorer to change it immediately
    Stop-Process -name explorer
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
    ((New-Object -Com Shell.Application).NameSpace("shell:::{4234d49b-0245-4df3-b780-3893943456e1}").Items() |
    ?{$_.Name -eq $appname}).Verbs() |
    ?{$_.Name.replace("&", "") -match "Unpin from Start"} |
    %{$_.DoIt(); $exec = $true}
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
