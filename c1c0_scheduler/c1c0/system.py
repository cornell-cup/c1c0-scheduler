# Original by Angela Zou and Sujith Naapa Ramesh
# Edits by Christopher De Jesus
# Used to be multithreading/multserver.py
# For details, see Github repo history

import subprocess
import os
from typing import MutableMapping, Tuple, Mapping, List

import serial
from xbox360controller import Xbox360Controller

from c1c0_movement.Locomotion import R2Protocol2 as r2p

from ..system import System, Worker
from ..utils import ReaderWriterSuite


# JETSON = True
JETSON = False


class C1C0System(System):

    class SerialReader(Worker):

        def __init__(self, port, baudrate, data_id, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.data_id = data_id
            self.ser_line = serial.Serial(port=port, baudrate=baudrate)
            self.ser_line.close()
            self.data = ''
            self.MAX_DATA_LEN = kwargs.get('MAX_DATA_LEN', 2**16)

        def run(self):
            super().run()
            self.ser_line.open()
            try:
                while not self.stop_event.is_set():
                    new_data = ''
                    s = self.ser_line.read(32)  # reads serial buf for terabee
                    # decodes serial message (see R2Protocol2.py)
                    mtype, msg, status = r2p.decode(s)
                    if status == 1:
                        for i in range(len(msg)):  # loop through data
                            if i % 2 == 0:
                                new_data += (str(msg[i]) + str(
                                    msg[i + 1]) + ",")
                        #  Only set data when checksum is set
                        self.data = new_data
            finally:
                self.ser_line.close()

    class XBoxControllerReader(Worker):
        kill_switch: bool

        def __init__(self, *args, **kwargs):
            super().__init__(*args, *kwargs)
            self.kill_switch = False

        def run(self):
            super().run()

            def on_button_pressed(button):
                print(f'Button {button.name} was pressed')
                self.kill_switch = True

            def on_button_released(button):
                print(f'Button {button.name} was released')
                self.kill_switch = False

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

    serial_lines: Mapping[str, Tuple[str, int]] = {
            # 'terabee1': ('/dev/ttyTHS1', 115200)
    }
    thread_list: List[Worker] = []
    data_threads: Mapping[str, Worker]
    controller_thread: XBoxControllerReader
    active_subsystems: MutableMapping[str, subprocess.Popen] = {}
    active_subsystems_lock_suite: ReaderWriterSuite = ReaderWriterSuite()

    def __init__(self, *args, **kwargs):
        if JETSON:
            self.data_threads = {
                data_id: self.SerialReader(port, baudrate, data_id)
                for data_id, (port, baudrate) in self.serial_lines.items()
            }
        else:
            class DummySerialData(Worker):
                def __init__(self, data_id, val):
                    super().__init__(*args, **kwargs)
                    self.data_id = data_id
                    self.data = val
                    from random import random
                    self.random = random

                def run(self) -> None:
                    import time
                    while not self.stop_event.is_set():
                        self.data += 1 if (int(self.random()*4) % 2) else -1
                        time.sleep(0.1)

            # Add dummy serial data
            self.data_threads = {
                'terabee1': DummySerialData('terabee1', 0),
                'terabee2': DummySerialData('terabee2', 0)
            }
        if JETSON:
            self.controller_thread = self.XBoxControllerReader()
        else:
            class DummyXboxData(Worker):
                def run(self) -> None:
                    pass
            self.controller_thread = DummyXboxData()
        self.thread_list.append(self.controller_thread)
        self.thread_list.extend(self.data_threads.values())

        def get_data(_, data_id, *__):
            # Note: Locking is not necessary here due to only one writer, worst
            #  case scenario is *just* late data, which wouldn't be solved
            #  by locking either.
            return self.data_threads[data_id].data

        def start_subsystem(caller, target, *_):
            with self.active_subsystems_lock_suite.writer():
                if target in self.active_subsystems:
                    self.active_subsystems[target].kill()
                path = os.path.join('.', 'c1c0_scheduler', 'c1c0',
                                    'shells', 'start.sh')
                print(path)
                print(os.getcwd())
                print(os.path.abspath(path))
                subsystem = subprocess.Popen([
                    path, target, caller
                ])

                self.active_subsystems[target] = subsystem
                return subsystem

        self.funcs = {
            'get_data': get_data,
            'start_subsystem': start_subsystem
        }

    def start(self, *args, **kwargs):
        # Start threads controlling sensor readings
        [t.start() for t in self.thread_list]

    def stop(self, *args, **kwargs):
        [t.stop() for t in self.thread_list]

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def get_workers(self):
        return self.thread_list

    def get_functionality(self):
        return self.funcs


