@echo off

rem magick convert bonjour.png -define icon:auto-resize=16,32,48,64,128,256 bonjour.ico

python -OO -m PyInstaller --ascii ^
                          --console ^
                          --onefile ^
                          --name BonjourInstaller ^
                          --icon bonjour.ico ^
                          install.py
