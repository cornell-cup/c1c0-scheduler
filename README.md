# Scheduler

### Overview

This repository handles communication between various subsystems. The subsystems are specified in the file structure below, each subystem has a client file and a specification file and may use utilities from `api`. The client files are stored in `clients` and are copied over to their respective subsystem directory when built. The specification files are stored in `specs` and tell the scheduler how to handle the various communications the subsytem can send to it. The scheduler itself depends on communication protocols and utilities stored within `scheduler`. The makefile commands are specified below in the order they should be run:

`make venv`: Creates the virtual environment and installs required packages.

`make build`: Copies over the various clients to their respective directories.

`make [all]`: Starts the scheduler and all required subsystems for C1C0 operation.

`make [subsytem]`: Starts a specific subsystem and displays its communications in terminal.

`make clean`: Removes all copied over client files and temporary directories.

### File Structure

```py
api/ # Folder Containing API Utilities
|-- __init__.py      # Making API A Package
|-- locomotionAPI.py # Locomotion Utilities
|-- preciseAPI.py    # Precise Arm Utilities
|-- rotateAPI.py     # Head Rotation Utilities
|-- serialAPI.py     # General Serial Utilities
|-- strongAPI.py     # Strong Arm Utilities

assets/ # Folder Containing Data Files
|-- r2d2-1.mp3 # C1C0 Sound 1
|-- r2d2-2.mp3 # C1C0 Sound 2
|-- r2d2-3.mp3 # C1C0 Sound 3
|-- r2d2-4.mp3 # C1C0 Sound 4
|-- r2d2-5.mp3 # C1C0 Sound 5

clients/ # Folder Containing Client Files
|-- __init__.py   # Make Clients A Package
|-- controller.py # Xbox Controller Client
|-- facial.py     # Facial Recognition Client
|-- manual.py     # Manual Control Client
|-- movement.py   # C1C0 Locomotion Client

scheduler/ # Folder Containing Scheduler Files
|-- __init__.py   # Make Scheduler A Package
|-- client.py     # Client Template For Subsystems
|-- config.py     # Configuration Variables
|-- server.py     # Server Template For Scheduler
|-- utils.py      # Utility Functions And Classes

specs/
|-- __init__.py   # Make Specs A Package
|-- controller.py # Xbox Controller Specification
|-- facial.py     # Facial Recognition Specification
|-- manual.py     # Manual Control Specification
|-- movement.py   # C1C0 Locomotion Specification

.gitignore        # Git Ignore Specifications
makefile          # Build & Run Commands
README.md         # Information File
requirements.txt  # Required Python Packages
scheduler.py      # Scheduler Server File
```

### Adding A Subsystem

If you want to add a subsytem, follow these instructions to make your life easier. First figure out a specification file for the client, all the scheduler really is a massive data queue that you can `get` and `put` data. So make a specification file that can handle your requests to scheduler, and then add it to the mapping found in `scheduler.py`. Now create a client file within `clients` to send the requests and deal with the response that the server gives (based on earlier specification), if any extra utilities or assets are needed, you can put them within the `api` or `assets` folder respectively. Final step is to add a makefile command and then test your code before commiting. Once all these steps are done, you have added a subsystem to scheduler, yay! 
