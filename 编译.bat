del *.pyd
del /s /q build
python setup.py build_ext --inplace
pause
