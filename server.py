import socket
import threading
import json

def load_questions():
    # Load questions from a JSON file
    with open('questions.json', 'r') as file:
        return json.load(file)

questions = load_questions()
total_questions = len(questions)
scores = {}
clients = []

def handle_client(client_socket, addr):
    current_question_index = 0

    # Function to send a question to the client
    def send_question(socket):
        if current_question_index < total_questions:
            question = questions[current_question_index]
            print(f"Sending question: {question}")  # Debugging
            socket.send(json.dumps(question).encode())
        else:
            print("Quiz finished")  # Debugging
            socket.send('QUIZ_FINISHED'.encode())

    # Function to update and broadcast scores to all clients
    def update_scores():
        scores_message = json.dumps(scores)
        for client, _ in clients:
            client.send(scores_message.encode())

    # Receive and store the username from the client
    username = client_socket.recv(1024).decode()
    scores[username] = 0
    clients.append((client_socket, username))
    
    send_question(client_socket)

    # Main loop to handle client requests
    while True:
        try:
            request = client_socket.recv(1024).decode()
            print(f"Received request: {request}")  # Debugging
        except ConnectionResetError:
            break

        if request.startswith('SUBMIT_ANSWER'):
            _, answer = request.split(' ', 1)
            correct_answer = questions[current_question_index]['answer']
            if answer == correct_answer:
                scores[username] += 1
            current_question_index += 1
            send_question(client_socket)
            update_scores()
        elif request == 'NEXT_QUESTION':
            send_question(client_socket)
        elif request == 'GET_SCORE':
            final_score = f'Your score is {scores[username]} out of {total_questions}'
            client_socket.send(final_score.encode())
        else:
            client_socket.send('Invalid request'.encode())

    clients.remove((client_socket, username))
    client_socket.close()

def server():
    # Create a server socket and bind it to a port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(5)
    print('Server started on port 9999')

    while True:
        # Accept a client connection
        client_socket, addr = server_socket.accept()
        print(f'Accepted connection from {addr}')
        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == '__main__':
    server()