@echo off
echo Removing previous dist or build folders...
if exist build rmdir /S /Q build
if exist dist rmdir /S /Q dist

echo Building EXE...
pyinstaller --onefile --icon sudoku_icon.ico sudoku.py

echo Moving boards to EXE directory
xcopy /Y *.board dist\ 

echo Completed!