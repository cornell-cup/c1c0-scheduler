import tkinter as tk
import time
import threading

from c1c0_scheduler.server import Subsystem

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Sequence, Mapping

# Based on https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes

# Built with experience with javax.swing/JFrame framework

class SubsystemStatusText(tk.Label):
    @staticmethod
    def format_text(subsystem: 'Subsystem'):
        return f'{subsystem.name}: {"Connected" if subsystem.connected else "Disconnected"}'

    def __init__(self, parent, subsystem: 'Subsystem', *args, **kwargs):
        self.var = tk.StringVar(value=self.format_text(subsystem))
        super().__init__(parent, textvariable=self.var, *args, **kwargs)
        self.parent = parent
        self.subsystem = subsystem

        self.update_thread = threading.Thread(target=self.update, daemon=True)
        self.update_thread.start()

    def update(self):
        while True:
            self.var.set(self.format_text(self.subsystem))
            self.update_idletasks()
            time.sleep(2)

class SystemStatusFrame(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: tk.Tk, subsystems: 'Sequence[Subsystem]', *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = tk.Label(self, text='Subsystem Statuses')

        self.columnconfigure(0, weight=1)
        # Configure rows of systems

        self.subsystem_statuses: 'Mapping[str, tk.Text]' = {
            SubsystemStatusText(self, subsystem) for subsystem in subsystems
        }
        for i, status in enumerate(self.subsystem_statuses):
            self.rowconfigure(i, weight=1)
            status.grid(row=i, column=0)

        
class WidgetsFrame(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: tk.Tk, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.quit = tk.Button(self, text='Close', command=controller.destroy)
        self.quit.grid(row=0, column=0)



class Window(tk.Tk):

    def __init__(self, name, subsystems, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm_title(name)
        self.attributes('-fullscreen', True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky='nsew')

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        self.sys_status_frame = SystemStatusFrame(container, self, subsystems)
        self.sys_status_frame.grid(row=0, column=0, sticky='nsew')

        self.widgets_frame = WidgetsFrame(container, self)
        self.widgets_frame.grid(row=0, column=1, sticky='nsew')





