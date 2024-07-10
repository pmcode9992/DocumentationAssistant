## Battleship


The project "DocuTest" is a Python program that implements the classic game of Battleship. It uses various technologies such as logging, sockets, and dataclasses. The program allows for two players to connect over a network and play against each other. The game features a graphical user interface that displays both the player's own board and the enemy's board. It also allows players to place their ships on the board and take turns guessing the location of the opponent's ships. The program includes error handling and input validation to ensure smooth gameplay. 

     Battleship.py


#Battleship.py



    ### Class - Person

    class Person {
        constructor(name, age) {
            this.name = name;
            this.age = age;
        }

        greet() {
            console.log(`Hello, my name is ${this.name}. I am ${this.age} years old.`);
        }
    }

    The next chunk of code is a class definition for a Person. This class contains a constructor function that takes in two parameters: name and age. These parameters are used to set the name and age properties of the Person object. The class also has a greet method, which uses string interpolation to print out a greeting message that includes the name and age of the Person. This class can be used to create Person objects with specific names and ages, and the greet method can be called on these objects to print out a personalized greeting.





### import logging

Logging is a useful tool for displaying information about the execution of a program, especially during debugging. This import statement allows us to use the logging module in our code.

### import socket

The socket module provides a low-level interface for network communication. It allows us to create and use sockets to establish connections with other devices on a network.

### import struct

The struct module is used for converting between Python values and C structs. It helps with packing and unpacking data to send and receive over a network.

### import subprocess as sp

The subprocess module allows us to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. By importing it as sp, we can use a shorter name for the module in our code.

### from dataclasses import dataclass

The dataclass decorator allows us to quickly create classes with pre-defined attributes and methods. It simplifies the process of creating data structures and reduces the amount of boilerplate code needed.

### from itertools import repeat

The itertools module provides various tools for efficient looping. The repeat function allows us to create an iterator that returns the same value indefinitely. This can be useful in certain scenarios, such as creating a grid for a battleship game.

### vertical_header = "




class Shot:

    x: int
    y: int

### create_empty_board()

This function creates an empty game board by returning a nested list with 10 rows and 10 columns, each filled with 0s.

### update_player_board(shot, board)

This function takes in a shot and a game board as parameters and updates the player's board based on the shot's coordinates. If the shot hits the player's own ship, the corresponding field on the board is changed to indicate a hit. Otherwise, the function returns False. 

### update_enemy_board(shot, board)

Similarly, this function updates the enemy's board based on the shot's coordinates. If the shot was a hit, the corresponding field on the board is changed to indicate a hit, otherwise it is marked as a miss.

### player_lost(board)

This function checks if the player has lost the game by checking if any of their own ships (represented by the constant OWN_SHIP) are still present on the board. If there are no OWN_SHIP fields left, the function returns True, indicating that the player has lost.

### Shot class

This is a dataclass that represents a shot made by a player. It stores the coordinates of the shot (x and y

 

### Class Shot

The Shot class represents a single shot fired in the game. It contains the x and y coordinates of the shot, as well as a boolean value indicating whether or not the shot hit its target. The class also has a method, __bytes__, which packs the shot's information into a byte string for transmission. Additionally, there is a static method, decode, which unpacks a byte string and returns a Shot object. 


]

### Network Class

The Network class is a class responsible for creating and maintaining a connection between two devices. It contains methods for sending and receiving data, as well as handling connections as a server or client.

The class has a class variable BUFSIZE with a value of 16, which determines the size of the buffer used for receiving data.

The constructor method, __init__, takes in the host and port as parameters and initializes the is_server attribute to determine if the device is acting as a server or client. It also creates a socket object and binds it to the host and port if the device is a server, or connects to a remote host if it is a client.

The _server_send and _client_send methods are used to send data to the connected device, depending on whether the device is acting as a server or client.

The send method is a wrapper method that calls either _server_send or _client_send depending on the is_server attribute.

The _server_recv and _client_recv methods are used to receive data from the connected device, again depending on the device's role. The _server_recv method first checks if a connection has already been established with a client, and if not, it waits for a connection to be made. Once a connection is



### logging.debug("Waiting for Data")

This code snippet uses the logging module to print a message indicating that the program is waiting for data. This is useful for troubleshooting and understanding the flow of the program. 

### while True:
            data = self.conn.recv(self.BUFSIZE)
            if not data:
                break
            return data

This snippet is a while loop that continuously receives data from a connection using the recv() method. The loop will continue indefinitely until the condition of no data being received is met, at which point the loop will break. The data is then returned to the caller. 

### def _client_recv(self):
        data = self.sock.recv(self.BUFSIZE)
        return data

This is a private function that is used to receive data from a socket. The _client_recv() function takes in the maximum buffer size as a parameter and returns the data received from the socket. 

### def recv(self):
        try:
            if self.is_server:
                return self._server_recv()
            return self._client_recv()
        except Exception:
            self.close()

This function checks whether the program is running as a server or a client and calls the appropriate receive function. If an exception is encountered, the close() function is called to close




### pre_process_string(s)

The `pre_process_string` function takes in a string and returns a processed version of it. First, it converts the string to lowercase using the `lower()` method. Then, it defines a `wanted` function which checks if a character is alphanumeric or a hyphen, or falls within the range of letters "a" through "k". This function is used to filter out unwanted characters from the string. 

Next, a list of all ASCII characters is created using a list comprehension. This list is then filtered using the `wanted` function to remove unwanted characters. Then, the string is encoded to ASCII and any errors are ignored. Finally, the `translate()` method is used to map the filtered list of ASCII characters to the corresponding characters in the string, effectively removing any unwanted characters.

### parse_shot(s)

The `parse_shot` function takes in a string representing a shot in a game and returns the coordinates of the shot. First, the string is processed by calling the `pre_process_string` function. Then, it is converted to lowercase and all spaces are removed using the `replace()` method. 

Next, the function checks if the length of the string is at least 2 characters. If not, an `Error




### def ask_player_for_shot():

This function prompts the player to shoot and returns the parsed shot input. It uses a while loop and a try-except block to continuously ask for valid input until the player enters a valid shot in the format of XY, such as A4. If an error is encountered, the function will continue to ask for input. 

### def ask_player_for_ship(ship_type):

This function prompts the player to place a ship of a given length and returns the coordinates of the ship. It uses a while loop and a try-except block to continuously ask for valid input until the player enters a valid format for placing the ship (XX-YY, such as A1-A5). The function then parses the input and validates the ship using various conditions such as checking for diagonal placement, out of bounds coordinates, and the correct length of the ship. If an error is encountered, the function will continue to ask for input. 




### place_ship(a, b, board)

This function takes in two coordinates and a game board, and places a ship on the board. It first checks if the coordinates are not diagonal (in a straight line), and then checks if the coordinates are not the same (as a ship must have more than one square). 

The function then iterates over the squares between the two coordinates, starting from the first coordinate and incrementing or decrementing the coordinates until it reaches the second coordinate. Each square is checked to see if it is already occupied, and if not, the square is marked as the player's ship. 

If the coordinates are successfully placed, the function returns. Otherwise, an error is raised and the player must try again. 

### place_ships(board, enemy_board)

This function iterates through all the ships in the PLAYER_SHIPS array and asks the player for coordinates to place each ship on their own board. The function also prints both the player's board and the enemy board (to give the player an idea of where the enemy ships might be). 

If the player successfully places a ship, the function breaks out of the loop and moves on to the next ship. If the player enters invalid coordinates, an error is raised and they must


