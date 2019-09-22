import os
import sys
import wget
import subprocess
import time
import psutil
import winreg


def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def downloadStudioLauncher():
    launcherPath = os.path.join(sys.path[0], 'RobloxStudioLauncherBeta.exe')
    url = 'http://setup.roblox.com/RobloxStudioLauncherBeta.exe'
    wget.download(url, launcherPath)
    return launcherPath


def installStudio(launcherPath):
    subprocess.Popen([launcherPath])
    secondsWaited = 0
    while True:
        # When RobloxStudioBeta.exe is running, the installer has completed
        if checkIfProcessRunning('RobloxStudioBeta.exe'):
            os.remove(launcherPath)
            break
        # If Studio still hasn't installed after ten minutes, something has probably gone wrong
        elif secondsWaited > 600:
            print('\nError: Studio installation timed out')
            os.remove(launcherPath)
            exit(1)
        time.sleep(1)
        secondsWaited += 1


def loginToStudio(cookie):
    secondsWaited = 0
    # These keys aren't created until Studio's first run, which we need to wait for
    while True:
        try:
            key = "SEC::<YES>,EXP::<9999-01-01T00:00:00Z>,COOK::<{}>".format(
                cookie)

            reg_robloxStudioBrowser = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r'Software\\Roblox\\RobloxStudioBrowser')
            reg_robloxDotCom = winreg.OpenKey(
                reg_robloxStudioBrowser,
                r'roblox.com',
                access=winreg.KEY_WRITE,
            )
            winreg.SetValueEx(reg_robloxDotCom,
                              r'.ROBLOSECURITY', 0, winreg.REG_SZ, key)
            return
        except:
            # If we still can't set these keys after 20 seconds, something has probably gone wrong
            if secondsWaited > 20:
                print('\nError: Failed to login to Studio')
                exit(1)
            time.sleep(0.1)
            secondsWaited += 0.1


print('\nDownloading RobloxStudioLauncherBeta.exe')
launcherPath = downloadStudioLauncher()

print('\nInstalling Roblox Studio')
installStudio(launcherPath)

print('\nLogging in to Studio')
loginToStudio(sys.argv[1])

print('\nStudio installed and authenticated')
