import os
import sys
import wget
import subprocess
import time
import psutil
import winreg
import pathlib


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
    while True:
        # When RobloxStudioBeta.exe is running, the installer has completed
        if checkIfProcessRunning('RobloxStudioBeta.exe'):
            break
        time.sleep(1)


def loginToStudio(cookie):
    # These keys aren't created until Studio's first run, which we need to wait for
    while True:
        try:
            key = "SEC::<YES>,EXP::<9999-01-01T00:00:00Z>,COOK::<{}>".format(
                cookie)

            reg_robloxDotCom = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r'Software\\Roblox\\RobloxStudioBrowser\\roblox.com', access=winreg.KEY_WRITE)
            winreg.SetValueEx(reg_robloxDotCom,
                              r'.ROBLOSECURITY', 0, winreg.REG_SZ, key)
            winreg.CloseKey(reg_robloxDotCom)
            return
        except:
            time.sleep(0.1)


def killStudioProcess():
    os.system("taskkill /im RobloxStudioBeta.exe")


def waitForContentPath():
    # The content path is used by applications like run-in-roblox to identify Studio's install directory
    # As it is not created until studio closes, we need to wait for it
    while True:
        try:
            regKey = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r'Software\\Roblox\\RobloxStudio', access=winreg.KEY_READ)
            winreg.QueryValueEx(regKey, r'ContentFolder')
            winreg.CloseKey(regKey)
            return
        except:
            print('\nNo path', flush=True)
            time.sleep(0.1)


def createPluginsDirectory():
    # The plugins directory isn't created during the install process
    # Tools like run-in-roblox need this, so let's create it
    userDir = pathlib.Path.home()
    pluginsDir = os.path.join(userDir, "AppData", "Local", "Roblox", "Plugins")
    if not os.path.isdir(pluginsDir):
        os.makedirs(pluginsDir)


print('\nDownloading RobloxStudioLauncherBeta.exe', flush=True)
launcherPath = downloadStudioLauncher()

print('\nInstalling Roblox Studio', flush=True)
installStudio(launcherPath)

print('\nLogging in to Studio', flush=True)
loginToStudio(sys.argv[1])

print('\nWaiting before killing studio', flush=True)
time.sleep(10)
print('\nKilled studio, waiting for content path to be registered', flush=True)
killStudioProcess()
waitForContentPath()

print('\nCreating plugins directory', flush=True)
createPluginsDirectory()

print('\nStudio installed and authenticated', flush=True)
