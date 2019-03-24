@echo off

python -m PyQt5.uic.pyuic interface.ui -o interface.py
python -m black interface.py -l 100
