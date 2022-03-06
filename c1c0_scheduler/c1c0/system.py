# Original by Angela Zou and Sujith Naapa Ramesh
# Edits by Christopher De Jesus
# Used to be multithreading/multserver.py
# For details, see Github repo history

import subprocess
import os
# import threading
from typing import MutableMapping, Tuple, Mapping, List, Union

import serial
from xbox360controller import Xbox360Controller

from c1c0_movement.Locomotion import R2Protocol2 as r2p

try:
    from ..system import System, Worker, DataProvider
    from ..utils import ReaderWriterSuite
except ImportError:
    from c1c0_scheduler.system import System, Worker, DataProvider
    from c1c0_scheduler.utils import ReaderWriterSuite

DUMMY_VALUES = True
# DUMMY_VALUES = False


class DummySerialData(Worker, DataProvider):
    """
    A debugger Worker subclass that mimics collecting data and making it
    publicly available for other processes.
    """
    def __init__(self, data_id, val, *args, **kwargs):
        """
        PARAMETERS
        ----------
        data_id
            The id for the data you are collecting.
        val
            The starting value for this fake data.
        """
        super().__init__(*args, **kwargs)
        self.data_id = data_id
        self.data = val
        from random import random
        self.random = random

    def run(self) -> None:
        import time
        while not self.stop_event.is_set():
            time.sleep(0.0001)
            with self.new_data:
                self.data += 1 if (int(self.random() * 4) % 2) else -1
                self.new_data.notify_all()


class DummyXboxData(Worker):
    """
    A debugger Worker subclass that mimics controller input.
    """
    def run(self) -> None:
        pass


class SerialReader(Worker, DataProvider):
    """
    A Worker subclass that collects data and makes it publicly available for
    other processes.
    """
    def __init__(self, port: str, baudrate: int, *args, **kwargs):
        """
        PARAMETERS
        ----------
        port
            The port string to form a serial connection to.
        baudrate
            The baudrate to read the serial connection at.
        data_id
            The id for the data you are collecting.
        """
        super().__init__(*args, **kwargs)
        self.ser_line = serial.Serial(port=port, baudrate=baudrate)
        self.ser_line.close()
        self.data = ''

    def run(self):
        super().run()
        self.ser_line.open()
        try:
            while not self.stop_event.is_set():
                with self.new_data:
                    new_data = ''
                    # reads serial buffer for terabee
                    s = self.ser_line.read(32)
                    # decodes serial message (see R2Protocol2.py)
                    mtype, msg, status = r2p.decode(s)
                    if status == 1:
                        for i in range(len(msg)):  # loop through data
                            if i % 2 == 0:
                                new_data += (str(msg[i]) + str(
                                    msg[i + 1]) + ",")
                        #  Only set data when checksum is set
                        self.data = new_data
                        self.new_data.notify_all()
        finally:
            self.ser_line.close()


class XBoxControllerReader(Worker):
    """
    A worker subclass that reads controller input.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

    def run(self):
        super().run()

        def on_button_pressed(button):
            print(f'Button {button.name} was pressed')
            self.stop_event.set()

        def on_button_released(button):
            print(f'Button {button.name} was released')
            self.stop_event.clear()

        def on_axis_moved(axis):
            # TODO send command to locomotion to control the head rotation
            print(f'Axis {axis.name} moved to {axis.x} {axis.y}')

        try:
            with Xbox360Controller(0, axis_threshold=0.2) as controller:
                # Button A events
                controller.button_a.when_pressed = on_button_pressed
                controller.button_a.when_released = on_button_released

                # Left and right axis move event
                controller.axis_l.when_moved = on_axis_moved
                controller.axis_r.when_moved = on_axis_moved

                self.stop_event.wait()
        except KeyboardInterrupt:
            pass


class C1C0System(System):

    serial_lines: Mapping[str, Tuple[str, int]] = {
            # 'terabee1': ('/dev/ttyTHS1', 115200)
    }
    """
    Serial lines to read from.
    """
    thread_list: List[Worker] = []
    """
    Primary list of threads acting as workers
    """
    data_threads: \
        Mapping[str, Union[SerialReader, DummySerialData]]
    """
    Sublist of threads acting as data collectors
    """
    controller_thread: \
        Union[XBoxControllerReader, DummyXboxData]
    """
    Sublist of threads acting as controller input readers.
    """
    active_subsystems: MutableMapping[str, subprocess.Popen] = {}
    """
    Currently active subsystems.
    """
    active_subsystems_lock_suite: ReaderWriterSuite = ReaderWriterSuite()
    """
    Lock suite to manage what systems read and write to active_systems.
    """

    def __init__(self, *args, **kwargs):
        super().__init__('C1C0_System', *args, **kwargs)
        print(self.data_worker_info)
        self.data_threads = {
            f'terabee{i}': SerialReader(port, baudrate)
            for i, (port, baudrate) in enumerate(self.data_worker_info)
        }
        if DUMMY_VALUES:
            # Add dummy serial data
            self.data_threads = {
                'terabee1': DummySerialData('terabee1', 0),
                'terabee2': DummySerialData('terabee2', 0)
            }
            self.controller_thread = DummyXboxData()
        else:
            self.data_threads = {
                data_id: SerialReader(port, baudrate, data_id)
                for data_id, (port, baudrate) in self.serial_lines.items()
            }
            self.controller_thread = XBoxControllerReader()
        self.thread_list.append(self.controller_thread)
        self.thread_list.extend(self.data_threads.values())

        def get_data(_, data_id, *__):
            """
            Server callable function, fulfilling the `funcs` specification of
            Callable[sender: str, receiver: str, data: str(?)]
            """
            # Note: Locking is not necessary here due to only one writer, worst
            #  case scenario is *just* late data, which wouldn't be solved
            #  by locking either.
            return self.data_threads[data_id]

        def start_subsystem(caller, target, *_):
            """
            Server callable function, fulfilling the `funcs` specification of
            Callable[sender: str, receiver: str, data: str(?)]
            """
            with self.active_subsystems_lock_suite.writer():
                if target in self.active_subsystems:
                    self.active_subsystems[target].kill()
                path = os.path.join('.', 'c1c0_scheduler', 'c1c0',
                                    'shells', 'start.sh')
                subsystem = subprocess.Popen([
                    path, target, caller
                ])

                self.active_subsystems[target] = subsystem
                return subsystem

        self.funcs = {
            'get_data': get_data,
            'start_subsystem': start_subsystem
        }
        print(f'Data threads: {self.data_threads}')

    def start(self, *args, **kwargs):
        """
        Start up all worker threads.
        """
        # Start threads controlling sensor readings
        [t.start() for t in self.thread_list]

    def stop(self, *args, **kwargs):
        """
        Stop all worker threads.
        """
        [t.stop() for t in self.thread_list]

    def __enter__(self):
        """
        Automatically calls `start`.
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Automatically calls `stop`.
        """
        self.stop()

    def get_workers(self):
        """
        Returns list of workers
        """
        return self.thread_list

    def get_functionality(self):
        """
        Returns dictionary of list of functions. All functions follow the
        parameter specification:

        sender - str
        receiver - str
        data - str (optional)
        """
        return self.funcs
