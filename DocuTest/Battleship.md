## Battleship


The project "DocuTest" is a battleship game that allows players to compete over a network. It uses modules such as logging, socket, struct, subprocess, dataclasses, and itertools to enable networking and logging of information. The code defines constants for different field and ship types and names. The project also includes documentation files such as splits.md and summaries.md.

     splits.md
     summaries.md
     Battleship.py
     Battleship.md


#splits.md


#summaries.md


#Battleship.py

 represent the names of the ships when displaying them on the game board. The player ships are used to store the information about the player's ships, such as their coordinates and their current state.

]

### Imports 

This chunk of code imports necessary modules for playing a game of battleship with another player on the same network. This includes the logging, socket, struct, subprocess, dataclasses, and itertools modules. These modules are used for logging information about the program, networking, converting data into bytes, running shell commands, creating data structures, and creating an infinite iterator. 

### Constants 

This chunk of code defines constants for the game, including field types, ship types, ship names, and player ships. These constants are used to represent different states of a field on the game board, different types of ships, the names of the ships, and information about the player's ships.





### Import logging

Logging is a built-in Python module that allows for recording and tracking of events that occur during a program's execution. This can be useful for debugging and troubleshooting purposes. In this case, we are importing the logging module to be able to log events related to our Battleship game.

### Import socket
### Import struct
### Import subprocess as sp
### From dataclasses import dataclass
### From itertools import repeat

These imports are necessary for various features of our Battleship game. The socket and struct modules are commonly used for network programming, which may be used in our game for multiplayer functionality. The subprocess module, imported as sp, can be used for creating and managing subprocesses, which can be helpful for managing multiple processes in our game. The dataclass and repeat imports are used for creating and manipulating data structures, which may be used for storing and managing game data.

### Vertical_header = " |A|B|C|D|E|F|G|H|I|J| "

This line of code creates a string variable that contains the headers for the game board. This will be used to label the columns of the game board for easier reference.

### Fields = [
    EMPTY,
    OWN_SHIP,
    OWN

 s


### Class Error(ValueError)

This class handles any errors that may occur during the execution of the code. It inherits from the built-in ValueError class and overrides the __init__ method to log the error and pass the arguments to the parent class. This allows for easier debugging and error handling in the code.

### Function print_err(*args, **kwargs)

This function takes in a variable number of arguments and keyword arguments and prints them in red text. It uses the predefined constants from the Text and Cursor classes to format the output. This function can be used to print out error messages or any other important information in a visually appealing way.

### Function coord_valid(c: int)

This function takes in an integer as an argument and checks if it falls within the range of 0 to 9. It returns a boolean value indicating whether the coordinate is valid or not. This function can be used to validate user input for coordinate values in a game or any other application.

### Function print_boards(board, enemy_board)

This function takes in two lists, representing the player's and enemy's boards in a game. It then formats and prints out both boards side by side, with the player's board on the left and the enemy's board on the right. It uses predefined


class Shot:
    x: int
    y: int 


### Function: create_empty_board()

This function creates an empty game board for the game of battleship. It returns an array of size 10x10 with all values initialized to 0. This will be used as the player's board to keep track of their own ships and shots.

### Function: update_player_board(shot, board)

This function takes in a shot and the player's game board as parameters. It then checks the coordinates of the shot and updates the corresponding field on the board. If the shot hits one of the player's own ships, the field is updated to indicate a hit. Otherwise, the field remains unchanged. This function returns a boolean value, True if the shot was a hit and False otherwise.

### Function: update_enemy_board(shot, board)

This function is similar to the update_player_board function, except it updates the enemy's game board. If the shot was a hit, the corresponding field on the enemy's board is updated to indicate a hit. Otherwise, it is updated to indicate a miss. This function does not return anything.

### Function: player_lost(board)

This function checks the player's game board to see if all their own ships have been



### Shot

