@echo off
echo Converting *.ui files to *.py files...

for %%f in (*.ui) do (
    echo %%f =^> %%~nf.py
    pyuic5 %%f -o %%~nf.py
)
