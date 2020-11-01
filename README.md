# Overview

Python script to download, install and authenticate Roblox Studio in a CI environment.

Run with a ROBLOSECURITY cookie as an argument.

This could theoretically be used along with [rojo](https://github.com/rojo-rbx/rojo), [run-in-roblox](https://github.com/rojo-rbx/run-in-roblox) and GitHub Actions / AppVeyor / others to create a gated CI system for Roblox projects that has full access to the Roblox API. In practice, you may find [TestEZ CLI](https://github.com/Roblox/testez) with [lemur](https://github.com/LPGhatguy/lemur) a more reliable solution (see [Warnings](#Warnings)).

# Usage

Powershell:

```powershell
Invoke-WebRequest -Uri "https://github.com/OrbitalOwen/roblox-win-installer/archive/0.2.zip" -OutFile roblox-win-installer.zip
Expand-Archive -LiteralPath roblox-win-installer.zip -DestinationPath .
cd roblox-win-installer-0.2
pip install -r requirements.txt
python install.py "${{ secrets.ROBLOSECURITY }}"
```

# Warnings

- Ensure you check this script carefully before running it on your machine, as it takes some destructive actions.
- The behavior this script relies on is not documented or endorsed by Roblox. It could break partially or completely at some point in the future.
- The install script has no built in timeout and can run indefinitely. Adding a timeout limit to its execution is strongly advised (ie `timeout-minutes` in Github Actions)
