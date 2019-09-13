# John Gresl
# Written under the GNU General Public License, V3. 29 June 2007
import sys
import os

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
      board: Must either be a file containing the board or a 9x9 iterable
    """
    try:
      with open(board) as board_file:
        board = board_file.read().split("\n")
    except (TypeError, FileNotFoundError):
      # If board is not a string or a path to a valid file path, then we assume 
      # it's a 9x9 iterable and can continue
      pass
    self.board = [ [0]*9 for _ in range(9)]  # Fully empty board object
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


def start():
  args = sys.argv[1:]
  if len(args) > 1:
    print(f"sudoku.exe: Invalid arguments -- {', '.join(args)}")
    print("Try 'sudoku.exe --help' for more information.")
  if len(args) == 1:
    if args[0] == "--help":
      print("Help message!")
    else:
      print("You (might) have entered a path!")
  else:
    pass



if __name__ == "__main__":
  start()
  # my_board = SudokuBoard("multiple_solutions.board")
  # print("\n\nOriginal board:")
  # my_board.print_board()
  # my_board.find_and_print_all_solutions()
  # input("Press enter to continue...")
  
