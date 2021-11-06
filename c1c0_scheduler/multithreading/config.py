from enum import Enum
from typing import Union, Mapping, Tuple, Optional, Iterable
import subprocess
import os


ENCODING = 'UTF-8'
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1233


def placeholder_fun(_, __, ___):
    pass


# Letter: (ProcessType, cmds_noargs, cmds_args)
class ProcessTypes(Enum):
    PATH_PLANNING = ('path-planning', {'get_data': placeholder_fun})
    OBJECT_DETECTION = ('object-detection', {'path': lambda _, __, ___: print('Old')})
    CHATBOT = ('chatbot', {'start': placeholder_fun})
    FACIAL_RECOGNITION = ('facial-recognition', {'run': placeholder_fun})


letter_process_map: Mapping[str, ProcessTypes] = {
    'P': ProcessTypes.PATH_PLANNING,
    'O': ProcessTypes.OBJECT_DETECTION,
    'C': ProcessTypes.CHATBOT,
    'F': ProcessTypes.FACIAL_RECOGNITION
}

# Inverting letter_process_map for convenience
process_letter_map: Mapping[ProcessTypes, str] = {
    process_data: letter for letter, process_data in letter_process_map.items()
}


PRIMARY_PROCESS = ProcessTypes.CHATBOT

PType = Union[str, ProcessTypes]


def extract_process_type(p_type: PType) -> ProcessTypes:
    # Attempt to cast process type regardless of whether it is a
    #  string or enum.
    try:
        return ProcessTypes[p_type]
    except KeyError:
        return ProcessTypes(p_type)


def cmd_digest(cmd: str) -> Tuple[Optional[str], Optional[str], Optional[str],
                                  Optional[str]]:
    def interp_args(s: str) -> Iterable:
        return map(lambda s_: s_.strip(), s.split(','))

    def dictify(s: str) -> Mapping:
        acc = {}
        next_start = s.index('(')
        while next_start != -1:
            pass
        return acc

    try:
        receiver = cmd[0]
        body = cmd[5:-1]
    except IndexError as e:
        # Although IndexError is more precise, this particular issue hints at
        #  a broader problem with the issued command.
        raise ValueError(e, f'Malformed command: `{cmd}`')
    # Should only need sender and receiver
    return sender, middle, receiver, body