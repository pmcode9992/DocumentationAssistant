import logging
import socket
import struct
import subprocess as sp
from dataclasses import dataclass
from itertools import repeat

from color import Text, Background, Cursor

vertical_header = " |A|B|C|D|E|F|G|H|I|J| "
FIELDS = [
    EMPTY,
    OWN_SHIP,
    OWN_SHIP_HIT,
    ENEMY_SHIP_HIT,
    MISS,
    OWN_SHIP_ENEMY_SHIP_HIT,
] = (0, 1, 2, 3, 4, 5)
SHIP_TYPES = [BATTLESHIP, CRUISER, DESTROYER, SUBMARINE] = (
    5,
    4,
    3,
    2,
)  # supported ship types
SHIP_NAMES = {
    BATTLESHIP: "Battleship"
    CRUISER: "Cruiser",
    DESTROYER: "Destroyer",
    SUBMARINE: "Submarine",
}
PLAYER_SHIPS = [BATTLESHIP, SUBMARINE]  # change this according to your needs


class Error(ValueError):
    def __init__(self, *args):
        logging.error(str(self))
        super().__init__(*args)


def print_err(*args, **kwargs):
    print(Text.RED, *args, Cursor.FULL_RESET, **kwargs)


def coord_valid(c: int):
    return 0 <= c <= 9


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


def create_empty_board():

    return [10 * [0] for _ in repeat(0, 10)]


def update_player_board(shot, board):

    x = shot.x
    y = shot.y
    field = board[y][x]
    if field == OWN_SHIP:
        board[y][x] = OWN_SHIP_HIT
        return True
    return False


def update_enemy_board(shot, board):
    x = shot.x
    y = shot.y
    if shot.last_shot_hit:
        board[y][x] = ENEMY_SHIP_HIT
    else:
        board[y][x] = MISS


def player_lost(board):
    return not any(OWN_SHIP in set(x) for x in board)


@dataclass
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

    def recv(self):
        try:
            if self.is_server:
                return self._server_recv()
            return self._client_recv()
        except Exception:
            self.close()

    def close(self):
        self.sock.close()
        if self.conn:
            self.conn.close()

    def __enter__(self):
        # enables context manager
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # enables context manager
        self.close()


def pre_process_string(s):
    s = s.lower()

    def wanted(c):
        return c.isalnum() or c == "-" or ord(c) in range(ord("a"), ord("k"))

    ascii_characters = [chr(ordinal) for ordinal in range(128)]
    ascii_code_point_filter = [c if wanted(c) else None for c in ascii_characters]
    s = s.encode("ascii", errors="ignore").decode("ascii")
    return s.translate(ascii_code_point_filter)


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


def ask_player_for_shot():
    while 1:
        try:
            return parse_shot(input("Shoot (Format XY, e.g. A4): "))
        except Error:
            pass


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
