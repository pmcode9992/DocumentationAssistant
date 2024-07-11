## Battleship

content='Overall Summary:\nThe project is a Battleship game implemented in Python. It includes functionalities such as creating and updating game boards, placing ships, shooting at enemy ships, and determining if a player has lost. The code also includes networking capabilities for playing the game over a network. Technologies used include socket programming for networking, dataclasses for defining data structures, and color for text formatting. The project aims to provide a classic Battleship game experience with additional features like network play.' response_metadata={'token_usage': {'completion_tokens': 94, 'prompt_tokens': 2550, 'total_tokens': 2644}, 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-5b2f87a6-ca91-496a-81f5-0f2bccad0d58-0' usage_metadata={'input_tokens': 2550, 'output_tokens': 94, 'total_tokens': 2644}

     Battleship.py
     Battleship.md


#Battleship.py

### Function: check_win(player_board)

```python
def check_win(player_board):
    for row in player_board:
        for cell in row:
            if cell == SHIP:
                return False
    return True
```

This function `check_win` takes a player's game board as input and iterates through each cell on the board. If it finds any cell that contains a ship, it returns `False` indicating that the player has not won yet. If no ships are found on the board, it returns `True` indicating that the player has lost all their ships and the game is over.

### Import Statements

- `logging`
- `socket`
- `struct`
- `subprocess as sp`
- `dataclass` from `dataclasses`
- `repeat` from `itertools`
- `Text`, `Background`, `Cursor` from `color`

These import statements bring in necessary modules and classes for the Battleship game implementation. 

### Constants and Variables

- `vertical_header`: A string representing the vertical header of the game board.
- `FIELDS`: A list of constants representing different states on the game board.
- `SHIP_TYPES`: A list of supported ship types with their lengths.
- `SHIP_NAMES`: A dictionary mapping ship types to their names.
- `PLAYER_SHIPS`: A list of ship types that belong to the player.

These constants and variables are crucial for setting up the game board, ship types, and player-specific settings.

### `Error` Class

```python
class Error(ValueError):
    def __init__(self, *args):
        logging.error(str(self))
        super().__init__(*args)
```

This class defines an error handling mechanism that logs errors and raises a `ValueError` with the given arguments.

### `print_err` Function

```python
def print_err(*args, **kwargs):
    print(Text.RED, *args, Cursor.FULL_RESET, **kwargs)
```

This function prints the arguments in red color and resets the cursor. It is used for printing error messages.

### `coord_valid` Function

```python
def coord_valid(c: int):
    return 0 <= c <= 9
```

This function checks if a given coordinate `c` is valid within the game board, which is from 0 to 9.

### `print_boards` Function

```python
def print_boards(board, enemy_board):
    # Code snippet
```

This function is responsible for printing the player's board and the enemy's board in a formatted manner. It uses different colors and characters to represent different states on the board. After printing the boards, it clears the screen for better visibility.

### create_empty_board()

```python
def create_empty_board():
    return [10 * [0] for _ in repeat(0, 10)]
```

This function creates and returns an empty game board with dimensions 10x10 filled with zeros.


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

This function updates the player's board based on the shot taken. If the shot hits the player's own ship, it marks the corresponding position as hit (OWN_SHIP_HIT) and returns True. Otherwise, it returns False.


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

This function updates the enemy's board based on the shot taken. If the last shot was a hit, it marks the corresponding position as hit (ENEMY_SHIP_HIT). Otherwise, it marks it as a miss (MISS).


### player_lost()

```python
def player_lost(board):
    return not any(OWN_SHIP in set(x) for x in board)
```

This function checks if the player has lost by checking if there are no more own ships (OWN_SHIP) left on the board. If there are no own ships remaining, it returns True indicating that the player has lost.

### Shot

```
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

The `Shot` class represents a shot taken in the Battleship game. It has attributes `x` and `y` representing the coordinates of the shot, and `last_shot_hit` indicating whether the last shot was a hit or not. The `__bytes__` method converts the shot object into bytes by packing the coordinates and hit status into a binary format. The `decode` static method decodes a packet of bytes back into a `Shot` object by unpacking the coordinates and hit status. It handles errors for coordinates exceeding 4 bits.

### Network

```python
class Network:
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

This chunk of code defines a class `Network` that is used for handling network communication in the Battleship game. It includes methods for sending and receiving data between players, setting up connections as a server or a client, and handling communication over sockets. The class also initializes attributes such as `is_server`, `sock`, and `conn` for managing the network state. The `BUFSIZE` constant is set to 16 for defining the buffer size for data transmission.

### Function: recv

```python
def recv(self):
    try:
        if self.is_server:
            return self._server_recv()
        return self._client_recv()
    except Exception:
        self.close()
```

This function is responsible for receiving data from either the server or the client based on the value of `is_server` attribute. It first checks if the instance is acting as a server, then calls `_server_recv()` function, otherwise calls `_client_recv()` function. If an exception occurs during the process, it closes the connection using the `close()` method.

### Function: close

```python
def close(self):
    self.sock.close()
    if self.conn:
        self.conn.close()
```

The `close` function closes the socket connection and checks if there is a connection object (`conn`) available before closing it.

### Special Method: __enter__

```python
def __enter__(self):
    # enables context manager
    return self
```

This special method `__enter__` enables the object to act as a context manager.

### Special Method: __exit__

```python
def __exit__(self, exc_type, exc_val, exc_tb):
    # enables context manager
    self.close()
```

The special method `__exit__` is used to handle the exiting of a context manager. It ensures that the connection is closed when exiting the context.

### pre_process_string

The `pre_process_string` function takes a string as input, converts it to lowercase, and filters out unwanted characters. It uses a helper function `wanted` which checks if the character is alphanumeric or a hyphen or falls within the range of "a" to "k". It then encodes the string into ASCII, ignores any errors, and decodes back to ASCII while translating the string based on the `ascii_code_point_filter`. The processed string is returned.

### parse_shot

The `parse_shot` function preprocesses the input string using the `pre_process_string` function, converts it to lowercase, removes spaces, and checks if the length of the string is at least 2. It then converts the characters into numbers between 0 and 9, handling errors for invalid input strings and out of bounds coordinates. Finally, it returns the converted x and y coordinates.

### ask_player_for_shot

The `ask_player_for_shot` function continuously prompts the user to input a shot in the format XY (e.g., A4). It calls the `parse_shot` function to process the input and returns the converted coordinates if successful. It handles errors by catching exceptions and retrying until a valid shot is provided.

### ask_player_for_shot

```python
def ask_player_for_shot():
    while 1:
        try:
            return parse_shot(input("Shoot (Format XY, e.g. A4): "))
        except Error:
            pass
```

This function prompts the player to input a shot in the format XY (e.g., A4) and then tries to parse the shot input. It keeps asking the player for a valid shot until a valid shot is entered.

### ask_player_for_ship

```python
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
            print_err("Invalid Format: ", str(e))

```

This function asks the player to place a ship on the board by specifying the ship's starting and ending positions in the format XX - YY (e.g., A1-A5). It then validates the ship's position, checking for diagonal placement, out-of-bounds coordinates, and ensuring the ship's length matches the specified ship type. The function continues to prompt the player until a valid ship placement is entered.

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

This function is responsible for placing a ship on the game board. It takes the start and end coordinates of the ship, along with the game board. It checks if the ship is not diagonal and has more than one square. Then it iterates over the squares between the start and end coordinates, checking if the squares are already occupied. If not, it places the ship on the board.

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

This function is responsible for placing all the ships on the game board. It iterates over the player's ships, asks the player for ship coordinates, and then calls the `place_ship` function to place the ship on the board. If there is an error, it prints the error message.


#Battleship.md


