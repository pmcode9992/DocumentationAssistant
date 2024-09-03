## BattleShip

The project is a Battleship game implemented in Python. It includes functionality for creating and updating game boards, placing ships, shooting, and determining the outcome of the game. It also has networking capabilities for playing against another player over a network. The project uses dataclasses, sockets, struct, subprocess, and color manipulation for the game interface. The color.py file contains classes for handling ANSI color codes for text and background colors.

     Battleship.py
     color.py


# Battleship.py

```
### Battleship Game Functions

Here we have defined various functions related to the battleship game, including printing boards, updating player and enemy boards, checking if the player has lost, creating empty boards, handling shots, placing ships, and communicating over a network. Additionally, functions for validating coordinates and parsing player input are also included in this chunk of code.
```

### Logging, Socket, Struct, Subprocess, Dataclasses, Repeat

This chunk of code imports various modules such as logging, socket, struct, subprocess, dataclasses, and repeat. These modules are essential for handling logging, network communication, data structuring, subprocess execution, and data class creation in the battleship game. 

### Constants and Lists

- `vertical_header` defines the header for the vertical axis of the game board.
- `FIELDS` contains constants representing different states of game fields such as empty, own ship, own ship hit, enemy ship hit, miss, and own ship enemy ship hit.
- `SHIP_TYPES` contains the supported ship types in the game.
- `SHIP_NAMES` maps ship types to their names for display purposes.
- `PLAYER_SHIPS` contains the types of ships assigned to the player.

These constants and lists are used throughout the code for defining game elements, ship types, and player configurations. 

### Explanation

This part of the code sets up the initial constants, lists, and imports required for the battleship game. It defines the game board layout, field states, supported ship types, ship names, and player ship configuration. These elements are essential for initializing the game and setting up the game environment for players.

### Error(ValueError):

```python
def __init__(self, *args):
    logging.error(str(self))
    super().__init__(*args)
```

This class defines a custom error class that inherits from the ValueError class. It logs the error message and then calls the superclass `__init__` method with the given arguments.

### print_err(*args, **kwargs):

```python
print(Text.RED, *args, Cursor.FULL_RESET, **kwargs)
```

This function prints error messages in red text with a full reset of the cursor position.

### coord_valid(c: int):

```python
return 0 <= c <= 9
```

This function checks if the given coordinate `c` is valid by ensuring it falls within the range of 0 to 9.

### print_boards(board, enemy_board):

```python
<<Code snippet omitted for brevity>>
```

This function prints the player's and enemy's boards with different symbols for empty squares, own ships, own ship hits, enemy ship hits, and misses. It also clears the screen on MacOS and Linux after printing the boards.

The next chunk of code consists of error handling, a function to print error messages, a function to validate coordinates, and a function to print the game boards.

### update_player_board

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

This function takes a shot object and a board as input, updates the player board based on the shot coordinates, and returns True if a player's own ship is hit, otherwise returns False.

### update_enemy_board

```python
def update_enemy_board(shot, board):
    x = shot.x
    y = shot.y
    if shot.last_shot_hit:
        board[y][x] = ENEMY_SHIP_HIT
    else:
        board[y][x] = MISS
```

This function updates the enemy board based on the shot coordinates and whether the last shot was a hit or miss.

### player_lost

```python
def player_lost(board):
    return not any(OWN_SHIP in set(x) for x in board)
```

This function checks if the player has lost by checking if the player's own ship is present in any row of the board.

### create_empty_board

```python
def create_empty_board():
    return [10 * [0] for _ in repeat(0, 10)]
```

This function creates and returns an empty board with dimensions of 10x10.

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

The `Shot` class defines the structure of a shot in the battleship game. It contains attributes `x` and `y` to store the coordinates of the shot and `last_shot_hit` to indicate whether the last shot was a hit.

The `__bytes__` method converts the shot object into a byte representation for network communication. It ensures that the coordinates fit within 4 bits each and then packs them along with the hit information into a byte sequence.

The `decode` method is a static method that takes a byte sequence as input, unpacks it to retrieve the shot coordinates and hit information, and constructs a `Shot` object from them.

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
```

The `Network` class defines a network connection for the battleship game. It initializes the socket, connection, and server status based on the input parameters. If the `is_server` flag is set to True, it creates a new socket, binds it to the host and port, and starts listening for incoming connections. If the flag is False, it connects to a remote host using the provided host and port.

---

```python
def _server_send(self, pkt):
    self.conn.sendall(pkt)

def _client_send(self, pkt):
    self.sock.send(pkt)

def send(self, pkt):
    if self.is_server:
        return self._server_send(pkt)
    return self._client_send(pkt)
```

These methods handle sending packets over the network. Depending on whether the instance is acting as a server or client, the appropriate method is called to send the packet data.

---

```python
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

These methods handle receiving data over the network. For the server, it waits for a connection and then receives data in chunks of `BUFSIZE`. For the client, it simply receives data in chunks of `BUFSIZE`.

### Network Communication

```python
logging.debug("Waiting for Data")
while True:
    data = self.conn.recv(self.BUFSIZE)
    if not data:
        break
    return data
```

This code snippet defines a function for receiving data over a network connection. It continuously waits for data to be received and returns the data once it is received.

### Client Receive

```python
def _client_recv(self):
    data = self.sock.recv(self.BUFSIZE)
    return data
```

This code defines a method for the client to receive data from the server using the socket's recv method.

### Receive Data

