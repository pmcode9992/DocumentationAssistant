## BattleShip

The project is a Battleship game implementation in Python. It includes game logic for creating and updating game boards, handling player shots, placing ships, and managing network communication for multiplayer games. The technologies used are Python. The functionalities include playing Battleship against an opponent either locally or over a network.

     Battleship.py
     Battleship.md


#Battleship.py

### Function: update_game_board

```python
def update_game_board(board, row, col, value):
    """
    Update the game board with the given value at the specified row and column.
    
    Parameters:
    - board (list): The game board to update.
    - row (int): The row index to update.
    - col (int): The column index to update.
    - value (str): The value to place at the specified position.
    
    Returns:
    - None
    """
    board[row][col] = value
```

This function is responsible for updating the game board with a specified value at a given row and column index. It takes the game board as a list, the row and column indices, and the value to update the board with. The function then updates the board at the specified position with the provided value.

### Import

The code snippet includes imports for modules such as logging, socket, struct, subprocess, dataclasses, and itertools. These modules are used for handling logging, network communication, data structuring, subprocess execution, data class creation, and iteration utilities, respectively.

### Constants and Variables

- `vertical_header` is a string representing the header for the game board.
- `FIELDS` is a list of constants representing different states on the game board, such as empty, own ship, own ship hit, enemy ship hit, miss, and own ship hit by enemy ship.
- `SHIP_TYPES` is a list of supported ship types with their corresponding lengths (battleship, cruiser, destroyer, submarine).
- `SHIP_NAMES` is a dictionary mapping ship types to their names.
- `PLAYER_SHIPS` is a list of ship types assigned to the player (battleship and submarine by default). This can be modified based on player preferences.

### coord_valid

```python
def coord_valid(c: int):
    return 0 <= c <= 9
```

This function checks if a given coordinate `c` is valid within the range of 0 to 9. It returns `True` if the coordinate is valid, otherwise `False`.

### print_boards

```python
def print_boards(board, enemy_board):

    s = "      Your Board  \t\t       Enemy Board\n\r"
    s += vertical_header + "\t\t" + vertical_header + "\n\r"
    for i, rows in enumerate(zip(board, enemy_board)):
        for j, entries in enumerate(rows):
            s += f"{i}|"
            for entry in entries:
                if entry == EMPTY:
                    s += Background.BLACK
                    s += " "
                elif entry == OWN_SHIP:
                    s += Background.GREEN
                    s += " "
                elif entry == OWN_SHIP_HIT:
                    s += Background.GREEN
                    s += Text.RED
                    s += "X"
                elif entry == ENEMY_SHIP_HIT:
                    s += Background.RED
                    s += " "
                elif entry == MISS:
                    s += Background.YELLOW
                    s += " "

                s += Cursor.FULL_RESET
                s += "|"
            if not j:
                s += f"{i}\t\t"

        s += f"{i}\n\r"

    s += vertical_header + "\t\t" + vertical_header + "\n\r"
    # clear the screen on OSX and linux
    _ = sp.call("clear", shell=True)
    print(s)
    return
```

This function prints the game boards for the player and the enemy, representing ships, hits, and misses with specific characters and colors. It uses the `board` and `enemy_board` lists to generate the visual representation of the game state.

### create_empty_board

```python
def create_empty_board():
    return [10 * [0] for _ in repeat(0, 10)]
```

This function creates and returns an empty game board for the Battleship game. It initializes a 10x10 grid with all elements set to 0.

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

This function updates the player's game board based on the shot taken. It checks if the shot hits the player's own ship and updates the board accordingly.

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

This function updates the enemy's game board based on the shot taken. It marks the position on the board as either a hit on the enemy's ship or a miss.

### player_lost

```python
def player_lost(board):
    return not any(OWN_SHIP in set(x) for x in board)
```

This function checks if the player has lost the game by checking if there are no more own ships left on the player's board.

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

The `Shot` class represents a shot in the Battleship game. It has attributes `x` and `y` to store the coordinates of the shot, and `last_shot_hit` to indicate if the last shot was a hit. The `__bytes__` method converts the shot object into bytes by packing `x`, `y`, and `last_shot_hit` into a byte stream. If `x` or `y` is too large to fit into 4 bits, an error is raised. The `decode` method decodes a byte stream into a `Shot` object by unpacking the coordinates and hit information.

### Network

```
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
```

This is a class named `Network` that handles network communication for the Battleship game. It has attributes like `is_server`, `sock`, and `conn` to manage the server-client connection. The `__init__` method initializes the network settings based on whether the instance is a server or a client. If it's a server, it creates a socket, binds it to the host and port, and starts listening for connections. If it's a client, it connects to a remote host.

---

