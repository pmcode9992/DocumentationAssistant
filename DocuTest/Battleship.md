## Battleship

The project is a Python implementation of the classic Battleship game. It consists of two code files: Battleship.py and color.py. Battleship.py contains classes and functions for the game implementation, including creating game boards, updating player and enemy boards, handling shots, and managing network communication for multiplayer gameplay. color.py contains classes for handling ANSI escape codes for text and background colors in the terminal.

Technologies used in the project include dataclasses, sockets for networking, and ANSI escape codes for styling the game output. The project allows players to place their ships, take shots, and play against each other in a turn-based fashion. It also includes error handling for user input validation.

     Battleship.md
     Battleship.py
     color.py


#Battleship.md


#Battleship.py

```
### Main Function

def main():
    # Initialize the game
    player1_board = create_board()
    player2_board = create_board()
    player1_ships = place_ships()
    player2_ships = place_ships()

    # Game loop
    while True:
        # Player 1's turn
        print_board(player1_board, player2_ships)
        player1_shot = get_player_shot()
        update_board(player1_shot, player2_board, player2_ships)
        if check_loss(player2_ships):
            print("Player 1 wins!")
            break

        # Player 2's turn
        print_board(player2_board, player1_ships)
        player2_shot = get_player_shot()
        update_board(player2_shot, player1_board, player1_ships)
        if check_loss(player1_ships):
            print("Player 2 wins!")
            break
```

This chunk of code contains the main function that initializes the game by creating boards for both players, placing ships on the boards, and then enters a game loop where players take turns shooting at each other's ships. The function prints the game boards, gets player shots, updates the boards based on the shots, and checks for a player's loss to determine the winner. The game continues until one of the players loses all their ships.

### logging, socket, struct, subprocess, dataclass, repeat

The code snippet imports various modules like logging, socket, struct, subprocess, dataclass, and repeat for different functionalities such as logging, network communication, data structuring, subprocess management, data class creation, and iterating over elements.

### vertical_header, FIELDS, SHIP_TYPES, SHIP_NAMES, PLAYER_SHIPS

The code defines constants like vertical_header for displaying the header of the game board, FIELDS for different states of the game board cells, SHIP_TYPES for supported ship types with their lengths, SHIP_NAMES for mapping ship types to their names, and PLAYER_SHIPS for defining the types of ships a player can place on the board.

It is setting up the necessary configurations and data structures for the battleship game implementation.

### Error

```python
class Error(ValueError):
    def __init__(self, *args):
        logging.error(str(self))
        super().__init__(*args)
```

This class defines a custom error class that logs the error message and calls the parent class `ValueError` with the given arguments.

### print_err

```python
def print_err(*args, **kwargs):
    print(Text.RED, *args, Cursor.FULL_RESET, **kwargs)
```

This function prints an error message in red color using `Text.RED` constant and resets the cursor position.

### coord_valid

```python
def coord_valid(c: int):
    return 0 <= c <= 9
```

This function checks if the given coordinate `c` is valid within the range of 0 to 9.

### print_boards

```python
def print_boards(board, enemy_board):
    # Code snippet omitted for brevity
```

This function prints the game boards with ships, hits, and misses for both the player's board and the enemy's board. It formats the output to display the boards side by side with different colors for different elements. It also clears the screen on OSX and Linux before printing the boards.

No main function found in this chunk of code.

### create_empty_board()

```python
def create_empty_board():
    return [10 * [0] for _ in repeat(0, 10)]
```

This function creates and returns a 10x10 empty game board filled with zeros.

### update_player_board()

```python
def update_player_board(shot, board):
    x = shot.x
    y = shot.y
    field = board[y][x]
    if field == OWN_SHIP:
        board[y][x] = OWN_SHIP_HIT
        return True
    return False
```

This function updates the player's board based on the shot fired. If the shot hits the player's own ship, it marks the hit on the board and returns True. Otherwise, it returns False.

### update_enemy_board()

```python
def update_enemy_board(shot, board):
    x = shot.x
    y = shot.y
    if shot.last_shot_hit:
        board[y][x] = ENEMY_SHIP_HIT
    else:
        board[y][x] = MISS
```

