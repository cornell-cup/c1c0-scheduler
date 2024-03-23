# Scheduler

### Overview

This repository handles communication between various subsystems. The subsystems are specified in the file structure below, each subystem has a client file and a specification file. The client files are stored in `clients` and are copied over to their respective subsystem directory when built. The specification files are stored in `specs` and tell the scheduler how to handle the various communications the subsytem can send to it. The scheduler itself depends on communication protocols and utilities stored within `scheduler`. The makefile commands are specified below in the order they should be run:

`make venv`: Creates the virtual environment and installs required packages.

`make build`: Copies over the various clients to their respective directories.

`make [all]`: Starts the scheduler and initiates socket communication.

`make [subsytem]`: Starts the respective subsytem and initiates socket communication.

`make [clean]`: Removes all copied over client files and temporary directories.

### File Structure

```py
clients/          # Folder Containing Client Files
|-- __init__.py   # Make Clients A Package
|-- facial.py     # Facial Recognition Client
|-- manual.py     # Manual Control Client

scheduler/        # Folder Containing Scheduler Files
|-- __init__.py   # Make Scheduler A Package
|-- client.py     # Client Template For Subsystems
|-- config.py     # Configuration Variables
|-- server.py     # Server Template For Scheduler
|-- utils.py      # Utility Functions And Classes

specs/
|-- __init__.py   # Make Specs A Package
|-- facial.py     # Facial Recognition Specification
|-- manual.py     # Manual Control Specification

.gitignore        # Git Ignore Specifications
makefile          # Build & Run Commands
README.md         # Information File
requirements.txt  # Required Python Packages
scheduler.py      # Scheduler Server File
```
