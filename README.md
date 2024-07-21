# Overview

This project is aimed at furthering my learning by developing a networking program that allows for a multiplayer quiz game. The software supports both client-server communication, enabling multiple users to connect and participate in a quiz simultaneously.

The client connects to the server, sends a username, receives quiz questions, submits answers, and finally displays the score. The server manages the quiz questions, tracks scores for each client, and communicates with multiple clients concurrently.

To use the software:

Start the server by running the server script.
Start each client by running the client script.
Enter a username on the client GUI to connect to the server and start the quiz.
The purpose of writing this software is to understand the intricacies of network communication, concurrency in server-client models, and GUI application development.


[Software Demo Video](http://youtube.link.goes.here)

# Network Communication

The architecture used in this project is a client-server model.

We are using TCP for reliable communication between the client and the server. The server listens on port 9999, and clients connect to this port to participate in the quiz.

Messages between the client and server are formatted as JSON objects.


        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Claude Monet", "Leonardo da Vinci", "Pablo Picasso"],
        "answer": "Leonardo da Vinci"


# Development Environment

The tools used to develop this software include:

Visual Studio Code (VS Code) for writing and debugging the code
Python as the programming language
Libraries used:

socket for network communication
threading for handling multiple client connections
json for message formatting
tkinter for the graphical user interface

# Useful Websites

* [Python Official Documentation](https://docs.python.org/3/)
* [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
* [Socket Programming in Python](https://realpython.com/python-sockets/)

# Future Work
* Enhance the GUI to provide a better user experience.
* Implement more robust error handling and user feedback mechanisms.
* Add a feature to track and display leaderboards.
* Implement the peer-to-peer model for the quiz game.