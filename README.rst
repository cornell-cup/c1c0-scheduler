*****
Scheduler
*****
This scheduler API allows for a cohesive integration of all the modules built by the CUP robotics team for whichever robot implementation they wish to use it with.

Usage:
######
See ``c1c0_scheduler/system.py`` for the base classes to implement.

See ``c1c0_scheduler/c1c0/system.py`` for an example implementation.

Two processes are started in parallel:
######
chatbot_scheduler.py runs the main chatbot program for input commands, and spawns new processes to run in parallel with everything else for each subsystem.

The locomotion takes input both from chatbot and an Xbox controller (as a synchronized multithreaded process) to handle all locomotion commands with no interference.



*****
C1C0
*****
Adding a new module:
######
Just run the

USAGE:
######

