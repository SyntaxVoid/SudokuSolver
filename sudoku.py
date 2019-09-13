# John Gresl
# Written under the GNU General Public License, V3. 29 June 2007
import sys
import os
import argparse
from _io import TextIOWrapper

class BoardSolved(Exception): 
  """ This exception should be raised when the board is solved. """
  pass


class BoardInvalid(Exception): 
  """ This exception should be raised when the board cannot be solved. """
  pass


class SudokuSquare(object):
  """ This class represents a square object on a Sudoku board """
  
  def __init__(self, row, col, sudoku_board):
    """
    Initializes the SudokuSquare object. Indexing begins at 0 and goes up to 8.
    Inputs:
      row: int - Row of the square (between 0 and 8)
      col: int - Column of the square (between 0 and 8)
      board: [[int]] - 2-D list of integers representing the entire Sudoku board
    """
    self.cur_row = row
    self.cur_col = col
    self.sudoku_board = sudoku_board
    self.valid_guesses = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    self.generate_valid_guesses()

  def generate_valid_guesses(self):
    """
    For the given square (from self.cur_row and self.cur_col), this method 
    determines the valid values for that square and stores them in the 
    self.valid_guesses array. Returns nothing because this modifies in place.
    """
    # Filter out the numbers in the row
    for row in range(9):
      if self.sudoku_board.board[row][self.cur_col] in self.valid_guesses:
        self.valid_guesses.remove(self.sudoku_board.board[row][self.cur_col])

    # Filter out the numbers in the column
    for col in range(9):
      if self.sudoku_board.board[self.cur_row][col] in self.valid_guesses:
        self.valid_guesses.remove(self.sudoku_board.board[self.cur_row][col])

    # Filter out the numbers in the 3x3 block
    for row in range((self.cur_row//3)*3, (self.cur_row//3)*3 + 3):
      for col in range((self.cur_col//3)*3, (self.cur_col//3)*3 + 3):
        if self.sudoku_board.board[row][col] in self.valid_guesses:
          self.valid_guesses.remove(self.sudoku_board.board[row][col])
    return

  def __iter__(self):
    """ Provides a way of iterating over the valid guesses. """
    for guess in self.valid_guesses:
      yield guess

  def __repr__(self):
    """
    Returns a valid representation of the current object. Should not be used to
    create a new object. Only for human-readable format """
    return f"SudokuSquare[{self.row}, {self.col}]"

  def __eq__(self, right):
    """ Compare the current square from self with the SudokuSquare on right """
    return (self.cur_row == right.cur_row) and (self.cur_col == right.cur_col)

  @property
  def row(self):
    """ Allows the user to call SudokuSquare.row to extract the row """
    return self.cur_row

  @property
  def col(self):
    """ Allows the user to call SudokuSquare.col to extract the column """
    return self.cur_col
  
  def __hash__(self):
    """
    Produces a unique value to be used in the hash-table when creating the
    solution dictionary. Collisions are impossible.
    """
    return int(f"{self.row}{self.col}")

class SudokuBoard(object):
  """ Represents an entire Sudoku board and does the high-level solving """
  
  def __init__(self, board):
    """
    Initializes the SudokuBoard object and internally generates a deep copy
    of the supplied board object. Provides no type checking. We are all
    consenting adults. If you pass the wrong kind of argument, then that is 
    YOUR fault... =)

    Inputs:
      board: Must be one of:
              1. An open text file with read permission
              2. A string containing the path to a sudoku board file
              3. A 9x9 iterable containing the board values
    """
    if isinstance(board, TextIOWrapper): # (1) from above
      board = board.read().split("\n")
    else:
      try:
        with open(board) as board_file: # (2) from above
          board = board_file.read().split("\n")
      except (TypeError, FileNotFoundError): # (3) from above (assumed)
        pass
    self.board = [ [0]*9 for _ in range(9)]
    for row in range(9):
      for col in range(9):
        self.board[row][col] = int(board[row][col])
  
  def __str__(self):
    out = ""
    dashes = "-" * 13
    numbers = "|{}{}{}|{}{}{}|{}{}{}|"
    for row in range(9):
      if row % 3 == 0:
        out += dashes + "\n"
      else:
        out += numbers.format(*self.board[row]) + "\n"
    return out


  def object_copy(self):
    """
    Creates a copy of the current object. Because __init__ explicitly creates
    a deep copy, this method returns a deepcopy.
    """
    return SudokuBoard(self.board)
  
  def make_guess(self, square, value):
    """
    Applies the value to the given square.

    Inputs:
      square: SudokuSquare object for the current SudokuBoard
      value: int - The value to apply to the given square
    """
    self.board[square.row][square.col] = value

  def undo_guess(self, square):
    """
    Undoes the application of a value to a square.
    Note: undo_guess(square) is equivalent to make_guess(square, 0)

    Inputs:
      square: SudokuSquare object for the current SudokuBoard
    """
    self.board[square.row][square.col] = 0

  def apply_guesses(self):
    """ Applies every guess """
    for row in range(9):
      for col in range(9):
        if self.board[row][col] == 0:
          return SudokuSquare(row, col, self)
    raise BoardSolved # If no 0s are in the board, then it is solved!

  def solve_first(self):
    """ Returns the first solution for the current SudokuBoard. """
    try:
      square = self.apply_guesses()
      for guess in square:
        self.make_guess(square, guess)
        guess_tree = self.object_copy().solve_first() # Make a copy and try to solve
        if len(guess_tree) != 0: # It was a good guess
          return guess_tree
        self.undo_guess(square)
    except BoardSolved: # Return the solved board
      return self.board
    except BoardInvalid:
      return {} # Triggers the self.undo_guess(square) call a few lines up
    return {} # Should never be reached anyways.

  def solve_all(self, solutions):
    """
    Finds ALL solutions to the current SudokuBoard. This method does not return
    anything, but instead should be passed an empty list for the solutions 
    parameter. The solutions will be recursively appended to this array
    and can be viewed after iteration is complete. (Kind of C++ style...)
    """
    try:
      square = self.apply_guesses()
      for guess in square:
        self.make_guess(square, guess)
        self.object_copy().solve_all(solutions)       
        self.undo_guess(square)
    except BoardSolved:
      solutions.append(self.board)
    except BoardInvalid:
      pass
    return None

  def find_and_print_solution(self):
    solution = self.solve_first()
    self.print_solution(solution)
    return

  def find_and_print_all_solutions(self):
    solutions = []
    self.solve_all(solutions)
    n_sols = len(solutions)
    grammar = ("was", "solution") if n_sols == 1 else ("were", "solutions")
    
    print(f"\nThere {grammar[0]} {len(solutions)} {grammar[1]}!")
    for n, solution in enumerate(solutions):
      print(f"Solution # {n+1}:")
      self.print_solution(solution)
      print("\n"*1)
    return

  def print_solution(self, solution):
    """ Given a solution, returned from solve_first, prints it prettily """
    
    dashes = "-" * 13
    numbers = "|{}{}{}|{}{}{}|{}{}{}|"
    for row in range(9):
      if row % 3 == 0:
        print(dashes)
      print(numbers.format(*solution[row]).replace("0", " "))
    print(dashes)

  def print_board(self):
    """ A wrapper to allow printing of a non-solution board """
    self.print_solution(self.board)


def stderr_print(*args, **kwargs):
  """ Acts just like print, but sends the output to stderr isntead of stdout """
  print(*args, **kwargs, file = sys.stderr)
  return 


def get_board_file():
  """ 
  Continuously asks the user to enter a file path until a valid path is 
  retrieved. Then attempts to return the opened file in read mode. If opening
  the file fails (because of lack of permissions or if the file was deleted
  between if-statements), an error message will be displayed and the user will
  be asked to enter another path. If any other exception occurs, a message is
  displayed, the exception is printed, and finally the original exception is
  raised. This function does no content validation on the file.

  Inputs: N/A

  Returns: An open file object to a sudoku board text file. 
  """
  while True:
    print("Enter the full or relative path to a sudoku board (q to quit)")
    print(f"    Current directory: {os.getcwd()}")
    user_in = input(">> ").strip()
    if user_in.lower() == "q":
      return None
    if not os.path.isfile(user_in):
      stderr_print("Not a valid file path.")
      continue
    try:
      return open(user_in, "r")
    except IOError:
      stderr_print("You do not have permission to read that location.")
      continue
    except FileNotFoundError: # Race condition; file could be deleted already
      stderr_print("Not a valid file path.")
      continue
    except Exception as e:
      stderr_print("Unexpected exception.")
      stderr_print(str(e))
      raise e
    
def pause(msg = "Press enter to continue. . ."):
  """ Displays msg and waits for user to enter. Does nothing with the input """
  input(msg)
  return

def get_usage():
  if sys.argv[0].endswith(".py"):
    return "python sudoku.py [-h] [-f FILE] [-a]"
  else:
    return "sudoku [-h] [-f FILE] [-a]"
  return

def start():
  """
  Main function to run when starting sudoku. Creates the argument parser
  and parses the arguments from the command line. The description of each
  argument is below
  
    1. -f FILE or --file FILE: FILE should be a path to a valid board file.
       This argument is optional. If it is not supplied, the user is asked
       to manually enter the path to a file.
    2. -a or --all: Boolean flag. Used to determine if _all_ solutions should
       be found for the board or just the first solution. This argument is
       optional. If it is supplied, args.all is set to True. Otherwise, 
       args.all is set to False.
    3. -h or --help: Displays a help message
  
  If any exception occurs after the arguments have been parsed, any open file
  object is guaranteed to be closed. An error message is then printed, followed
  by the actual exception. The exceptions is then re-raised, potentially
  printing it twice. The function pauses at the end to ensure the window 
  doesn't close after completion.

  Returns None
  """
  parser = argparse.ArgumentParser(description = "Sudoku Solver",
                                   usage = get_usage())
  parser.add_argument("-f", "--file", 
                      help = "File to the sudoku board", 
                      type = argparse.FileType("r", encoding = "UTF-8"))
  parser.add_argument("-a", "--all", 
                      help = "Find ALL solutions to the given board",
                      action = "store_true")
  args = parser.parse_args()
  try:
    if args.file is not None:
      file_object = args.file
    else:
      file_object = get_board_file()
      if file_object is None: # User aborted
        return
    my_board = SudokuBoard(file_object)
    file_object.close() # No longer need it!
    file_object = None
    print("\n\nOriginal Board:")
    my_board.print_board()
    pause("\nPress enter to solve your board. . .")
    if args.all:
      my_board.find_and_print_all_solutions()
    else:
      my_board.find_and_print_solution()
  except Exception as e:
    if file_object is not None:
      file_object.close()
      stderr_print("An unknown exception occured, open file resources freed.")
      stderr_print(str(e))
      raise e
  pause()
  return None


if __name__ == "__main__":
  start()  