This function updates the enemy's board based on the shot fired. If the last shot was a hit, it marks the hit on the board. Otherwise, it marks a miss.

### player_lost()

```python
def player_lost(board):
    return not any(OWN_SHIP in set(x) for x in board)
```

This function checks if the player has lost the game by checking if their own ship is still present on the board. If no own ship is found on the board, it returns True indicating that the player has lost. 

@Dataclass

This annotation is used to create data classes in Python for storing data. It simplifies the process of defining classes with attributes.

### Shot

```python
class Shot:
    x: int
    y: int
    last_shot_hit: bool = False

    def __bytes__(self):
        if self.x >= 2**4:
            raise Error(
                f"X={self.x} is too large to fit into 4 bit: {hex(self.x)} > 0xf."
            )
        if self.y >= 2**4:
            raise Error(
                f"X={self.y} is too large to fit into 4 bit: {hex(self.y)} > 0xf."
            )

        return struct.pack("!BB", (self.x << 4) | self.y, int(self.last_shot_hit) << 7)

    @staticmethod
    def decode(pkt):
        xy, h = struct.unpack("!BB", pkt)
        return Shot(xy >> 4, xy & 0xF, h >> 7)
```

The `Shot` class represents a shot in the battleship game. It has attributes `x` and `y` representing coordinates, and `last_shot_hit` indicating if the last shot was a hit. The `__bytes__` method converts the shot object to bytes, packing `x` and `y` into a byte and storing `last_shot_hit` in the last bit. The `decode` method unpacks the byte data to recreate a `Shot` object with coordinates and hit status.

### Network

```python
BUFSIZE = 16

def __init__(self, host, port, is_server):

    self.is_server = is_server
    self.sock = None
    self.conn = None

    if self.is_server:
        # Create a new socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()
        logging.debug("Server is listening on port " + str(port))

    else:
        # Connect to a remote host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

def _server_send(self, pkt):
    self.conn.sendall(pkt)

def _client_send(self, pkt):
    self.sock.send(pkt)

def send(self, pkt):
    if self.is_server:
        return self._server_send(pkt)
    return self._client_send(pkt)

def _server_recv(self):
    if self.conn is None:
        while True:
            logging.debug("Server is waiting for a connection.")
            self.conn, self.addr = self.sock.accept()
            break

    logging.debug("Waiting for Data")
    while True:
        data = self.conn.recv(self.BUFSIZE)
        if not data:
            break
        return data

def _client_recv(self):
    data = self.sock.recv(self.BUFSIZE)
    return data
```

This class defines a network communication interface for the battleship game. It includes methods for initializing the network connection, sending and receiving data, and handling server and client behaviors. The `__init__` method sets up the socket based on whether the instance is a server or a client. The `send` method determines whether to use `_server_send` or `_client_send` based on the instance type. The `_server_recv` and `_client_recv` methods handle receiving data from the server and client sockets, respectively.

### Network Communication

The provided code snippet is responsible for handling network communication in the battleship game. It includes functions for sending and receiving data over the network, closing connections, and enabling context management.

The `logging.debug("Waiting for Data")` statement is used for logging purposes to indicate that the program is waiting to receive data.

The `while True:` loop continuously receives data from the connection using `self.conn.recv(self.BUFSIZE)`. If no data is received, the loop breaks. The received data is then returned.

The `_client_recv` function is used to receive data when the program is acting as a client and uses `self.sock.recv(self.BUFSIZE)` to receive data from the socket.

The `recv` function determines whether the program is acting as a server or client and calls the respective receive function. If an exception occurs during receiving data, the `close` function is called to close the connections.

The `close` function closes the socket connection and the client connection if it exists.

The `__enter__` and `__exit__` functions enable the context manager functionality for the network communication class. The `__exit__` function ensures that the connections are closed when exiting the context.

### pre_process_string

This function takes a string as input and preprocesses it by converting it to lowercase and filtering out unwanted characters according to the criteria specified. It then returns the cleaned string.

### parse_shot

This function processes the player's shot input by preprocessing the string, converting it to lowercase, and removing spaces. It then extracts the X and Y coordinates from the input string after performing validity checks and returns them.

### ask_player_for_shot

