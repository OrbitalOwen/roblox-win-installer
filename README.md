Python script to download, install and authenticate Roblox Studio in a CI environment.

Run with a ROBLOSECURITY cookie as an argument.

Please check the script carefully before running it on your machine as it takes some destructive actions (such as deleting your local Roblox directory and overwriting your Roblox settings)

# Usage

For an example GitHub action, see the `.github/workflows` directory. For a platform agnostic example, see below:

```powershell
# Download this repo (there are currently no releases)
git clone git@github.com:OrbitalOwen/roblox-win-installer.git

# Install Roblox Studio
cd roblox-win-installer
py install.py $env:cookie

# Download run-in-roblox (you could also build this from source using cargo install run-in-roblox)
cd ..
Invoke-WebRequest "https://github.com/OrbitalOwen/run-in-roblox/releases/download/0.2.0/run-in-roblox.exe" -OutFile run-in-roblox.exe
.\run-in-roblox.exe -t 1800 .\file.lua
```
