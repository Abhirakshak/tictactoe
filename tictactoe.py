import random

class Player:
    def __init__(self, marker="X", is_human=True):
        self._marker = marker   #both attributes are non public 
        self._is_human = is_human

    @property      #marker getter
    def marker(self):
        return self._marker
    
    @property      #is human getter
    def is_human(self):
        return self._is_human
    
    def get_player_move(self, board):
        if self._is_human:
            return self.get_human_move(board)
        else:
            return self.get_computer_move(board)

    def get_human_move(self, board):
        move = input("Enter your move (X)") 

        #checks if move is made in valid format and if it done in an empty space.
        while not(self.is_move_valid(move, board)):
            move = input("Invalid input. Please enter row and column of your move. (Example: 1A). Move must be done on an empty space")
        return move
    
    def get_computer_move(self, board):
        row = random.choice(["1", "2", "3"])   #in video 1,2 and 3 are integers
        col = random.choice(["A", "B", "C"])     
        move = row + col

        while not(self.is_move_valid(move, board)):
            row = random.choice(["1", "2", "3"])   #in video 1,2 and 3 are integers
            col = random.choice(["A", "B", "C"])     
            move = row + col

        print(f"Computer's move is (O): {move}")
        return move
    
        #checks validity of user inputted move
    def is_move_valid(self, move, board):
        row_index = int(move[0]) - 1
        col_index = Board.COLUMNS[move[1]]
        value = board.game_board[row_index][col_index]
        return((len(move) == 2) and (move[0] in Board.ROWS) and (move[1] in Board.COLUMNS) and (value == Board.EMPTY))
    
class Board:

    EMPTY = 0  #empty cells on board are denoted by 0
    COLUMNS = {"A": 0, "B": 1, "C": 2}
    ROWS = ("1", "2", "3")  #tuples are immutable

    def __init__(self, game_board=None):
        if game_board:   #why does this condition work?
            self.game_board = game_board    #why is it public?
        
        else:
            self.game_board = [[0, 0, 0], 
                               [0, 0, 0], 
                               [0, 0, 0]]

    #method to print the board
    def print_board(self):
        print("    A   B   C")
        for i, row in enumerate(self.game_board, 1):
            print(i, end=" | ")
            for col in row:
                if col != Board.EMPTY:
                    print(col, end=" | ")
                else:
                    print("  | ", end="")
            print("\n---------------")

    #submits move of player
    def submit_move(self, move, player):
        row_index = int(move[0]) - 1    #get row index of move
        col_index =  Board.COLUMNS[move[1]] #get value of key(move[1]) from the dict and use as column index of move
        self.game_board[row_index][col_index] = player.marker
        
    #The following methods is to determine the winner of the game
    # row and col are assumed to be passed as strings into each method

    def is_winner(self, player, row, col):
        if (self.check_row(row, player)) or (self.check_col(col, player)) or (self.check_diagonal(player)) or (self.check_antidiagonal(player)):
            return True
        else:
            return False 

    def check_row(self, row, player):
        row_index = int(row) - 1
        board_row = self.game_board[row_index]

        #checks if row is filled with player's markers
        if board_row.count(player.marker) == 3:
            return True
        else:
            return False

    def check_col(self, col, player):
        col_index = Board.COLUMNS[col]
        total_markers = 0

        #checks if column is filled with player's marker
        for i in range(3):
            if self.game_board[i][col_index] == player.marker:
                total_markers += 1

        if total_markers == 3:
            return True
        else:
            return False

    def check_diagonal(self, player):
        total_markers = 0
        for i in range(3):
            if self.game_board[i][i] == player.marker:
                total_markers += 1

        if total_markers == 3:
            return True
        else:
            return False
        

    def check_antidiagonal(self, player):
        total_markers = 0
        for i in range(3):
            if self.game_board[i][2 - i] == player.marker:
                total_markers += 1
                
        if total_markers == 3:
            return True
        else:
            return False

    def check_tie(self):
        total_empty = 0  #counts number of empty cells
        for row in self.game_board:
            total_empty += row.count(Board.EMPTY)
        
        if total_empty == 0:
            return True
        else:
            return False

# Game implementation (main function)

#game display header
print("______________________________________________ \n\n")
print("Welcome to the Single Player Tic Tac Toe Game\n\n")
print("______________________________________________")

board = Board()   #create board instance
player = Player()  #create user's instance
computer = Player("O", False) #create computer AI bot's instance

board.print_board() #print initial board

while True:  #must change so that there is no infinite loop or break statements

    #checking for tie
    is_tie = board.check_tie()
    if is_tie:
        print("The game has ended in a tie")
        break

    #ask human player move
    move = player.get_player_move(board)
    #submit move
    board.submit_move(move, player)
    #print updated board
    board.print_board()

    if board.is_winner(player, move[0], move[1]):
        print("You win!")
        break  #must change method so that there is no infinite loop or break statements

    #ask computer player to move
    comp_move = computer.get_player_move(board)
    #submit move
    board.submit_move(comp_move, computer)
    #print board
    board.print_board()

    if board.is_winner(computer, comp_move[0], comp_move[1]):
        print("The computer won!")
        break