This function prompts the player to input their shot in the specified format and repeatedly asks for input until a valid shot is provided, using the `parse_shot` function.

### ask_player_for_shot

    def ask_player_for_shot():
        while 1:
            try:
                return parse_shot(input("Shoot (Format XY, e.g. A4): "))
            except Error:
                pass

Explanation:
This function prompts the player to input a shot in the format XY (e.g., A4) and returns the parsed shot. It repeatedly asks the player if an incorrect format is provided until a valid shot format is entered.

### ask_player_for_ship

    def ask_player_for_ship(ship_type):
        length = ship_type
        while True:
            s = input(
                f"Place your {SHIP_NAMES.get(ship_type)} (length: {length}) formatted as XX - YY (e.g. A1-A5): "
            )
            # assume the following format: XX - YY and ask until the user enters something valid
            try:
                a, b = s.lower().replace(" ", "").split("-")
                a0, a1, _ = parse_shot(a)
                b0, b1, _ = parse_shot(b)

                # validate ship
                # ships can be either vertical or horizontal
                # so only one dimension can change: a-z or 1-9
                if a0 != b0 and a1 != b1:
                    print_err("Ships cannot be diagonal.")
                    continue

                # out of bounds
                if any([not coord_valid(x) for x in [a0, a1, b0, b1]]):
                    print_err("Ships coordinates out of bounds.")
                    continue

                # length
                if max(abs(a0 - b0), abs(a1 - b1)) != (length - 1):
                    print_err(f"Ship must be exactly {length} fields long.")
                    continue

                return (a0, a1), (b0, b1)

            except (IndexError, ValueError) as e:
                print_err("Invalid Format: ", str(e)

Explanation:
This function prompts the player to place a ship of a specific type on the board. It verifies that the ship is placed within the board's boundaries, is of the correct length, and is either vertical or horizontal. The function loops until a valid ship placement format is entered by the player.

### place_ship(a, b, board)

```
def place_ship(a, b, board):
    a0, a1 = a
    b0, b1 = b

    if a0 != b0 and a1 != b1:
        raise Error("Ship cannot be diagonal")

    if a0 == b0 and a1 == b1:
        raise Error("Ship must have more than one square")

    # iterate over the squares until a0 == b0 and b1 == b1
    while True:
        if board[a1][a0] != EMPTY:
            raise Error("Field already occupied")

        board[a1][a0] = OWN_SHIP

        if a0 != b0:
            a0 += 1 * (-1 if a0 > b0 else 1)

        elif a1 != b1:
            a1 += 1 * (-1 if a1 > b1 else 1)

        if a0 == b0 and a1 == b1:
            board[a1][a0] = OWN_SHIP
            return
```

This function is used to place a ship on the board based on the given coordinates. It checks if the ship is being placed diagonally, ensures that the ship has more than one square, and verifies if the field is already occupied. The ship placement progresses based on the given coordinates until it reaches the final position.


### place_ships(board, enemy_board)

```
def place_ships(board, enemy_board):
    for ship in PLAYER_SHIPS:
        print_boards(board, enemy_board)
        while 1:
            try:
                coords = ask_player_for_ship(ship)
                place_ship(*coords, board)
                break
            except ValueError as err:
                print_err(str(err))
```

This function iterates over the player ships, prints the game boards, and prompts the player to place ships by asking for coordinates. It then calls the `place_ship` function to actually place the ship on the board. If an error occurs during the ship placement, it notifies the player.


#color.py

# Ansi Color Codes Documentation

## Imports
```python
# No imports needed
```

## Functionalities
- `CSI` is a constant representing the ANSI color escape sequence.

### Class: Ansi
- `FULL_RESET`: Represents the ANSI code for a full reset.

### Class: Text
- `DEFAULT`: Default text color.
- Colors: Black, Red, Green, Yellow, Blue, Magenta, Cyan, White.

### Class: Background
- `DEFAULT`: Default background color.
- Colors: Black, Red, Green, Yellow, Blue, Magenta, Cyan, White.

### Class: Cursor
- `BLINK`: Represents the ANSI code for a blinking cursor.

### Initialization
```python
Text = Text()
Background = Background()
Cursor = Cursor()
```
