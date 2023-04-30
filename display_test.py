import time
import tkinter as tk
import tkinter.ttk as ttk
from c1c0_scheduler.server import Subsystem, default_read


# Color constants
PAGE_COLOR: str = '#D7F0FF'
NAVBAR_COLOR: str = '#7FB3D5'
TABLE_COLOR: str = '#2A3B4C'
TERMINAL_COLOR: str = '#1F1F1F'
TERMINAL_TEXT: str = '#F0F0F0'


# Size constants
PAGE_RATIO: int = 0.925
NAVBAR_RATIO: int = 0.075
BUTTON_PADDING: int = 16


# Status constants
DELAY_TIME: int = 100
TIME_RUNNING: int = 0
DATA_SENT: int = 0
DATA_RECEIVED: int = 0


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
        self.status: Table = Table(self, 8, 2, 0.885, 0.48)
        self.status.place(in_ = self, relx = 0.01, rely = 0.02)
        self.status.edit_head('c0', 'System')
        self.status.edit_head('c1', 'Status')

        # Creating statistics table
        self.statistic: Table = Table(self, 8, 2, 0.885, 0.48)
        self.statistic.place(in_ = self, relx = 0.51, rely = 0.02)
        self.statistic.edit_head('c0', 'Statistic')
        self.statistic.edit_head('c1', 'Value')

        # Updating table
        self.update()

    def update(self: 'HomePage') -> None:
        # Updating status table
        for i, system in enumerate(self.systems):
            status = 'Connected' if system.connected else 'Disconnected'
            name = system.name.replace('-', ' ').title() + ':'
            self.status.edit_row(i, [name, status])

        # Updating statistics table
        self.statistic.edit_row(0, ['Time Running:', str(TIME_RUNNING / 1000) + ' s'])
        self.statistic.edit_row(1, ['Data Sent:', str(DATA_SENT / 1000) + ' kb'])
        self.statistic.edit_row(2, ['Data Received:', str(DATA_RECEIVED / 1000) + ' kb'])

    def lift(self: 'HomePage') -> None:
        # Raising page and tables
        self.tkraise()
        self.status.tkraise()
        self.statistic.tkraise()


class Table(ttk.Treeview):
    def __init__(self: 'Table', parent: HomePage, hnum: int, wnum: int, height: float, width: float) -> None:
        # Processing arguments
        self.table_width = int(parent.winfo_screenwidth() * width)
        self.table_height = int(parent.winfo_screenheight() * height)
        self.cell_width = int(self.table_width / wnum)
        self.cell_height = int(self.table_height / (hnum + 1))

        # Creating columns and rows
        self.columns = ['c' + str(i) for i in range(wnum)]
        super().__init__(parent, column = self.columns, height = hnum, show = 'headings')
        for column in self.columns:
            self.heading(column, text = '', anchor = 'center')
            self.column(column, width = self.cell_width, anchor = 'center')
        for row in range(hnum):
            self.insert('', 'end', iid=str(row), values = [''] * wnum)

        # Styling table
        style = ttk.Style(parent)
        style.theme_use('clam')
        style.configure('Treeview', rowheight = self.cell_height, font = ('Helvetica', 16))
        style.configure('Treeview', background = TABLE_COLOR, foreground = 'white')
        style.configure('Treeview.Heading', rowheight = self.cell_height, font = ('Helvetica', 24))

    def edit_head(self: 'Table', column: str, text: str) -> None:
        # Editing heading
        self.heading(column, text = text)

    def edit_row(self: 'Table', row: int, text: list[str]) -> None:
        # Editing row
        self.item(str(row), values = text)


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
        if (TIME_RUNNING % 1000 == 0):
            from_str = 'From System Working ... {0}\n'.format(TIME_RUNNING)
            to_str = 'To System Working ... {0}\n'.format(TIME_RUNNING)
            self.from_system.write(from_str)
            self.to_system.write(to_str)

            global DATA_SENT, DATA_RECEIVED
            DATA_SENT += from_str.encode('utf-8').__len__()
            DATA_RECEIVED += to_str.encode('utf-8').__len__()

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
        global TIME_RUNNING, DELAY_TIME
        TIME_RUNNING += DELAY_TIME

        home_page.update()
        facial_recognition.update()
        object_detection.update()
        path_planning.update()

        window.after(DELAY_TIME, update)

    # Closing window
    def close() -> None:
        window.destroy()

        #! facial_system.stop()
        #! object_system.stop()
        #! path_system.stop()

    # Starting window
    window.after(DELAY_TIME, update)
    window.protocol('WM_DELETE_WINDOW', close)
    window.mainloop()
