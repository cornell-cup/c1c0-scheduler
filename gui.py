from tkinter import font as tkFont
import tkinter as tk
import subprocess
import signal
import os


global process
process = None


def run_command():
    global process
    if process is not None:
        print("A process is already running.")
        return

    process = subprocess.Popen(
        "cd ~/c1c0-main/c1c0-scheduler && make",
        shell=True, preexec_fn=os.setsid  # This starts the process in a new session (group)
    )


def stop_command():
    global process
    if process is None:
        print("No process is running.")
        return

    # Kill the whole process group, including all child processes
    os.killpg(process.pid, signal.SIGTERM)
    process = None  # Reset the process variable after stopping


def kill_python():
    subprocess.run("killall python python3", shell=True)

def gui_wave():
    subprocess.run("cd ~/c1c0-main/c1c0-scheduler && make gui-wave", shell=True)

def gui_detect():
    subprocess.run("cd ~/c1c0-main/c1c0-scheduler && make gui-detect", shell=True)


# Ensure Tkinter runs in a virtual display (for headless environments)
if "DISPLAY" not in os.environ:
    os.environ["DISPLAY"] = ":0"


# Create main window
def initialize_gui():
    root = tk.Tk()
    root.title("Command Runner")
    root.config(background='black')
    root.geometry("1280x720")

    cust_font = tkFont.Font(family='Helvetica', size=18, weight='bold')

    # Create frames to align buttons
    button_frame = tk.Frame(root, bg="black")
    button_frame.pack(expand=True)  # Makes sure frame is centered
    side_button_frame = tk.Frame(button_frame, bg="black")
    side_button_frame.pack(side=tk.RIGHT, padx=20)

    # Create buttons
    run_button = tk.Button(button_frame, text="Run Scheduler", fg='white', bg='red', command=run_command, height=4, width=50, font=cust_font)
    stop_button = tk.Button(button_frame, text="Stop Scheduler", fg='white', bg='red', command=stop_command, height=4, width=50, font=cust_font)
    kill_button = tk.Button(button_frame, text="Kill Python", fg='white', bg='red', command=kill_python, height=4, width=50, font=cust_font)

    # Place buttons in frame (centered)
    run_button.pack(pady=10)
    stop_button.pack(pady=10)
    kill_button.pack(pady=10)

    # Place button in side frame
    wave_button = tk.Button(side_button_frame, text="Wave Hello", fg='white', bg='blue', command=gui_wave, height=3, width=20, font=cust_font)
    object_button = tk.Button(side_button_frame, text="Detect Object", fg='white', bg='blue', command=gui_detect, height=3, width=20, font=cust_font)
    placeholder2 = tk.Button(side_button_frame, text="Button 3", fg='white', bg='gray', height=3, width=20, font=cust_font)
    placeholder3 = tk.Button(side_button_frame, text="Button 4", fg='white', bg='gray', height=3, width=20, font=cust_font)

    wave_button.pack(pady=5)
    object_button.pack(pady=5)
    placeholder2.pack(pady=5)
    placeholder3.pack(pady=5)

    # Run the GUI
    stop_button.focus_set()
    root.mainloop()


while True:
   try: initialize_gui()
   except Exception as e:
      print(f"Waiting for GUI to become available: {e}")
      time.sleep(0.2) # Small delay, not needed but recommended
