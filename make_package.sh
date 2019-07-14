python -OO -m nuitka --standalone \
                     --follow-imports \
                     --plugin-enable=qt-plugins \
                     --experimental=use_pefile \
                     "./jvmangui.py"

chmod +x "./jvmangui.dist/jvmangui"
mkdir -p "./jvmangui.dist/jvman/"
cp "./jvman/interface.ui" "./jvmangui.dist/jvman/"
