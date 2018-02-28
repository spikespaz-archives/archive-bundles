@echo off
python -OO -m PyInstaller --ascii ^
                          --console ^
                          --onefile ^
                          --name BonjourInstaller ^
                          -icon bonjour.ico ^
                          install.py