The Shot class represents a shot fired in a game. It has attributes for the x and y coordinates of the shot, as well as a boolean flag for whether or not the shot hit its target. The class also has methods for converting an instance of Shot into a byte representation, and for decoding a byte packet into a Shot object. The byte representation is created using the struct library, which allows for efficient packing and unpacking of data. The encode and decode methods ensure that the x and y coordinates are within the range of 0 to 15, which can be represented using 4 bits. If either coordinate is larger than 15, an Error will be raised. The encode method also sets the most significant bit of the byte to represent the value of the last_shot_hit attribute. The decode method unpacks the byte and creates a new Shot object with the appropriate x, y, and last_shot_hit values.



    def receive(self):
        if self.is_server:
            return self._server_recv()
        return self._client_recv()

]

### Network

The Network class is responsible for handling network connections. It has two main functions: sending and receiving data. The class also includes a BUFSIZE variable that specifies the size of the data buffer. In the constructor, the class initializes the socket and connection variables based on whether it is acting as a server or a client. If it is a server, it creates a new socket and binds it to the specified host and port, then starts listening for connections. If it is a client, it simply connects to the specified host and port.

The class also includes two private functions: _server_send and _client_send, which handle sending data to either the server or the client. The send function checks whether the instance is acting as a server or a client, and calls the appropriate private function. Similarly, the class also includes two private functions for receiving data: _server_recv and _client_recv. The receive function again checks whether the instance is acting as a server or a client, and calls the appropriate private function.

The server-side functions also include some additional code for handling connections. The _server_recv function checks if there is a



### Logging.debug

The logging.debug function in this code snippet is used to output a debug message to the console. This is useful for troubleshooting and identifying potential issues in the code. In this case, the message being output is "Waiting for Data". This suggests that the code is waiting for data to be received from the connection. 

### While True 

The while True loop in this code snippet is a common way to create an infinite loop. In this case, it is used to continuously run the code until a break statement is encountered. This is often used for listening for incoming data or continuously performing a task.

### Self.conn.recv

The self.conn.recv function is used to receive data from a connection. It takes in one argument, which is the maximum amount of data to be received at a time. In this case, the BUFSIZE variable is used to specify the maximum size of the data to be received. 

### Not data 

The "not data" statement in this code snippet is used to check if the data received is empty. If it is, the while loop will be terminated. This is a common way to handle the end of a data stream. 

### Return data 

The return statement in this code snippet is used to return the received data.



### pre_process_string

This function takes in a string and performs preprocessing on it by converting it to lowercase and removing any non-alphanumeric characters except for the hyphen and characters within the range of "a" to "k". The resulting string is then encoded into ASCII, ignoring any errors, and then decoded back into a string. The purpose of this function is to prepare the string for further processing, such as searching for specific characters or words. 

### parse_shot

This function takes in a string representing a coordinate in the form of a letter and number (e.g. A4) and converts it into two integers that represent the X and Y coordinates respectively. The string is first preprocessed using the pre_process_string() function and then converted into numbers between 0 and 9. If the string is not in the correct format, an Error is raised. The function also checks if the coordinates are within the valid range and raises an Error if they are not. 

### ask_player_for_shot

This function continuously prompts the user for a coordinate input and uses the parse_shot() function to convert it into usable coordinates. If the input is not in the correct format, the function will continue to prompt the user until a valid input is provided.



### ask_player_for_shot()

The `ask_player_for_shot()` function prompts the player to enter a shot in the format of XY, such as A4. The function then tries to parse the shot and return it. If there is an error, it will continue to ask the player until a valid shot is entered.


### ask_player_for_ship(ship_type)

The `ask_player_for_ship` function prompts the player to enter the coordinates for placing a ship of a specified type. It uses the `SHIP_NAMES` dictionary to display the ship type and length in the prompt. The user must enter the coordinates in the format of XX - YY (e.g. A1-A5). The function then tries to parse the coordinates and validate the ship placement. If the ship placement is not valid, the function will continue to ask the player until a valid placement is entered. 


### place_ship(a, b, board)

    This function takes in two coordinates and a board as arguments. It then checks if the two coordinates are either horizontal or vertical, and throws an error if they are diagonal. It also checks that the ship has more than one square. Then it iterates over the squares between the two coordinates and checks if they are already occupied. If not, it places the ship on the board. Finally, it returns the updated board.

### place_ships(board, enemy_board)

    This function takes in two boards as arguments and iterates through the player's ships. It prompts the player for coordinates and calls place_ship() to place the ship on the board. If there is an error, it prints the error message. This process continues until all ships are placed on the board. 


#Battleship.md


