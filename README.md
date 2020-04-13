# Overview

Python script to download, install and authenticate Roblox Studio in a CI environment.

Run with a ROBLOSECURITY cookie as an argument.

This could theoretically be used along with [rojo](https://github.com/rojo-rbx/rojo), [run-in-roblox](https://github.com/rojo-rbx/run-in-roblox) and some additional tech to parse results to create a gated CI system for Roblox projects that has full access to the Roblox API. In practice, you are likely to find [TestEZ CLI](https://github.com/Roblox/testez) with [lemur](https://github.com/LPGhatguy/lemur) a more reliable solution (see [Warnings](#Warnings)).

# Usage

Powershell:

```powershell
# Download this repo (there are currently no releases)
git clone git@github.com:OrbitalOwen/roblox-win-installer.git

# Install Roblox Studio
cd roblox-win-installer
pip install -r requirements.txt
py .\install.py $env:cookie

# Download run-in-roblox (you could also build this from source using cargo install run-in-roblox)
cd ..
Invoke-WebRequest "https://github.com/OrbitalOwen/run-in-roblox/releases/download/0.2.0/run-in-roblox.exe" -OutFile run-in-roblox.exe
.\run-in-roblox.exe -t 1800 .\file.lua
```

# Warnings

-   Ensure you check this script carefully before running it on your machine, as it takes some destructive actions.
-   The behavior this script relies on is not documented or endorsed by Roblox. It could break partially or completely at some point in the future.
