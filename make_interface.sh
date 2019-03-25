if !(which python3 &> /dev/null); then
    alias python3=python
fi

python3 -m PyQt5.uic.pyuic interface.ui -o jvman/interface.py
python3 -m black jvman/interface.py -l 100
