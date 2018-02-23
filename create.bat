@echo off
echo Converting *.ui files to *.py files...

rem This doesn't use quotes, or escape unsafe file names because it assumes the developer isn't an idiot.

for %%f in (*.ui) do (
    echo %%f =^> %%~nf.py
    pyuic5 %%f -o %%~nf.py
    yapf %%~nf.py -i
)