```
    def _server_send(self, pkt):
        self.conn.sendall(pkt)

    def _client_send(self, pkt):
        self.sock.send(pkt)

    def send(self, pkt):
        if self.is_server:
            return self._server_send(pkt)
        return self._client_send(pkt)
```

These methods `_server_send`, `_client_send`, and `send` handle sending packets over the network. Depending on whether the instance is a server or a client, the appropriate method is called to send the packet.

---

```
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

These methods `_server_recv` and `_client_recv` handle receiving data from the network. For the server, it waits for a connection and then receives data in chunks of `BUFSIZE`. For the client, it directly receives data in chunks of `BUFSIZE`.

### Code Chunk Explanation

```python
logging.debug("Waiting for Data")
while True:
    data = self.conn.recv(self.BUFSIZE)
    if not data:
        break
    return data
```

This code snippet is responsible for waiting to receive data from the connection (`self.conn`) in a loop. It continuously receives data until no more data is available and then returns the received data.

### Code Chunk Explanation

```python
def _client_recv(self):
    data = self.sock.recv(self.BUFSIZE)
    return data
```

This function `_client_recv` is defined to receive data from the socket (`self.sock`) and return the received data.

### Code Chunk Explanation

```python
def recv(self):
    try:
        if self.is_server:
            return self._server_recv()
        return self._client_recv()
    except Exception:
        self.close()
```

The `recv` function is defined to handle receiving data based on whether the instance is a server or a client. It calls the appropriate receive function (`_server_recv` or `_client_recv`) based on the `is_server` attribute. If an exception occurs during receiving, it closes the connection.

### Code Chunk Explanation

```python
def close(self):
    self.sock.close()
    if self.conn:
        self.conn.close()
```

The `close` method is defined to close the socket connection (`self.sock`) and if there is a connection (`self.conn`), it also closes the connection.

### Code Chunk Explanation

```python
def __enter__(self):
    # enables context manager
    return self
```

This special method `__enter__` is defined to enable the use of this class as a context manager.

### Code Chunk Explanation

```python
def __exit__(self, exc_type, exc_val, exc_tb):
    # enables context manager
    self.close()
```

This special method `__exit__` is defined to handle the context manager exit, ensuring that the connection is closed properly.

### Function - pre_process_string

```python
def pre_process_string(s):
    s = s.lower()

    def wanted(c):
        return c.isalnum() or c == "-" or ord(c) in range(ord("a"), ord("k"))

    ascii_characters = [chr(ordinal) for ordinal in range(128)]
    ascii_code_point_filter = [c if wanted(c) else None for c in ascii_characters]
    s = s.encode("ascii", errors="ignore").decode("ascii")
    return s.translate(ascii_code_point_filter)
```

This function `pre_process_string` is used to process a string by converting it to lowercase, filtering out unwanted characters, and translating it based on ASCII values. The input string `s` is first converted to lowercase, then a helper function `wanted` is defined to filter out alphanumeric characters, hyphens, and characters falling within the ASCII range from 'a' to 'j'. It then generates a list of ASCII characters and applies the filter to keep only the desired characters. The input string `s` is encoded to ASCII, errors are ignored, and then decoded back to ASCII, filtering the characters based on the generated translation table. The processed string is returned.

### Function - parse_shot

```python
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

The `parse_shot` function takes an input string `s` representing a shot location in a Battleship game. It first preprocesses the string by converting it to lowercase, removing spaces, and ensuring it has at least two characters. It then processes the input coordinates by converting the first character to a number between 0 and 9 and the second character to an integer. If the conversion fails, an error is raised. It then checks if the converted x and y coordinates are within bounds using a helper function `coord_valid`. Finally, it returns the processed x and y coordinates.

### Function - ask_player_for_shot

```python
def ask_player_for_shot():
    while 1:
        try:
            return parse_shot(input("Shoot (Format XY, e.g. A4): "))
        except Error:
            pass
```

The function `ask_player_for_shot` continuously prompts the player to input a shot location in the format XY (e.g., A4) until a valid input is provided. It calls the `parse_shot` function with the user input and handles any errors that may occur during the parsing process.

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

This function prompts the player to input the coordinates for placing a ship on the game board. It validates the input format, checks if the ship is within bounds, and verifies the ship's length. If any errors occur during the input or validation process, appropriate error messages are displayed.

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

This function takes two points `a` and `b` representing the start and end locations of a ship, and the game `board` where the ship is to be placed. It validates if the ship is placed correctly (not diagonal and has more than one square) and then iterates over the squares to place the ship on the board.

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

This function iterates over each ship of the player, prints the game boards, and asks the player for ship placement coordinates. It then calls the `place_ship` function to place the ship on the board, handling any errors that may occur during the process.


#Battleship.md


