import time

from scheduler import config # Configurations

from typing import Optional # Type Hinting

class Message:
    """
    A message class for formatting and decoding messages.
    """

    def __init__(self: any, name: str, tag: str, data: str) -> 'Message':
        """
        Initializes a message instance with the given name, tag, and data.

        @param name: A string representing the name of the message.
        @param tag:  A string representing the tag of the message.
        @param data: A string representing the data of the message.
        @return: A Message instance with fields set as specified.
        """

        # Initializing fields
        self.name: str = name
        self.tag: str  = tag
        self.data: str = data

    def __str__(self: any) -> str:
        """
        Returns a string representation of the message.

        @return: A string representing the message.
        """

        # Returning string representation of message
        return f'{self.name}{config.TAG_SEP}{self.tag}{config.DATA_SEP}{self.data}'

    def __eq__(self: any, other: any) -> bool:
        """
        Compares two messages for equality.

        @param other: Another Message instance to compare to.
        @return: Whether or not the two messages are equal.
        """

        # Comparing message fields
        return (self.name == other.name and self.tag == other.tag and self.data == other.data)

    def show(self: any) -> bool:
        """
        Returns whether or not the message should be shown.

        @return: Whether or not the message should be shown.
        """

        return self.data != 'null' and self.data != ''

    @staticmethod
    def encode(self: any, msg: 'Message') -> str:
        """
        Encodes a message into a string.

        @param msg: A Message instance representing the message to be encoded.
        @return: A string representing the message.
        """

        # Encoding message
        return f'{msg.name}{config.TAG_SEP}{msg.tag}{config.DATA_SEP}{msg.data}'

    @classmethod
    def decode(self: any, string: str) -> 'Message':
        """
        Decodes a message from the given string.

        @param message: A string representing the message to be decoded.
        @return: A Message instance with fields set as specified.
        """

        # Splitting message into name, tag, and data
        str_split = string.split(config.DATA_SEP)
        meta, data = str_split[0], config.DATA_SEP.join(str_split[1:])
        name, tag = meta.split(config.TAG_SEP)

        # Returning message instance
        return Message(name, tag, data)

class DataQueue:
    """
    A queue for storing data to be processed by the server.
    """

    def __init__(self: any) -> 'DataQueue':
        """
        Initializes a data queue instance.

        @return: A DataQueue instance with fields set as specified.
        """

        # Initializing fields
        self.queue = []

    def add(self: any, message: Message) -> None:
        """
        Adds a message to the queue with the given name, tag, and data.

        @param message: A Message instance representing the message to be added.
        """

        # Adding message to queue
        print(str(message))
        self.queue.append((message, time.time()))

    def find(self: any, name: str, tag: str) -> Optional[Message]:
        """
        Finds a message in the queue with the given name and tag.

        @param name: A string representing the name of the message.
        @param tag:  A string representing the tag of the message.
        @return: The message, if found.
        """

        # Finding message in queue
        for message, timestamp in self.queue:
            if (time.time() - timestamp > config.TIMEOUT):
                self.queue.remove((message, timestamp))
                continue

            if (message.name == name and message.tag == tag):
                self.queue.remove((message, timestamp))
                return message

        # Returning none if message not found
        return None

def printc(msg: str, color: str) -> None:
    """
    Prints a message with the given color.

    @param msg: A string representing the message to be printed.
    @param color: A string representing the color to print the message in.
    """

    # Printing message with color
    print(f'{color}{msg}{config.END_COLOR}')
