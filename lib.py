def int_prompt(text: str, lo: int, hi: int) -> int:
    """Prompts user for int within a range, with error handling"""
    while True:
        user_in = input(f'Select a{text} between {lo} and {hi}: ')
        try:
            val = int(user_in)
            if val not in range(lo, hi+1):
                raise ValueError
            break
        except ValueError:
            print('\nInvalid entry - try again')
    return val

def count_tokens(list: str, token: str, goal: int) -> bool:
    """Returns true if unbroken sequence of tokens in list meets or exceeds goal"""
    counter = 0
    result = False
    for x in list:
        if x == token:
            counter += 1
            result = counter >= goal #check if goal has been met
        else:
            counter = 0
    return result

class Board():
    def __init__(self, rows: int, columns: int):
        self.rows = rows #number of rows
        self.cols = columns #number of columns
        
        self.contents = [' ' for x in range(self.cols * self.rows)] #board unravelled into a single list
        self._print_y_rule = True #display y-axis ruler
        #visual elements:
        self._border = ["---" for x in range(self.cols)]
        self._line = ["- +" for x in range(self.cols)]
        self._x_rule = [str(x) for x in range(1, self.cols + 1)]
        self._y_rule = [str(x) for x in range(1, self.rows + 1)]

    def wipe(self):
        """Clears the board"""
        self.contents = [' ' for spot in self.contents]

    def grid(self) -> list:
        """Returns the board as a list (rows) of lists (cols)"""
        return [self.contents[i * self.cols:(i+1) * self.cols]for i in range(self.rows)]
        
    def display(self):
        """Prints the formatted board"""
        grid = self.grid() #redraw board grid
        print('\n   ', '   '.join(self._x_rule), '  X') #X axis
        print('  ', ' '.join(self._border)) #top border

        for row in range(self.rows):
            if self._print_y_rule: 
                opener = self._y_rule[row] #Y axis
            else:
                opener = ' '
            print(opener, '|', ' | '.join(grid[row]), '|') #print each row
            if row < (self.rows - 1):
                print('  +', ' '.join(self._line)) #print lines between rows

        print('  ', ' '.join(self._border)) #bottom border

        if self._print_y_rule:
            print('Y\n')
        else:
            print('\n')
    
    def blank_space(self) -> bool: 
        """Returns True if blank space left on board"""
        return ' ' in self.contents
    
    def spot_empty(self, x: int, y: int) -> bool:
        """Returns true if spot at coordinates is empty"""
        return self.contents[x + (y * self.cols)] == ' '

    def add_piece(self, token: str, x: int, y: int):
        """Add token to board at given coordinates"""
        if self.spot_empty(x, y): #check if spot is empty
            self.contents[x + (y * self.cols)] = token #place token at spot
        else:
            raise ValueError

class Player():
    def __init__(self, token: str):
        self.token = token
        
    def choose(self, board: Board) -> tuple:
        """Prompt player for x and y coordinates of chosen space"""
        x = int_prompt('n X coordinate', 1, board.cols) - 1
        if board._print_y_rule:
            y = int_prompt(' Y coordinate', 1, board.rows) - 1
        else:
            y = None
        return (x, y)

class Game():
    def __init__(self, board: Board, num_players: int, goal: int):
        self.board = board
        self.num_players = num_players
        self.goal = goal
        self.players = []
        self.winner = None
    
    def check_win(self, player: Player, x: int, y: int) -> bool:
        """Checks column, row and both diagonals for player victory"""
        b = self.board
        grid = b.grid()

        #col = [b.contents[x + (i * b.cols)] for i in range(b.rows)]
        col = [grid[i][x] for i in range(b.rows)] 
        if count_tokens(col, player.token, self.goal): #check column victory
            self.winner = player

        #row = b.contents[(y * b.cols):((y * b.cols) + b.cols)]
        row = grid[y]
        if count_tokens(row, player.token, self.goal): #check row victory
            self.winner = player

        diag1 = [grid[r][c] for r in range(b.rows) for c in range(b.cols) if (r - c) == (x - y)] #diag \
        if count_tokens(diag1, player.token, self.goal): #check diagonal victory 2
            self.winner = player
        
        diag2 = [grid[r][c] for r in range(b.rows) for c in range(b.cols) if (r + c) == (x + y)] #diag /
        if count_tokens(diag2, player.token, self.goal): #diagonal victory 1 
            self.winner = player

    def move(self, player: Player):
        """Prompts player for move coordinates and passes them to board, with error handling, then checks win condition for player"""
        print('Place your game piece on the board')
        while True:
            coords = player.choose(self.board)
            x = coords[0]
            if self.board._print_y_rule:
                y = coords[1]
            else:
                for i in reversed(range(self.board.rows)): #check for spaces in column bottom to top
                    y = i
                    if self.board.spot_empty(x, y): #set y to lowest empty space in column
                        break
            try:
                self.board.add_piece(player.token, x, y)
                break
            except ValueError:
                print('\nChosen space must be empty - try again')
        self.check_win(player, x, y)

class TicTacToe(Game):
    def __init__(self, board=Board(3, 3), num_players=2, goal=3):
        super().__init__(board, num_players, goal)
        self.players = [Player('x'), Player('○')]
        board._print_y_rule = True

class Connect4(Game):
    def __init__(self, board=Board(6, 7), num_players=2, goal=4):
        super().__init__(board, num_players, goal)
        self.players = [Player('@'), Player('○')]
        board._print_y_rule = False #only display X-axis ruler