```python
def recv(self):
    try:
        if self.is_server:
            return self._server_recv()
        return self._client_recv()
    except Exception:
        self.close()
```

This code snippet defines a function that determines whether to receive data as a server or client and calls the appropriate method. If an exception occurs during data reception, it closes the connection.

### Close Connection

```python
def close(self):
    self.sock.close()
    if self.conn:
        self.conn.close()
```

This code snippet defines a function to close the network connection gracefully by closing the socket and the connection if it exists.

### Context Manager

```python
def __enter__(self):
    # enables context manager
    return self

def __exit__(self, exc_type, exc_val, exc_tb):
    # enables context manager
    self.close()
```

These methods enable the network communication class to act as a context manager, allowing it to be used with the `with` statement for resource management. The `__enter__` method returns the instance, while the `__exit__` method closes the connection.

    def wanted(c):
        return c.isalnum() or c == "-" or ord(c) in range(ord("a"), ord("k"))

```
def parse_shot(s):
    # be gentle
    s = pre_process_string(s)
    s = s.lower().replace(" ", "")

    if len(s) < 2:
        raise Error("Invalid String provided")

    # convert input into numbers between 0 and 9
    try:
        x = ord(s[0]) - 97
        y = int(s[1])
    except ValueError:
        raise Error("Invalid String provided")

    if not coord_valid(x):
        raise Error("X out of bounds")

    if not coord_valid(y):
        raise Error("Y out of bounds")

    return x, y, False
```

This function processes the player's shot input by converting it into coordinates (x, y) on the game board. It performs preprocessing on the input string, checks for validity, converts alphabetic characters into numerical values, and handles exceptions appropriately. The function returns the x and y values representing the shot's location. If an error is encountered, it raises an error message.

This function `pre_process_string` is used to process a string by converting it to lowercase, filtering out unwanted characters, and translating it based on ASCII values. The input string `s` is first converted to lowercase, then a helper function `wanted` is defined to filter out alphanumeric characters, hyphens, and characters falling within the ASCII range from 'a' to 'j'. It then generates a list of ASCII characters and applies the filter to keep only the desired characters. The input string `s` is encoded to ASCII, errors are ignored, and then decoded back to ASCII, filtering the characters based on the generated translation table. The processed string is returned.

```
def ask_player_for_shot():
    while 1:
        try:
            return parse_shot(input("Shoot (Format XY, e.g. A4): "))
        except Error:
            pass
```

This function prompts the player to input their shot with a specific format (e.g., A4) and repeatedly asks the player to input a valid shot until a valid one is provided. It uses the `parse_shot` function to process the input and return the coordinates of the shot. If an error occurs during parsing, it catches the error and continues to prompt the player.

### ask_player_for_shot

The function `ask_player_for_shot` is a loop that continuously prompts the player to input a shot in the format `XY`, for example, `A4`. It catches any errors that may occur during the parsing of the shot input.

### ask_player_for_shot()

```python
def ask_player_for_shot():
    while 1:
        try:
            return parse_shot(input("Shoot (Format XY, e.g. A4): "))
        except Error:
            pass
```

This function prompts the player to input a shot in the format "XY" (e.g., A4), parses the input using the `parse_shot` function, and returns the result. It handles any errors that may occur during the input process.

### ask_player_for_ship(ship_type)

The function `ask_player_for_ship` prompts the player to place a ship of a given type. It validates the input format to ensure the ship coordinates are in the correct format `XX - YY`, for example, `A1-A5`. It then proceeds to validate the ship's position by checking if it's either vertical or horizontal, ensures it's not diagonal, checks if it's within the bounds of the board, and verifies if the ship's length matches the expected length. If any validation fails, an error message is printed, and the player is prompted again to input the ship's coordinates.

### place_ship

```python
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

This function is responsible for placing a ship on the board based on the given coordinates. It checks if the ship placement is valid, iterates over the squares to place the ship, and handles error cases like diagonal placement, single square ship, and occupied fields.

### place_ships

```python
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

The `place_ships` function iterates over the player ships, prints the boards, asks the player for ship coordinates, and places the ship on the board using the `place_ship` function. It handles errors during the ship placement process.


# color.py

## Project Documentation

### Overview
This code snippet defines classes for ANSI escape sequences to format text in the terminal. It provides options for changing text color, background color, and cursor behavior.

### Imports
No external libraries are used in this code snippet.

### Functionalities

#### Ansi Class
- `CSI = '\x1b['`: Defines the Control Sequence Introducer for ANSI escape sequences.

#### Text Class
- `DEFAULT = 39`: Default text color code
- `[BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE] = range(30, 38)`: Text color codes for various colors

#### Background Class
- `DEFAULT = 49`: Default background color code
- `[BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE] = range(40, 48)`: Background color codes for various colors

#### Cursor Class
- `BLINK = 5`: Cursor blink code

#### Text, Background, Cursor Instances
- `Text = Text()`: Instance of Text class for text formatting
- `Background = Background()`: Instance of Background class for background color formatting
- `Cursor = Cursor()`: Instance of Cursor class for cursor behavior

### Usage
You can use the instances of Text, Background, and Cursor classes to format text in the terminal by combining them with the desired text or output. For example:
```python
print(Text.RED + 'This text will be displayed in red color' + Text.DEFAULT)
print(Background.BLUE + 'This text will have a blue background' + Background.DEFAULT)
print(Cursor.BLINK + 'This text will have a blinking cursor' + Text.DEFAULT)
```
