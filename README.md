# SudokuSolver
General sudoku solver written in python 3 without any external dependencies.

## [Cloning SudokuSolver to your local directory][100]
Navigate to where you want to clone SudokuSolver. Note that cloning *will* create a "SudokuSolver" folder itself.

```
$ git clone https://github.com/syntaxvoid/SudokuSolver.git
```

## [Using the program][101]
Open a command prompt and navigate to the folder containing sudoku.py. Then run
```
python sudoku.py
```
Soon, you will be able to specify a file with the board in the command line. As of right now, you must edit the name of the file near the bottom of the `sudoku.py` file


# [Contributing your own code][102]
## [Setting remote origin][103]
If you want to make your own contributions, make sure you're a collaborator. Once you're a collaborator, run the following to make the master branch the default, replacing YOUR\_GITHUB\_USERNAME with your github.com username.

```
$ cd SudokuSolver
$ git remote rm origin
$ git remote add origin https://YOUR_GITHUB_USERNAME@github.com/syntaxvoid/SudokuSolver.git
```

## [Daily Workflow][104]
* Start by pulling changes made by others.

```
$ git pull origin master
```

* Make your own changes and stage them for comitting. 
```
$ git add my_new_file.py
$ git add my_new_file2.py
```

* Commit your changes. 

```
$ git commit -m "Summarize your changes."
```

* Push your changes to the master branch. If you get an error about https request denied, make sure you complete the 'Setting remote origin' section.

```
$ git push -u origin master
```

## [Forking][105]
Feel free to fork your own version and submit a pull request (which will add yourself as a contributor).

## [Building into a .EXE][999]
### *In progress*
Make sure you have pyinstaller installed. Type `pyinstaller` in any command prompt; if you see a help message then it's installed. If you need to install pyinstaller, run
```
$ pip install pyinstaller
```

Then change directory to wherever sudoku.py is located and execute the builder batch script (this only works for windows)
```
$ builder
```
Say yes to any prompts (if they appear). This will create two folders: "dist", and "build". The executable you need to run is found under "dist/" and is named sudoku.exe

Now run `SudokuSolver\dist\sudoku.exe` and let the Sudoku solving begin.

# Remember to [submit any issues][1]!


[1]: https://github.com/SyntaxVoid/SudokuSolver/issues/new

[100]: https://github.com/SyntaxVoid/SudokuSolver#cloning-sudokusolver-to-your-local-directory
[101]: https://github.com/SyntaxVoid/SudokuSolver#using-the-program
[102]: https://github.com/SyntaxVoid/SudokuSolver#contributing-your-own-code
[103]: https://github.com/SyntaxVoid/SudokuSolver#setting-remote-origin
[104]: https://github.com/SyntaxVoid/SudokuSolver#forking
[105]: https://github.com/SyntaxVoid/SudokuSolver#daily-workflow
[999]: https://github.com/SyntaxVoid/SudokuSolver#building-into-a-exe

