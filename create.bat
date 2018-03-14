@echo off
echo Converting *.ui files to *.py files...

rem This doesn't use quotes, or escape unsafe file names because it assumes the developer isn't an idiot.
rem Also requires the yapf formatter to be installed in the system path

for %%f in (*.ui) do (
    echo %%f =^> %%~nf.py
    pyuic5 %%f -o %%~nf.py
    yapf %%~nf.py -i --style "{based_on_style: pep8, column_limit: 120}"
)
