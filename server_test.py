import time
import threading

from c1c0_scheduler.server import Subsystem, HierarchicalControlSystem, default_read
from c1c0_scheduler.client import Client
from c1c0_scheduler.config import SUBSYSTEMS
from c1c0_scheduler.display import Window

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Mapping

disp = True

def delayed_start(subsystem: 'Subsystem', delay):
    time.sleep(delay)
    print(f'delayed starting: {subsystem.name}')
    subsystem.start()

def chatbot_prot(subsystem: 'HierarchicalControlSystem', delay=0.1):
    time.sleep(0.1)
    


if __name__ == '__main__':
    with Subsystem.ctx():
        # Created facial client
        # xbox_controller = HierarchalControlSystem('xbox-controller', 0, timeout=0.0)
        # chatbot = HierarchalControlSystem('chatbot', 1)

        facial_system = Subsystem('facial-recognition', default_read)
        obj_det_system = Subsystem('object-detection', default_read)
        path_planning_system = Subsystem('path-planning', default_read)

        # chatbot = HierarchicalControlSystem('chatbot', group=0, timeout=1.0)
        # xbox_controller = HierarchalControlSystem('xbox-controller', group=1, timeout=0.0)

        facial_system.start()
        obj_det_system.start()
        # path_planning_system.start()
        t = threading.Thread(target=delayed_start, args=(path_planning_system,5.), daemon=True)
        t.start()

        if disp:
            window = Window('C1C0 Main View', (facial_system, obj_det_system, path_planning_system))
            window.mainloop()
        else:
            while True: 
                time.sleep(10)
                print('10s passed.')
                print(f'Facial Detection: {facial_system.connected}')
                print(f'Object Detection: {obj_det_system.connected}')
                print(f'Path Planning: {path_planning_system.connected}')
