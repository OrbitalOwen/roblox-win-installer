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
            print('\nError: Studio installation timed out', flush=True)
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

            reg_robloxDotCom = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r'Software\\Roblox\\RobloxStudioBrowser\\roblox.com', access=winreg.KEY_WRITE)
            winreg.SetValueEx(reg_robloxDotCom, r'.ROBLOSECURITY', 0, winreg.REG_SZ, key)
            winreg.CloseKey(reg_robloxDotCom)
            return
        except:
            # If we still can't set these keys after 20 seconds, something has probably gone wrong
            if secondsWaited > 20:
                print('\nError: Failed to login to Studio', flush=True)
                exit(1)
            time.sleep(0.1)
            secondsWaited += 0.1

def killStudioProcess():
    os.system("taskkill /im RobloxStudioBeta.exe")

def waitForContentPath():
    # The content path is used by applications like run-in-roblox to identify Studio's install directory
    # As it is not created until studio closes, we need to wait for it
    secondsWaited = 0
    while True:
        try:
            regKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Roblox\\RobloxStudio', access=winreg.KEY_READ)
            winreg.QueryValueEx(regKey, r'ContentFolder')
            winreg.CloseKey(regKey)
            return
        except:
            # If we still can't find this key after 20 seconds, something has probably gone wrong
            if secondsWaited > 20:
                print('\nError: Studio content path not registered. Studio has installed but applications may not be able to find it.', flush=True)
                exit(1)
            time.sleep(0.1)
            secondsWaited += 0.1

print('\nDownloading RobloxStudioLauncherBeta.exe', flush=True)
launcherPath = downloadStudioLauncher()

print('\nInstalling Roblox Studio', flush=True)
installStudio(launcherPath)

print('\nLogging in to Studio', flush=True)
loginToStudio(sys.argv[1])

print('\nWaiting for content path to be registered', flush=True)
killStudioProcess()
waitForContentPath()

print('\nStudio installed and authenticated', flush=True)
