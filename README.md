# c1c0-scheduling
Integrating all modules

In this repo are the programs intended to directly run on C1C0's main Jetson, from which processes are managed based on chatbot and Xbox controller input. In order for these programs to work, install all modules for chatbot, locomotion, facial recognition, and object detection. These should be available by cloning each Git repo and running the setup commands (thank you Chris!), which lets you use pip to install the modules in your environment - which allows each of the import lines for these modules to work.

Two processes are started in parallel:
chatbot_scheduler.py runs the main chatbot program for input commands, and spawns new processes to run in parallel with everything else for each subsystem.

The locomotion takes input both from chatbot and an Xbox controller (as a synchronized multithreaded process) to handle all locomotion commands with no interference.

## Refactoring April 2023:
- Cleaned up the scheduler into usable packages by CS.

### Old branches archived
- scheduler-refactor
  - An original attempt to refactor the scheduler. Was at some point discontinued, details unclear.
- scheduler-path-planning
  - A branch that integrated with path-planning's terrabee and scheduler needs. Great for reference.
- grpc-impl
  - A gRPC implementation developed at the suggestion of Professor Ken Birman.
- scheduler-testing
  - An out of date, but very useful example of xbox controller integration.

To see/use the above archived branches, checkout the Tags in this repository.
For eg) to see the state of scheduler-testing at when it was archived, click on [tags](https://github.com/cornell-cup/c1c0-scheduling/tags), and click on
the commit version (in this case, it should be `9d79f8a`, unless it has been further updated.) From here, hit Browse files to see the repository in the
state it was in when that branch was archived.
