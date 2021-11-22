# Original by Angela Zou and Sujith Naapa Ramesh
# Edits by Christopher De Jesus
# Used to be multithreading/multserver.py
# For details, see Github repo history

import subprocess
import os
import threading
from typing import MutableMapping, Tuple, Mapping, List, Union

import serial
from xbox360controller import Xbox360Controller

from c1c0_movement.Locomotion import R2Protocol2 as r2p

from ..system import System, Worker, DataProvider
from ..utils import ReaderWriterSuite


DUMMY_VALUES = True
# DUMMY_VALUES = False


class C1C0System(System):

    class SerialReader(Worker, DataProvider):

        class DummySerialData(Worker, DataProvider):
            def __init__(self, data_id, val, *args, **kwargs):
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

        def __init__(self, port, baudrate, data_id, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.data_id = data_id
            self.ser_line = serial.Serial(port=port, baudrate=baudrate)
            self.ser_line.close()
            self.data = ''

        def run(self):
            super().run()
            self.ser_line.open()
            try:
                print('acquiring new_data lock')
                with self.new_data:
                    print('acquired new_data lock')
                    while not self.stop_event.is_set():
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

        class DummyXboxData(Worker):
            def run(self) -> None:
                pass

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
    data_threads: \
        Mapping[str, Union[SerialReader, SerialReader.DummySerialData]]
    controller_thread: \
        Union[XBoxControllerReader, XBoxControllerReader.DummyXboxData]
    active_subsystems: MutableMapping[str, subprocess.Popen] = {}
    active_subsystems_lock_suite: ReaderWriterSuite = ReaderWriterSuite()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if DUMMY_VALUES:
            # Add dummy serial data
            self.data_threads = {
                'terabee1': self.SerialReader.DummySerialData('terabee1', 0),
                'terabee2': self.SerialReader.DummySerialData('terabee2', 0)
            }
            self.controller_thread = self.XBoxControllerReader.DummyXboxData()
        else:
            self.data_threads = {
                data_id: self.SerialReader(port, baudrate, data_id)
                for data_id, (port, baudrate) in self.serial_lines.items()
            }
            self.controller_thread = self.XBoxControllerReader()
        self.thread_list.append(self.controller_thread)
        self.thread_list.extend(self.data_threads.values())

        def get_data(_, data_id, *__):
            # Note: Locking is not necessary here due to only one writer, worst
            #  case scenario is *just* late data, which wouldn't be solved
            #  by locking either.
            return self.data_threads[data_id]

        def start_subsystem(caller, target, *_):
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
