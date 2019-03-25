rm -rf build dist

if !(which python3 &> /dev/null); then
    alias python3=python
fi

python3 -OO -m PyInstaller --noconfirm --noupx --windowed jvmangui.py
