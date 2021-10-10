*****
c1c0-scheduling
*****
This scheduler API allows for a cohesive integration of all the modules built by the CUP robotics team for C1C0.

Integrating all modules:
######
In this repo are the programs intended to directly run on C1C0's main Jetson, from which processes are managed based on chatbot and Xbox controller input. In order for these programs to work, install all modules for chatbot, locomotion, facial recognition, and object detection. These should be available by cloning each Git repo and running the setup commands (thank you Chris!), which lets you use pip to install the modules in your environment - which allows each of the import lines for these modules to work.

Two processes are started in parallel:
######
chatbot_scheduler.py runs the main chatbot program for input commands, and spawns new processes to run in parallel with everything else for each subsystem.

The locomotion takes input both from chatbot and an Xbox controller (as a synchronized multithreaded process) to handle all locomotion commands with no interference.
