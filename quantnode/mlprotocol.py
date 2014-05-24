import string
import consts
from consts import BUFFER_SIZE
MSG_LENGTH_SIZE = 10


def create_message(msg):
    """
    Properly formats a message according to the "ML Protocol" (message-length protocol)
    for sending over a socket connection
    """
    msglength = string.zfill(len(msg), MSG_LENGTH_SIZE)
    return msglength + msg


def get_message(socket, buffer_size = BUFFER_SIZE):
    """
    Retrieves a message from the socket by iteratively receiving
    bytes until none are left
    """
    msglength = int(socket.recv(MSG_LENGTH_SIZE))
    counter = 0
    messages = []

    while True:
        tmp = socket.recv(buffer_size)
        messages.append(tmp)
        counter += len(tmp)
        if counter >= msglength:
            break

    message = ''.join(messages)
    return message


def stop_message():
    return create_message(consts.STOP_FLAG)


def continue_message():
    return create_message(consts.CONTINUE_FLAG)


def end_message():
    return create_message(consts.END_FLAG)

