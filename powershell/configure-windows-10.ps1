# To use this:
# 1. Enable running scripts (must be run as an administrator):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force
# 2. Unblock this file:
# Unblock-File -Path ./configure-windows-10.ps1
# 3. Run the file
# ./configure-windows-10.ps1

# Disable Cortana
# Source: https://gallery.technet.microsoft.com/scriptcenter/How-to-disable-Cortana-on-b44924a4
# License: TechNet terms of use (https://gallery.technet.microsoft.com/scriptcenter/site/How-to-disable-Cortana-on-b44924a4/eulapartial?licenseType=TechNet)
Function DisableCortana {
    $path = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search"    
    IF (!(Test-Path -Path $path)) { 
        New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows" -Name "Windows Search"
    } 
    Set-ItemProperty -Path $path -Name "AllowCortana" -Value 0 
    # Restart Explorer to change it immediately    
    Stop-Process -name explorer
}
DisableCortana
