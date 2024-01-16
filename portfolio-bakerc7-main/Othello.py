# Cameron Baker
# GitHub username: bakerc7
# Date: 6/11/23
# Description: Creates a version of the game Othello, that allows two people to play. It creates
# black and white players for the game as well as establishes the board and manages moves on the
# board. The game board consists of column and rows. It starts with four pieces in the middle of
# the board. It consists of two classes. One to make a player and one to manage the game itself.
# It provides feedback to the players on their moves, whether they're valid and when a player wins.


class Player:
    """Represents a player in the game of Othello. Stores the player name and piece color.
    Instances of this class will be created and managed by the Othello class."""

    def __init__(self, player_name, color):
        """Initializes a player with the given name and piece color.
        Parameters:
        player_name: The name of the player.
        color: The color of the player's pieces, black or white."""
        self.player_name = player_name
        self.color = color


class Othello:
    """Represents the game of Othello. Manages the players and the board.
    Creates methods to play the game. It will use the Player class to
    make players for the game."""

    EMPTY = '.'
    black = 'X'
    white = 'O'

    def __init__(self):
        """Initializes the Othello game. It will make a list of players and make a board for the game."""
        self._board = [[self.EMPTY] * 10 for _ in range(10)]
        for i in range(10):
            self._board[i][0] = self._board[i][9] = '*'
            self._board[0][i] = self._board[9][i] = '*'
        self._board[4][4] = self._board[5][5] = self.white
        self._board[4][5] = self._board[5][4] = self.black
        self._players = []

    def print_board(self):
        """Prints the current board and the boundaries."""
        for row in self._board:
            print(' '.join(row))
        print()

    def create_player(self, player_name, color):
        """Creates a player object with a name and color, then adds it to the player list."""
        player = Player(player_name, color)
        self._players.append(player)

    def return_winner(self):
        """Finds and returns the winner. Returns:
        "Winner is white player: player’s name" when white
        player wins, returns "Winner is black player: player’s name"
        when black player wins, returns "It's a tie" if black and white
        player have the same number of pieces on the board when the game
        ends."""
        black_count, white_count = self.count_pieces()
        if black_count > white_count:
            for player in self._players:
                if player.color == self.black:
                    return f"Winner is black player: {player.player_name}"
        elif white_count > black_count:
            for player in self._players:
                if player.color == self.white:
                    return f"Winner is white player: {player.player_name}"
        else:
            return "It's a tie"

    def return_available_positions(self, color):
        """Returns a list of available positions for a player with a specific color to move on the board."""
        available_positions = []
        for row in range(1, 9):
            for col in range(1, 9):
                if self.is_valid_move(col, row, color):
                    available_positions.append((row, col))
        return available_positions

    def make_move(self, color, piece_position):
        """Puts a piece of the specified color at the specific position and updates the position on the board."""
        row, col = piece_position
        self._board[row][col] = self.black if color == self.black else self.white
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            x, y = row + dx, col + dy
            to_flip = []
            while 1 <= x < 9 and 1 <= y < 9 and self._board[x][y] == self.opposite_color(color):
                to_flip.append((x, y))
                x += dx
                y += dy
            if 1 <= x < 9 and 1 <= y < 9 and self._board[x][y] == color:
                for flip_x, flip_y in to_flip:
                    self._board[flip_x][flip_y] = color
        return self._board

    def opposite_color(self, color):
        """Returns the opposite color of the given color."""
        return self.black if color == self.white else self.white

    def count_pieces(self):
        """Counts the number of black and white pieces on the board.
        Returns a tuple (black_count, white_count)."""
        black_count = 0
        white_count = 0
        for row in range(1, 9):
            for col in range(1, 9):
                if self._board[row][col] == self.black:
                    black_count += 1
                elif self._board[row][col] == self.white:
                    white_count += 1
        return black_count, white_count

    def is_valid_move(self, row, col, color):
        """Checks if a move is valid for the given position and color on the board.
        Returns True if the move is valid, False otherwise."""
        if self._board[row][col] != self.EMPTY:
            return False
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        opposite_color = self.opposite_color(color)
        for dx, dy in directions:
            x, y = row + dx, col + dy
            if 1 <= x < 9 and 1 <= y < 9 and self._board[x][y] == opposite_color:
                while 1 <= x < 9 and 1 <= y < 9 and self._board[x][y] == opposite_color:
                    x += dx
                    y += dy
                if 1 <= x < 9 and 1 <= y < 9 and self._board[x][y] == color:
                    return True
        return False

    def play_game(self, player_color, piece_position):
        """
        Attempts to make a move for the player with the given color at the specified position.
        Returns:
        "Invalid move" if the position is invalid.
        The current state of the board as a 2D list if the move is valid.
        None if the game has ended, and it prints the game result.
        """
        color = self.black if player_color == "black" else self.white
        if not self.is_valid_move(piece_position[0], piece_position[1], color):
            print("Invalid move")
            print("Here are the valid moves:")
            available_positions = self.return_available_positions(color)
            print(available_positions)
            return "Invalid move"
        else:
            self.make_move(color, piece_position)
            self.print_board()

        available_positions = self.return_available_positions(self.opposite_color(color))
        if len(available_positions) == 0:
            available_positions = self.return_available_positions(color)
            if len(available_positions) == 0:
                print("Game is ended")
                black_count, white_count = self.count_pieces()
                print(f"white pieces: {white_count} black pieces: {black_count}")
                winner = self.return_winner()
                print(winner)
                return None

        return self._board
