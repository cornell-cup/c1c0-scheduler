import tkinter as tk
import time
from c1c0_scheduler.server import Subsystem, default_read


# Color Constants
PAGE_COLOR: str = '#D7F0FF'
NAVBAR_COLOR: str = '#7FB3D5'
TABLE_COLOR: str = '#2A3B4C'
TERMINAL_COLOR: str = '#1F1F1F'
TERMINAL_TEXT: str = '#F0F0F0'

# Size Constants
PAGE_RATIO: int = 0.925
NAVBAR_RATIO: int = 0.075
BUTTON_PADDING: int = 16

# Time Constants
DELAY_TIME: int = 500


class Window(tk.Tk):
    def __init__(self: 'Window', name: str, *args: tuple, **kwargs: dict) -> None:
        # Processing arguments
        super().__init__(*args, **kwargs)
        self.pages: dict = {}
        self.buttons: dict = {}

        # Setting window properties
        self.title(name)
        self.attributes('-fullscreen', True)

        # Creating container frames
        container_height = self.winfo_screenheight() * PAGE_RATIO
        navbar_height = self.winfo_screenheight() * NAVBAR_RATIO
        self.container: tk.Frame = tk.Frame(self, height = container_height, bg = PAGE_COLOR)
        self.navbar: tk.Frame = tk.Frame(self, height = navbar_height, bg = NAVBAR_COLOR)
        self.navbar.pack(side = 'top', fill = 'both', expand = True)
        self.container.pack(side = 'top', fill = 'x', expand = False)

    def add(self: 'Window', page: 'HomePage | SystemPage') -> None:
        # Placing page and button
        page.place(in_ = self.container, x = 0, y = 0, relwidth = 1, relheight = 1)
        button = tk.Button(self.navbar, text = page.name, padx = BUTTON_PADDING, pady = BUTTON_PADDING, command = page.lift)
        button.pack(side = 'left')

        # Recording page and button
        self.pages[page.name] = page
        self.buttons[page.name] = button

        # Raising page if it is the first page
        if (page is HomePage): page.lift()


class HomePage(tk.Frame):
    def __init__(self: 'HomePage', systems: list[Subsystem], *args: tuple, **kwargs: dict) -> None:
        # Processing arguments
        super().__init__(bg = PAGE_COLOR, *args, **kwargs)
        self.name: str = 'Home Page'
        self.systems: list[Subsystem] = systems

        # Creating status table
        self.status: Table = Table(self, len(systems), 3, 0.48, 0.885)
        self.status.place(in_ = self, relx = 0.01, rely = 0.02)

        # Creating statistics table
        self.statistic: Table = Table(self, 6, 2, 0.48, 0.885)
        self.statistic.place(in_ = self, relx = 0.51, rely = 0.02)

    def update(self: 'HomePage') -> None:
        for i, system in enumerate(self.systems):
            text: str = "Connected" if system.connected else "Disconnected"
            self.status.write(i, 0, text)

    def lift(self: 'HomePage') -> None:
        # Raising page and tables
        self.tkraise()
        self.status.tkraise()
        self.statistic.tkraise()


class Table(tk.Frame):
    def __init__(self: 'Table', parent: HomePage, wnum: int, hnum: int, width: float, height: float, *args: tuple, **kwargs: dict) -> None:
        # Processing arguments
        self.table_width: int = int(parent.winfo_screenwidth() * width)
        self.table_height: int = int(parent.winfo_screenheight() * height)
        super().__init__(bg = TABLE_COLOR, width = self.table_width, height = self.table_height, *args, **kwargs)


class SystemPage(tk.Frame):
    def __init__(self: 'SystemPage', name: str, system: Subsystem, *args: tuple, **kwargs: dict) -> None:
        # Processing arguments
        super().__init__(bg = PAGE_COLOR, *args, **kwargs)
        self.name = 'Subsystem: ' + name
        self.system: Subsystem = system

        # Creating from terminal
        from_system_name: str = 'From {0} To Scheduler:'.format(self.name[11:])
        self.from_system: Terminal = Terminal(self, from_system_name, 0.48, 0.885)
        self.from_system.place(in_ = self, relx = 0.01, rely = 0.02)

        # Creating to terminal
        to_system_name: str = 'From Scheduler To {0}:'.format(self.name[11:])
        self.to_system: Terminal = Terminal(self, to_system_name, 0.48, 0.885)
        self.to_system.place(in_ = self, relx = 0.51, rely = 0.02)

    def update(self: 'SystemPage') -> None:
        # Updating terminals
        self.from_system.write('From System Working ... {0}\n'.format(time.time()))
        self.to_system.write('To System Working ...{0}\n'.format(time.time()))

    def lift(self: 'SystemPage') -> None:
        # Raising page and terminals
        self.tkraise()
        self.from_system.tkraise()
        self.to_system.tkraise()


class Terminal(tk.Frame):
    def __init__(self: 'Terminal', parent: SystemPage, name: str, width: float, height: float, *args: tuple, **kwargs: dict) -> None:
        # Processing arguments
        self.terminal_width: int = int(parent.winfo_screenwidth() * width)
        self.terminal_height: int = int(parent.winfo_screenheight() * height)
        super().__init__(bg = TABLE_COLOR, borderwidth = 3, width = self.terminal_width, height = self.terminal_height, *args, **kwargs)

        # Creating label
        self.label: tk.Label = tk.Label(self, fg = TERMINAL_TEXT, bg = TABLE_COLOR, borderwidth = 3, text = name, font = ('Helvetica', 24))
        self.label.place(in_ = self, relx = 0.01, rely = 0.01)

        # Creating text
        self.text: tk.Text = tk.Text(self, fg = TERMINAL_TEXT, borderwidth = 3, wrap = 'word', font = ('Helvetica', 16))
        self.text.place(in_ = self, relx = 0.01, rely = 0.05, relwidth = 0.98, relheight = 0.94)

    def write(self: 'Terminal', text: str) -> None:
        # Writing text to terminal
        self.text.insert(tk.END, text)


if __name__ == '__main__':
    # Creating window
    window: Window = Window('C1C0 Status Viewer')

    # Creating subsystems
    facial_system: Subsystem = Subsystem('facial-recognition', default_read)
    object_system: Subsystem = Subsystem('object-detection', default_read)
    path_system: Subsystem = Subsystem('path-planning', default_read)

    # Starting subsystems
    #! facial_system.start()
    #! object_system.start()
    #! path_system.start()

    # Creating pages
    facial_recognition: SystemPage = SystemPage('Facial Recognition', facial_system)
    object_detection: SystemPage = SystemPage('Object Detection', object_system)
    path_planning: SystemPage = SystemPage('Path Planning', path_system)
    home_page: HomePage = HomePage((facial_system, object_system, path_system))

    # Adding pages to window
    window.add(home_page)
    window.add(facial_recognition)
    window.add(object_detection)
    window.add(path_planning)

    # Updating window
    def update() -> None:
        if (facial_recognition is not None): facial_recognition.update()
        if (object_detection is not None): object_detection.update()
        if (path_planning is not None): path_planning.update()
        window.after(DELAY_TIME, update)

    # Closing window
    def close() -> None:
        window.destroy()
        if (facial_system is not None): facial_system.stop()
        if (object_system is not None): object_system.stop()
        if (path_system is not None): path_system.stop()

    # Starting window
    window.after(DELAY_TIME, update)
    window.protocol('WM_DELETE_WINDOW', close)
    window.mainloop()
