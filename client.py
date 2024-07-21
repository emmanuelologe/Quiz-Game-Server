import socket
import threading
import tkinter as tk
import json

client_socket = None
answer_submitted = False

# Function to connect to the server
def connect():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 9999))
    username = username_entry.get()
    client_socket.send(username.encode())
    threading.Thread(target=listen_for_messages).start()

# Function to listen for messages from the server
def listen_for_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(f"Received message: {message}")  # Debugging
        except ConnectionResetError:
            break
        if message == 'QUIZ_FINISHED':
            display_final_score()
        elif message.startswith('{') and message.endswith('}'):
            try:
                question = json.loads(message)
                if 'question' in question and 'options' in question:
                    update_question(question)
                # else:
                #     question_label.config(text="Received invalid question format")
            except json.JSONDecodeError:
                question_label.config(text="Error decoding question from server")
        else:
            score_label.config(text=message)

# Function to update the GUI with the new question
def update_question(question):
    question_label.config(text=question['question'])
    options = question['options']
    for i, option in enumerate(options):
        option_buttons[i].config(text=option)
    next_button.config(state=tk.DISABLED)  # Disable next button initially
    global answer_submitted
    answer_submitted = False  # Reset answer submission flag

# Function to submit an answer to the server
def submit_answer(answer):
    global answer_submitted
    if not answer_submitted:
        client_socket.send(f'SUBMIT_ANSWER {answer}'.encode())
        answer_submitted = True  # Set flag to indicate answer is submitted
        next_button.config(state=tk.NORMAL)  # Enable next button

# Function to move to the next question
def next_question():
    client_socket.send('NEXT_QUESTION'.encode())

# Function to request the score from the server
def get_score():
    client_socket.send('GET_SCORE'.encode())

# Function to display the final score when the quiz is finished
def display_final_score():
    client_socket.send('GET_SCORE'.encode())
    final_score = client_socket.recv(1024).decode()
    question_label.config(text="Quiz Finished!")
    for button in option_buttons:
        button.pack_forget()
    score_label.config(text=final_score)

# Function to set up the GUI
def setup_gui():
    root = tk.Tk()
    root.title("Multiplayer Quiz Game Client")

    global username_entry
    global question_label
    global option_buttons
    global score_label
    global next_button

    # Username input section
    username_label = tk.Label(root, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()
    connect_button = tk.Button(root, text="Connect", command=connect)
    connect_button.pack()

    # Question display section
    question_label = tk.Label(root, text="")
    question_label.pack()

    # Option buttons for answers
    option_buttons = []
    for i in range(4):
        button = tk.Button(root, text="", command=lambda i=i: submit_answer(option_buttons[i].cget("text")))
        button.pack()
        option_buttons.append(button)

    # "Next" button to move to the next question
    next_button = tk.Button(root, text="Next", state=tk.DISABLED, command=next_question)
    next_button.pack()

    # Score display section
    score_label = tk.Label(root, text="")
    score_label.pack()

    root.mainloop()

if __name__ == '__main__':
    setup_gui()