rm -rf build dist

if !(which python3 &> /dev/null); then
    alias python3=python
fi

python3 -OO -m nuitka --standalone \
                      --follow-imports \
                      --plugin-enable=qt-plugins \
                      jvmangui.py

chmod +x "./jvmangui.dist/jvmangui"
