![roblox-win-installer](https://github.com/OrbitalOwen/roblox-win-installer/workflows/roblox-win-installer/badge.svg)

_This installer is brittle and can break with changes to the Roblox Studio installer. An actions workflow runs every 12 hours to verify it is working correctly and its status can be seen above._

# Overview

Python script to download, install and authenticate Roblox Studio in a CI environment.

Run with a ROBLOSECURITY cookie as an argument.

This can be used along with [rojo](https://github.com/rojo-rbx/rojo), [run-in-roblox](https://github.com/rojo-rbx/run-in-roblox) and GitHub Actions / AppVeyor / others to create a gated CI system for Roblox projects that has full access to the Roblox API. In practice, you may find [TestEZ CLI](https://github.com/Roblox/testez) with [lemur](https://github.com/LPGhatguy/lemur) a more reliable solution (see [Warnings](#Warnings)).

# Usage

If you are using GitHub Actions, it is recommended you use [roblox-win-installer-action](https://github.com/OrbitalOwen/roblox-win-installer-action). This is less verbose, and will automatically use the most recent version.

```yml
- uses: OrbitalOwen/roblox-win-installer-action@1.0
  with:
      cookie: ${{ secrets.ROBLOSECURITY }}
      token: ${{ secrets.GITHUB_TOKEN }}
```

Alternatively, if you are using Powershell:

```powershell
Invoke-WebRequest -Uri "https://github.com/OrbitalOwen/roblox-win-installer/archive/0.4.zip" -OutFile roblox-win-installer.zip
Expand-Archive -LiteralPath roblox-win-installer.zip -DestinationPath .
cd roblox-win-installer-0.4
pip install -r requirements.txt
python install.py "${{ secrets.ROBLOSECURITY }}"
```

# Warnings

-   Ensure you check this script carefully before running it on your machine, as it takes some destructive actions.
-   The behavior this script relies on is not documented or endorsed by Roblox. It could break partially or completely at some point in the future.
-   The install script has no built in timeout and can run indefinitely. Adding a timeout limit to its execution is strongly advised (ie `timeout-minutes` in Github Actions)
