python -OO -m nuitka --standalone \
                     --follow-imports \
                     --plugin-enable=qt-plugins \
                     --experimental=use_pefile \
                     --windows-disable-console \
                     "./jvtgui.py"

cat > "./jvtgui.dist/run_jvtgui.bat" << EOL
@echo off

set PATH=%PATH%;%~dp0

rem NOTE: If you wish, you may use variants of the Fusion theme by changing the arguments.
rem For the default Qt Fusion theme: "fusion"
rem For a custom Fusion Dark theme with a blue accent: "fusion fusion-dark"
rem With an orange accent (this is for you brother): "fusion fusion-dark orange-accent"
rem Or just nothing to let the gods decide.

set ARGS=fusion fusion-dark accent-orange

start "" jvtgui.exe %ARGS%

exit
EOL

cat > "./jvtgui.dist/run_jvtgui.sh" << EOL
#! /usr/bin/sh
export PATH="\$PATH:\${pwd}"

# NOTE: If you wish, you may use variants of the Fusion theme.

# For the default Qt Fusion theme:
# ./jvtgui fusion

# For a custom Fusion Dark theme with a blue accent:
# ./jvtgui fusion fusion-dark

For a custom Fusion Dark theme with an orange accent (this is for you brother):
# ./jvtgui fusion fusion-dark accent-orange

# Let the gods decide
./jvtgui

exit
EOL

mkdir -p "./jvtgui.dist/jvtgui/"
cp "./jvtgui/interface.ui" "./jvtgui.dist/jvtgui/"

chmod +x "./jvtgui.dist/jvtgui"
chmod +x "./jvtgui.dist/run_jvtgui.sh"